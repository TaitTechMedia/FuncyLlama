from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Ollama

import os
import importlib

# Generate the RAVEN_PROMPT (config.py) from the docstrings in each module function - This allows us
#   to easily maintain our modules without needs to break up the configs
from func_prompt_gen import generate_config
generate_config()
from config import RAVEN_PROMPT

# Import all functions from all py files in the modules directory
modules_directory = 'modules'
function_files = [f[:-3] for f in os.listdir(modules_directory) if f.endswith('.py') and f != '__init__.py']
for module_name in function_files:
    module_path = f'{modules_directory}.{module_name}'
    module = importlib.import_module(module_path)
    globals().update({name: getattr(module, name) for name in dir(module) if callable(getattr(module, name))})

# LLM Configuration
llm = Ollama(
    model="nexusraven",
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    base_url="http://192.168.1.234:11434" # This can be used to access a remote instance of Ollama on your LAN or over the internet
)

def query_raven(prompt):
    # Use the Ollama instance to process the prompt
    output = llm(prompt)
    call = output.replace("Call:", "").strip()
    return call

# Chatbot Loop
while True:
    # Step 2: User Input
    user_input = input("Ask me anything: ")
    
    # Check for exit condition
    if user_input.lower() == 'exit()':
        print("Exiting chatbot.")
        break

    # Step 3: Process the Query
    my_question = RAVEN_PROMPT.format(query=user_input)
    raven_call = query_raven(my_question)

    # Step 4: Execute the Function Call
    function_call = raven_call.split('\n')[0].strip()
    
    try:
        print("\n\n\n")
        exec(function_call)
        print("\n")
    except Exception as e:
        print(f"An error occurred: {e}")