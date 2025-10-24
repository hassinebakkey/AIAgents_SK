import os
import asyncio
from semantic_kernel import Kernel
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.prompt_template import KernelPromptTemplate, HandlebarsPromptTemplate, PromptTemplateConfig


DEPLOYMENT_NAME = "gpt-4o"
AZURE_OPENAI_ENDPOINT = ""
AZURE_OPENAI_KEY = ""


async def main():
    # Create a kernel with Azure OpenAI chat completion
    kernel = Kernel()
    chat_completion = AzureChatCompletion(
        api_key=AZURE_OPENAI_KEY,
        endpoint=AZURE_OPENAI_ENDPOINT,
        deployment_name=DEPLOYMENT_NAME
    )
    kernel.add_service(chat_completion)

    chat_history = ChatHistory()

    async def get_reply():
        # Get the assistant's response
        reply = await chat_completion.get_chat_message_content(
            chat_history=chat_history,
            kernel=kernel,
            settings=AzureChatPromptExecutionSettings()
        )
        print("Assistant:", reply)
        chat_history.add_assistant_message(str(reply))

    # --- First prompt: role recommendations ---
    sk_prompt_template = KernelPromptTemplate(
        prompt_template_config=PromptTemplateConfig(
            template="""
            You are a helpful career advisor. Based on the user's skills and interests, suggest up to 5 suitable roles.
            Return the output as JSON in the following format:
            "Role Recommendations":
            {
                "recommendedRoles": [],
                "industries": [],
                "estimatedSalaryRange": ""
            }

            My skills are: {{$skills}}. My interests are: {{$interests}}. What are some roles that would be suitable for me?
            """,
            name="recommend_roles_prompt",
            template_format="semantic-kernel",
        )
    )

    sk_rendered_prompt = await sk_prompt_template.render(
        kernel,
        KernelArguments(
            skills="Software Engineering, C#, Python, Drawing, Guitar, Dance",
            interests="Education, Psychology, Programming, Helping Others"
        )
    )

    chat_history.add_user_message(sk_rendered_prompt)
    await get_reply()

    # --- Second prompt: skill gap analysis ---
    hb_prompt_template = HandlebarsPromptTemplate(
        prompt_template_config=PromptTemplateConfig(
            template="""
            <message role="system">
            Instructions: You are a career advisor. Analyze the skill gap between 
            the user's current skills and the requirements of the target role.
            </message>
            <message role="user">Target Role: {{targetRole}}</message>
            <message role="user">Current Skills: {{currentSkills}}</message>

            <message role="assistant">
            "Skill Gap Analysis":
            {
                "missingSkills": [],
                "coursesToTake": [],
                "certificationSuggestions": []
            }
            </message>
            """,
            name="missing_skills_prompt",
            template_format="handlebars",
        )
    )

    hb_rendered_prompt = await hb_prompt_template.render(
        kernel,
        KernelArguments(
            targetRole="Game Developer",
            currentSkills="Software Engineering, C#, Python, Drawing, Guitar, Dance"
        )
    )

    chat_history.add_user_message(hb_rendered_prompt)
    await get_reply()

    # --- User interaction ---
    print("Assistant: How can I help you?")
    user_input = input("User: ")
    chat_history.add_user_message(user_input)
    await get_reply()


if __name__ == "__main__":
    asyncio.run(main())
