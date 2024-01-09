from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Ollama

import requests

# LLM Configuration

llm = Ollama(
    model="nexusraven",
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    base_url="http://192.168.1.234:11434" # This can be used to access a remote instance of Ollama on your LAN or over the internet
)

# Functions
def get_weather_data(coordinates):
    latitude, longitude = coordinates
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m",
        "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m"
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        print (f"""Temperature in C: {response.json()["current"]["temperature_2m"]}""")
    else:
        return {"error": "Failed to fetch data, status code: {}".format(response.status_code)}
    
def get_coordinates_from_city(city_name):
    base_url = "https://geocode.maps.co/search"
    params = {"q": city_name}

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data:
            # Assuming the first result is the most relevant
            return data[0]["lat"], data[0]["lon"]
        else:
            return {"error": "No data found for the given city name."}
    else:
        return {"error": "Failed to fetch data, status code: {}".format(response.status_code)}
    
def gather_information_general(query):
    llm = Ollama(
        model="mistral",
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        base_url="http://192.168.1.234:11434"
    )
    print("\nHanding to Mistral\n")
    llm(query)

def gather_information_code(query):
    llm = Ollama(
        model="codellama",
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        base_url="http://192.168.1.234:11434"
    )
    print("Handing to Codellama\n")
    llm(query)


# Prompt and request to LLM
RAVEN_PROMPT = \
'''
Function:
def get_weather_data(coordinates):
    """
    Fetches weather data from the Open-Meteo API for the given latitude and longitude.

    Args:
    coordinates (tuple): The latitude of the location.

    Returns:
    float: The current temperature in the coordinates you've asked for
    """

Function:
def get_coordinates_from_city(city_name):
    """
    Fetches the latitude and longitude of a given city name using the Maps.co Geocoding API.

    Args:
    city_name (str): The name of the city.

    Returns:
    tuple: The latitude and longitude of the city.
    """

Function:
def gather_information_general(query):
    """
    Fetches general information from another Large Language Model

    Args:
    query (str): The user input to the LLM.

    Returns:
    string: The answer to the user's query.
    """

Function:
def gather_information_code(query):
    """
    Fetches coding information from a specialized Large Language Model

    Args:
    query (str): The user input to the LLM.

    Returns:
    string: The answer to the user's query.
    """

User Query: {query}
'''

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