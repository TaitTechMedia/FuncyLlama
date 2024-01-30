from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Ollama
import os
from dotenv import load_dotenv
load_dotenv()

def gather_information_general(query):
    """
    This tool can answer all types of general questions. This tool is a helpful assistant!

    Args:
    query (str): The user query.

    Returns:
    string: The answer to the user's query.
    """
    llm = Ollama(
        model="mistral",
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        base_url=os.getenv('OLLAMA_BASE_URL')
    )
    print("\nHanding to Mistral\n")
    llm.invoke(query)