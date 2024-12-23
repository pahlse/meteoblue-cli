from data_parser import fetch_osm_location, load_weather_report
from ascii_formatter import format_weather_to_ascii, write_ascii_to_file

def main():
    # Meteoblue API settings
    API_KEY = "wEir9pPKohA5Fvl1"

    # Get location and coordinates
    location = "Varanasi, India"
    coordinates = fetch_osm_location(location)

    if "error" in coordinates:
        print("Error:", coordinates["error"])
        return

    print(f"Location: {coordinates['display_name']}")
    print(f"Latitude: {coordinates['latitude']}")
    print(f"Longitude: {coordinates['longitude']}")

    # Load weather report
    weather_data = load_weather_report()

    # Format data into ASCII
    ascii_text = format_weather_to_ascii(weather_data, location, coordinates)

    # Write ASCII text to file
    write_ascii_to_file(ascii_text, output_path="meteoblue/weather_cache/weather_report.txt")

if __name__ == "__main__":
    main()
