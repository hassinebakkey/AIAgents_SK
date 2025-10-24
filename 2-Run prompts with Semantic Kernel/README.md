Run prompts with Semantic Kernel
# Run prompts with Semantic Kernel

In this exercise, you'll use Semantic Kernel to create an AI assistant that suggests suitable roles based on a user's skills and interests, identifies missing skills for a target role, and recommends courses to close the skill gap.

## Steps Overview

### 1. Environment Setup
```bash
python -m venv labenv
./labenv/bin/Activate.ps1 ou .\labenv\Scripts\Activate.ps1 (windows)
pip install python-dotenv semantic-kernel[azure]
```

### 2. Configuration
Create a `.env` file with your Azure credentials:
```
DEPLOYMENT_NAME="gpt-4o"
AZURE_OPENAI_ENDPOINT="https://your-endpoint.openai.azure.com/"
AZURE_OPENAI_KEY="your_api_key"
```

### 3. Running the Code
Save the following file as `prompts.py` and execute:
```bash
python prompts.py
```

### 4. Expected Output
The assistant will recommend roles, identify missing skills, and respond interactively.

 

