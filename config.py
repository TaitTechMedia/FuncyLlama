RAVEN_PROMPT = \
'''
Function:
def get_coordinates_from_city:
    """
    Fetches the latitude and longitude of a given city name using the Maps.co Geocoding API.

    Args:
    city_name (str): The name of the city.

    Returns:
    tuple: The latitude and longitude of the city.
    """

Function:
def get_weather_data:
    """
    Fetches weather data from the Open-Meteo API for the given latitude and longitude.

    Args:
    coordinates (tuple): The latitude of the location.

    Returns:
    float: The current temperature in the coordinates you've asked for
    """

Function:
def gather_information_code:
    """
    Fetches coding information from a specialized Large Language Model

    Args:
    query (str): The user input to the LLM.

    Returns:
    string: The answer to the user's query.
    """

Function:
def gather_information_general:
    """
    Fetches general information from another Large Language Model

    Args:
    query (str): The user input to the LLM.

    Returns:
    string: The answer to the user's query.
    """

User Query: {query}
'''
