import requests

def get_weather_data(coordinates):
    """
    Fetches weather data from the Open-Meteo API for the given latitude and longitude.

    Args:
    coordinates (tuple): The latitude of the location.

    Returns:
    float: The current temperature in the coordinates you've asked for
    """
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
    """
    Fetches the latitude and longitude of a given city name using the Maps.co Geocoding API.

    Args:
    city_name (str): The name of the city.

    Returns:
    tuple: The latitude and longitude of the city.
    """
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