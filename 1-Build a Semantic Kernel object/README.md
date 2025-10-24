# Semantic Kernel Python Lab

## Build a Semantic Kernel object

This lab shows how to create a Python client application using the Semantic Kernel SDK to connect to an Azure OpenAI chat model and run prompts.

### Prerequisites

* Python 3.10+ installed
* Git installed
* Azure account with OpenAI service

### Setup

1. Create and activate a virtual environment:

```bash
python -m venv labenv
./labenv/bin/Activate.ps1  # For PowerShell
```

2. Install required libraries:

```bash
pip install python-dotenv semantic-kernel[azure]
```


### Running the Code

```bash
python kernel.py
```

Expected output:

```
Assistant > Certainly! Here's a list of popular breakfast foods that incorporate eggs and cheese:
1. Omelette
2. Frittata
3. Breakfast burrito
4. Scrambled eggs with cheese
5. Quiche
6. Huevos rancheros
7. Cheese and egg sandwich
8. Egg and cheese bagel
9. Egg and cheese croissant
10. Baked eggs with cheese
```

### Summary

* Created a Python client for Semantic Kernel
* Connected to Azure OpenAI chat deployment
* Ran a prompt using the kernel

