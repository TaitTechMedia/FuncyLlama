from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Ollama

def gather_information_general(query):
    """
    Fetches general information from another Large Language Model

    Args:
    query (str): The user input to the LLM.

    Returns:
    string: The answer to the user's query.
    """
    llm = Ollama(
        model="mistral",
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        base_url="http://192.168.1.234:11434"
    )
    print("\nHanding to Mistral\n")
    llm(query)