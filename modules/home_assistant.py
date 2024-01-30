from dotenv import load_dotenv
import os
import requests

load_dotenv()

def get_states(token):
    """
    This allows you to see and control my lights.

    Args:
        token (str): the token variable found within this function

    Returns:
        array: An array of JSON objects
    """
    token = os.getenv('HA_TOKEN')
    url = os.getenv('HA_BASE_URL')+"/api/states"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.get(url, headers=headers, verify=False)
        print("Response:", response)
        print("Response history:", response.history)
        print("Content-Type:", response.headers['Content-Type'])  # Check content type
        print("Response content:", response.text)  # Print response body

        if response.status_code == 200:
            try:
                return response.json()  # Attempt to parse JSON
            except ValueError as e:
                print("JSON decoding failed:", e)
                return None
        else:
            print(f"Error: {response.status_code}, Response Content: {response.content}")
            return []
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []