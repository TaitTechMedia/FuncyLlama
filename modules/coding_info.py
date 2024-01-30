from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Ollama
import os
from dotenv import load_dotenv
load_dotenv()

def gather_information_code(query):
    """
    This tool can answer quesitons about software and coding. It can generate and understand code.

    Args:
    query (str): The user query.

    Returns:
    string: The answer to the user's query.
    """
    llm = Ollama(
        model="codellama",
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        base_url=os.getenv('OLLAMA_BASE_URL')
    )
    print("Handing to Codellama\n")
    llm.invoke(query)