import os
import asyncio
from semantic_kernel import Kernel
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.functions.kernel_arguments import KernelArguments
from flight_booking_plugin import FlightBookingPlugin

async def main():

    # Set your Azure OpenAI values directly
    api_key = ""
    endpoint = ""
    deployment_name = "gpt-4o"

    kernel = Kernel()
    chat_completion = AzureChatCompletion(
        api_key=api_key,
        endpoint=endpoint,
        deployment_name=deployment_name
    )
    kernel.add_service(chat_completion)

    # Add the plugin to the kernel
    kernel.add_plugin(FlightBookingPlugin(), "flight_booking_plugin")

    # Configure function choice behavior
    settings = AzureChatPromptExecutionSettings(
        function_choice_behavior=FunctionChoiceBehavior.Auto(),
    )
    #    # Configure function choice behavior
    #settings=AzureChatPromptExecutionSettings(
    #   function_choice_behavior=FunctionChoiceBehavior.Auto(filters={"included_functions": ["search_flights"]}),
    #)


    chat_history = ChatHistory()
    chat_history.add_system_message("The year is 2025 and the current month is January")

    async def get_reply():
        reply = await chat_completion.get_chat_message_content(
            chat_history=chat_history,
            kernel=kernel,
            settings=settings
        )
        print("Assistant:", reply)
        chat_history.add_assistant_message(str(reply))

    def get_input():
        user_input = input("User: ")
        if user_input.strip() != "":
            chat_history.add_user_message(user_input)
        return user_input

    def add_user_message(msg: str):
        print(f"User: {msg}")
        chat_history.add_user_message(msg)

    chat_history.add_user_message("Find me a flight to Tokyo on the 19")
    await get_reply()
    get_input()
    await get_reply()

if __name__ == "__main__":
    asyncio.run(main())
