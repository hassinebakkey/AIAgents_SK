import os
import asyncio
from semantic_kernel import Kernel
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.functions.kernel_function_from_prompt import KernelFunctionFromPrompt
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)
from semantic_kernel.prompt_template.handlebars_prompt_template import HandlebarsPromptTemplate
from semantic_kernel.prompt_template.prompt_template_config import PromptTemplateConfig, InputVariable
from typing import Awaitable, Callable
from semantic_kernel.filters import FunctionInvocationContext
from semantic_kernel.functions import FunctionResult
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from pathlib import Path

# Intégration directe des variables d'environnement
MODEL_ID = "gpt-4o"
AZURE_OPENAI_ENDPOINT = ""
AZURE_OPENAI_KEY = ""

# A class for DevOps functions
class DevopsPlugin:
    """A plugin that performs developer operation tasks."""

    @kernel_function(name="DeployToStage")
    def deploy_to_stage(self):
        return "Staging site deployed successfully."

    @kernel_function(name="DeployToProd")
    def deploy_to_prod(self):
        return "Production site deployed successfully."

    @kernel_function(name="CreateNewBranch")
    def create_new_branch(self, branchName: str, baseBranch: str):
        return f"Created new branch `{branchName}` from `{baseBranch}`."

    @kernel_function(name="ReadLogFile")
    def read_log_file(self):
        file_path = Path(__file__).parent / "Files" / "build.log"
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

async def main():
    # Création du kernel avec Azure OpenAI chat completion
    kernel = Kernel()
    chat_completion = AzureChatCompletion(
        api_key=AZURE_OPENAI_KEY,
        endpoint=AZURE_OPENAI_ENDPOINT,
        deployment_name=MODEL_ID
    )
    kernel.add_service(chat_completion)

    # Importer le plugin DevOps
    kernel.add_plugin(DevopsPlugin(), plugin_name="DevopsPlugin")

    # Kernel function pour build stage environment
    @kernel_function(name="BuildStageEnvironment")
    def build_stage_environment(self):
        return "Stage build completed."

    # Création d'une kernel function depuis un prompt pour déployer le stage
    deploy_stage_function = KernelFunctionFromPrompt(
        prompt="""This is the most recent build log:
{{DevopsPlugin.ReadLogFile}}

If there are errors, do not deploy the stage environment. Otherwise, invoke the stage deployment function""",
        function_name="DeployStageEnvironment",
        description="Deploy the staging environment"
    )
    kernel.add_function(plugin_name="DeployStageEnvironment", function=deploy_stage_function)

    # Création d'un prompt Handlebars pour créer une nouvelle branche
    hb_prompt = """<message role="system">Instructions: Before creating a new branch for a user, request the new branch name and base branch name/message>
<message role="user">Can you create a new branch?</message>
<message role="assistant">Sure, what would you like to name your branch? And which base branch would you like to use?</message>
<message role="user">{{input}}</message>
<message role="assistant">"""

    hb_template = HandlebarsPromptTemplate(
        prompt_template_config=PromptTemplateConfig(
            template=hb_prompt, 
            template_format="handlebars",
            name="CreateBranch", 
            description="Creates a new branch for the user",
            input_variables=[
                InputVariable(name="input", description="The user input", is_required=True)
            ]
        ),
        allow_dangerously_set_content=True,
    )

    # Création d'une fonction plugin depuis le prompt
    prompt_function = KernelFunctionFromPrompt(
        function_name="CreateBranch",
        description="Creates a branch for the user",
        template_format="handlebars",
        prompt_template=hb_template,
    )
    kernel.add_function(plugin_name="BranchPlugin", function=prompt_function)

    # Paramètres d'exécution pour invoquer automatiquement les fonctions
    execution_settings = AzureChatPromptExecutionSettings()
    execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    # Historique du chat
    chat_history = ChatHistory()

    # Filtre pour demander l'approbation avant certaines actions
    async def permission_filter(context: FunctionInvocationContext, next: Callable[[FunctionInvocationContext], Awaitable[None]]) -> None:
        await next(context)
        result = context.result
        if context.function.plugin_name == "DevopsPlugin" and context.function.name == "DeployToProd":
            print("System Message: The assistant requires approval to complete this operation. Do you approve (Y/N)")
            should_proceed = input("User: ").strip()
            if should_proceed.upper() != "Y":
                context.result = FunctionResult(
                    function=result.function,
                    value="The operation was not approved by the user",
                )

    # Ajouter le filtre
    kernel.add_filter('function_invocation', permission_filter)

    # Interaction avec l'utilisateur
    async def get_reply():
        reply = await chat_completion.get_chat_message_content(
            chat_history=chat_history,
            kernel=kernel,
            settings=execution_settings
        )
        print("Assistant:", reply)
        chat_history.add_assistant_message(str(reply))

    def get_input():
        user_input = input("User: ")
        if user_input.strip() != "":
            chat_history.add_user_message(user_input)
        return user_input

    print("Press enter to exit")
    print("Assistant: How may I help you?")
    user_input = input("User: ")

    if user_input.strip() != "":
        chat_history.add_user_message(user_input)

    while user_input.strip() != "":
        await get_reply()
        user_input = get_input()


if __name__ == "__main__":
    asyncio.run(main())
