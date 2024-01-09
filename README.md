# FuncyLlama
This is an implementation of Ollama over langchain, utilizin NexusRaven-V2 as a function calling LLM to invoke custom functions as well
as other LLMs.

## Installation
Be sure to install Ollama first. Detail instructions can be found here: `https://github.com/jmorganca/ollama`

Once installed you will need to ensure you have downloaded NexusRaven-V2, Codellama, and Mistral
`ollama pull nexusraven && ollama pull codellama && ollama pull mistral`

After Ollama is installed and you have downloaded the appropriate models you can run the following commands to clone the repo and run
the script:

### Install
```
git clone https://github.com/TaitTechMedia/FuncyLlama
cd FuncyLlama
python3 -m venv venv
source venv/bin/activate
pip install langchain requests
```

### Run
```
source venv/bin/activate
python3 -m app.py
```