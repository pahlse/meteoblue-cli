# Meteoblue CLI Weather App 🌦️

A command-line weather application that fetches detailed weather forecasts from
the Meteoblue API and formats them into an easy-to-read ASCII report.


## Features ✨

- Fetch current weather data using the **Meteoblue API**.
- Supports custom locations using the **OpenStreetMap Nominatim API**.
- Formats weather data into **ASCII art-based reports**.
- Saves reports to disk for offline viewing.
- Automatically backs up weather data in a structured directory.


## Directory Structure 📂

```
.
├── main.py                 # The entry point for the application
├── data_parser.py          # Handles data fetching and parsing
├── ascii_formatter.py      # Formats weather data into ASCII and saves output
├── meteoblue
│   ├── pictograms/         # (Optional) Contains weather pictograms
│   ├── weather_cache/      # Contains cached weather reports
│   ├── pictocodes.json     # Maps weather codes to descriptions
├── README.md               # Documentation
```


## Prerequisites ⚙️

- **Python 3.8+**
- Required Python packages: 
  - `requests`
  - `json`
- Meteoblue API Key: Free API key available at [Meteoblue](https://content.meteoblue.com/en).

---


## Example Output 📋

```
Location: Varanasi, India
Latitude: 25.29
Longitude: 82.99

Weather Summary:
-----------------------------
Temperature:        28 °C
Rainfall:           2.5 mm
Snowfall:           0 mm
Humidity:           70%
Windspeed:          3 m/s
Cloud Cover:        20%
Sunshine Hours:     8 h
Visibility:         10 km
-----------------------------
Sunlight:    06:12 AM - 06:48 PM
Moonlight:   07:03 PM - 05:18 AM
```

---

## Configuration ⚙️

### API Key
Update the `API_KEY` variable in `main.py` with your personal Meteoblue API key.

### Custom Locations
Modify the `location` variable in `main.py` to use a city name or coordinates:
```python
location = "New York, USA"  # City name
location = "40.66, -73.93"  # Latitude, Longitude
```

### Directory Structure
- Weather reports are cached in `meteoblue/weather_cache/`.
- Backups are stored in `meteoblue/weather_backups/`.

---
