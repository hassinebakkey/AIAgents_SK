import asyncio
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.functions.kernel_arguments import KernelArguments

async def main():
    # --- Définition directe des variables ---
    api_key = ""
    endpoint = ""
    deployment_name = ""

    # --- Création du Kernel et ajout du service Azure Chat ---
    kernel = Kernel()
    chat_completion = AzureChatCompletion(
        api_key=api_key,
        endpoint=endpoint,
        deployment_name=deployment_name
    )
    kernel.add_service(chat_completion)

    # --- Test du service de chat ---
    response = await kernel.invoke_prompt(
        "Give me a list of 10 breakfast foods with eggs and cheese",
        KernelArguments()
    )
    print("Assistant > " + str(response))

if __name__ == "__main__":
    asyncio.run(main())
