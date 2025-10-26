# Create an AI Assistant with Semantic Kernel

## Description

In this lab, you will learn how to use **Semantic Kernel** to build a generative AI assistant that can perform **DevOps tasks**. You will create a Python client application that interacts with Azure OpenAI GPT-4o model, defines plugins for DevOps actions, and applies filters for user consent.

---

## Prerequisites

* Python 3.10 or higher installed on your system
* Azure subscription with Azure OpenAI resource deployed
* Visual Studio Code installed (optional, for editing configuration files)
* Basic knowledge of Python and asynchronous programming

---

## 1. Setup Python Environment (Windows)

1. Open a terminal (PowerShell) in the folder containing your lab code.
2. Create a virtual environment:

   ```powershell
   python -m venv labenv
   ```
3. Activate the virtual environment:

   ```powershell
   .\labenv\Scripts\Activate.ps1
   ```
4. Install required packages:

   ```powershell
   pip install python-dotenv azure-identity semantic-kernel[azure]
   ```

---

## 2. Configure the Application

1. Open the configuration file `.env` in a code editor.
2. Replace placeholders with your Azure OpenAI details:

   ```text
   AZURE_OPENAI_ENDPOINT="YOUR_AZURE_OPENAI_ENDPOINT"
   AZURE_OPENAI_KEY="YOUR_AZURE_OPENAI_KEY"
   MODEL_ID="gpt-4o"
   ```
3. Save the changes.

---

## 3. Run the AI DevOps Assistant

1. Open a terminal in the lab folder (with `labenv` activated).
2. Run the application:

   ```powershell
   python devops.py
   ```
3. Interact with the assistant by typing commands, for example:

   ```
   User: Please build the stage environment
   User: Please deploy the stage environment
   User: Please create a new branch
   ```
4. For deployment to production, the assistant will ask for approval:

   ```
   System Message: The assistant requires approval to complete this operation. Do you approve (Y/N)
   ```

---

