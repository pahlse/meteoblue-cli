A command-line weather application that fetches detailed weather forecasts from
the Meteoblue API and formats them into an easy-to-read ASCII report. A free
meteoblue API Key is available at [https://content.meteoblue.com/en](https://content.meteoblue.com/en).

## Features

- Fetch current weather data using the **Meteoblue API**.
- Supports custom locations using the **OpenStreetMap Nominatim API**.
- Formats weather data into **ASCII based reports**.
- Saves reports to disk for offline viewing.
- Automatically backs up weather data in a structured directory.


## Configuration

### API Key
Update the `API_KEY` variable in `main.py` with your personal Meteoblue API key.

### Custom Locations
Modify the `location` variable in `main.py` to use a city name or coordinates:

```python
location = "New York, USA"
location = "40.66, -73.93"
```
