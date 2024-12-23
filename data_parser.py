import os
import json
import requests
from datetime import datetime

def _get_file_path(relative_path):
    """Utility function to get the absolute path of a file in the repository."""
    return os.path.join(os.path.dirname(__file__), relative_path)

# Define paths
weather_report_path = _get_file_path("./meteoblue/weather_cache/weatherreport.json")
location_data_path = _get_file_path("./meteoblue/weather_cache/location_data.json")
backup_dir = _get_file_path("./meteoblue/weather_backups")
pictocode_file_path = _get_file_path("./meteoblue/pictocodes.json")

# Ensure directories exist
os.makedirs(os.path.dirname(weather_report_path), exist_ok=True)
os.makedirs(backup_dir, exist_ok=True)


def fetch_osm_location(location_name):
    """
    Fetches latitude and longitude for a given location name using Nominatim API and Openstreetmaps.

    :param location_name: The name of the city, postal code, or location.
    :return: A dictionary with latitude and longitude or an error message.
    """
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location_name,  # The location name or postal code
        "format": "json",    # Response format
        "addressdetails": 1, # Include detailed address in the response
        "limit": 1           # Limit the number of results
    }
    
    try:
        response = requests.get(base_url, params=params, headers={"User-Agent": "meteoblue_weather_cli/1.0"})
        response.raise_for_status()
        data = response.json()
        
        if data:
            output = {
                "latitude": data[0]["lat"],
                "longitude": data[0]["lon"],
                "display_name": data[0]["display_name"],
                "address": data[0]["address"],
            }
            return output
        else:
            return {"error": "Oops! Fetching locaton failed."}
    except requests.RequestException as e:
        return {"error": str(e)}


def fetch_weather_report(API_KEY, LAT, LON, CITY):
    """Fetches weekly wether forecast from the Meteoblue API and save it locally."""

    base_url = (f"https://my.meteoblue.com/packages/basic-15min_basic-1h_basic-3h_basic-day_"
                                f"current_clouds-day_sunmoon_airquality-1h_airquality-3h_airquality-day?"
                                f"apikey={API_KEY}&lat={LAT}&lon={LON}&format=json"
    )

    response = requests.get(base_url)
    response.raise_for_status()
    
    print(f"Fetched new weather data for {CITY}")
    weather_data = response.json()
    with open(weather_report_path, "w") as file:
        json.dump(weather_data, file, indent=4)

    backup_path = os.path.join(backup_dir, CITY.replace(' ', '_'))
    backup_file = os.path.join(
        backup_path, f"{datetime.now().strftime('%Y-%m-%d')}-{CITY.replace(' ', '_')}.json"
    )

    os.makedirs(backup_path, exist_ok=True)
    print(f"Backup saved in  /{CITY}")

    with open(backup_file, "w") as file:
        json.dump(weather_data, file, indent=4)

    return weather_data


def load_weather_report(API_KEY, LAT, LON, CITY):
    """Load the weather report from the local cache or fetch it if missing."""

    if os.path.exists(weather_report_path):
        print(f"Using weather data from cached file.")
        with open(weather_report_path, "r") as file:
            return json.load(file)
    return fetch_weather_report(API_KEY, LAT, LON, CITY)


def get_pictocode_description(pictocode):
    """Look up the description for a pictocode."""

    with open(pictocode_file_path, "r") as file:
        pictocode_data = json.load(file)

    codes = pictocode_data["data_daily"]["pictocode"]
    descriptions = pictocode_data["data_daily"]["en_GB"]
    try:
        index = codes.index(pictocode)
        return descriptions[index]
    except ValueError:
        return "Unknown"


