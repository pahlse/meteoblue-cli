import os
import pandas as pd
import plotille

from data_parser import fetch_osm_location, load_weather_report
from ascii_formatter import format_weather_to_ascii, write_ascii_to_file

def main():
    # Meteoblue API settings
    api_key = ""

    # Get location and coordinates
    location = "Stephenville, Texas"
    coordinates = fetch_osm_location(location)

    print(coordinates)

    lat = coordinates["latitude"]
    lon = coordinates["longitude"]
    city = coordinates["address"]["town"]

    os.remove("./meteoblue/weather_cache/weatherreport.json")
    weather_data = load_weather_report(api_key, lat, lon, city)


if __name__ == "__main__":
    main()
