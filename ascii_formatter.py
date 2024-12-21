import os

def write_ascii_to_file(ascii_text, output_path="weather_report.txt"):
    """Write the formatted ASCII text to a file."""
    with open(output_path, "w") as file:
        file.write(ascii_text)
    print(f"Weather report saved to {output_path}")


def format_weather_to_ascii(weather_data, location, coordinates):
    """Format the weather data into an ASCII art-based string."""
    formatted_text = f"""
    Location: {location}
    Latitude: {coordinates['latitude']}
    Longitude: {coordinates['longitude']}
    
    Weather Summary:
    -----------------------------
    Temperature: {weather_data.get('temperature', 'N/A')} °C
    Rainfall: {weather_data.get('rainfall', 'N/A')} mm
    Snowfall: {weather_data.get('snowfall', 'N/A')} mm
    Humidity: {weather_data.get('humidity', 'N/A')}%
    Windspeed: {weather_data.get('windspeed', 'N/A')} m/s
    -----------------------------
    """
    return formatted_text
