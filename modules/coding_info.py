from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Ollama

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
        base_url="http://192.168.1.234:11434"
    )
    print("Handing to Codellama\n")
    llm.invoke(query)