# Semantic Kernel Flight Booking Lab

# Create Semantic Kernel plugins

In this exercise, you'll use Semantic Kernel to create an AI assistant that can search for and book flights for a user. You'll create custom plugin functions to help accomplish the task.

## Deploy a chat completion model

1. Open the [Azure AI Foundry portal](https://ai.azure.com) and sign in.
2. Search for the `gpt-4o` model and select **Use this model**.
3. Create a new project with valid settings for your Azure resource, subscription, resource group, and region.
4. Wait for the project to be created and view the chat playground.
5. Under **Libraries**, select **Azure OpenAI** to get your API key and endpoint.

## Create an AI client app

6. Set up the environment and install libraries:

   **Python**:

   ```powershell
   python -m venv labenv
   ./labenv/bin/Activate.ps1 ou .\labenv\Scripts\Activate.ps1 (windows)
   pip install python-dotenv semantic-kernel[azure]
   ```


## Summary

You successfully created an AI assistant with Semantic Kernel and Azure OpenAI that can search and book flights.
