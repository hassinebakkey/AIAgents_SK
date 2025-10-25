## Description
In this exercise, you learn how to apply filters on functions with Semantic Kernel. The goal is to consume a previous chat conversation between the user and the assistant to generate a new response, while applying a trust filter on the function result.


---

## 1. Deploy a Chat Completion Model

1. Open the [Azure AI Foundry portal](https://ai.azure.com) and sign in with your Azure credentials.
2. Close any tips or quick start panes.
3. In **Explore models and capabilities**, search for `gpt-4o` and select **Use this model**.
4. When prompted, create a new project:
   - Enter a valid project name.
   - Expand **Advanced options**.
   - Select **Customize** and provide:
     - Azure AI Foundry resource
     - Subscription
     - Resource group
     - Region
5. Click **Create** and wait for the project to deploy.
6. Navigate to the **Overview** page of your project.
7. Under **Libraries**, select **Azure OpenAI** and keep your keys secure.

---

## 2. Prepare the Environment (Python)

1. Open a local terminal.
```

2. Create a virtual environment and activate it (Windows):

```powershell
python -m venv labenv
.\labenv\Scripts\activate
```

4. Install the required libraries:

```
pip install python-dotenv semantic-kernel[azure]
```

5. Edit the configuration file:

```
code .env
```

Replace the placeholders with your Azure OpenAI endpoint, API key, and deployment name. Save and close the editor.

---


## 3. Test the Filter

Run the application:

```
python filters.py
```
