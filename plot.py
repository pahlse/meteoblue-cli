import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

# Load the JSON weather data
with open('./meteoblue/weather_cache/weatherreport.json', 'r') as file:
    weather_data = json.load(file)

# Input parameters
input_datetime = "2024-12-24T06:00:00"  # Input datetime
duration_hours = 9  # Number of hours to display (e.g., next 24 hours)
input_datetime = pd.Timestamp(input_datetime)

# Find the nearest index for `data_1h`
index_1h = pd.to_datetime(weather_data['data_1h']['time']).searchsorted(input_datetime)
index_1h -= index_1h % 3  # Align to the nearest previous 3-hour interval
index_1h_end = index_1h + duration_hours

# Find the nearest index for `data_3h`
index_3h = pd.to_datetime(weather_data['data_3h']['time']).searchsorted(input_datetime)
index_3h -= index_3h % 3  # Align to the nearest previous 3-hour interval
index_3h_end = index_3h + (duration_hours // 3)


# Extract data
rainspot_data = weather_data['data_3h']['rainspot'][index_3h:index_3h_end]
timestamps_3h = pd.to_datetime(weather_data['data_3h']['time'][index_3h:index_3h_end])
hourly_rainfall = weather_data['data_1h']['precipitation'][index_1h:index_1h_end]
hourly_timestamps = pd.to_datetime(weather_data['data_1h']['time'][index_1h:index_1h_end])
relativehumidity = weather_data['data_3h']['relativehumidity'][index_3h:index_3h_end]
precipitation = weather_data['data_3h']['precipitation'][index_3h:index_3h_end]
precipitation_probability = weather_data['data_3h']['precipitation_probability'][index_3h:index_3h_end]
felttemperature = weather_data['data_3h']['felttemperature'][index_3h:index_3h_end]
totalcloudcover = weather_data['data_3h']['totalcloudcover'][index_3h:index_3h_end]
fog_probability = weather_data['data_3h']['fog_probability'][index_3h:index_3h_end]
visibility = weather_data['data_3h']['visibility'][index_3h:index_3h_end]
windspeed = weather_data['data_3h']['windspeed'][index_3h:index_3h_end]
winddirection = weather_data['data_3h']['winddirection'][index_3h:index_3h_end]
uvindex = weather_data['data_3h']['uvindex'][index_3h:index_3h_end]
airqualityindex = weather_data['data_3h']['airqualityindex'][index_3h:index_3h_end]

# Define color mapping for rainspots
colors = {
    '0': '#f0f0f0',
    '1': '#7bccc4',
    '2': '#43a2ca',
    '3': '#0868ac',
    '9': '#a8ddb5'
}

# Split hourly rainfall into chunks of 3 for each rainspot grid
rainfall_chunks = [hourly_rainfall[i:i + 3] for i in range(0, len(hourly_rainfall), 3)]
num_intervals = len(timestamps_3h)

# Plot rainspots and corresponding hourly rainfall dynamically
fig, axes = plt.subplots(3, num_intervals, figsize=(5 * num_intervals, 15), gridspec_kw={'height_ratios': [2, 2, 1]})

# Handle single-column case
if num_intervals == 1:
    axes = [[axes[0]], [axes[1]], [axes[2]]]

# Plot weather data annotations (top row)
for idx, ax in enumerate(axes[0]):
    text_data = (
        f"{'Rain:':<12}{precipitation[idx]:>6.1f} mm\n"
        f"{'Rain Prob:':<12}{precipitation_probability[idx]:>5}%\n"
        f"{'Humidity:':<12}{relativehumidity[idx]:>5}%\n"
        f"{'Temp:':<12}{felttemperature[idx]:>5}°C\n"
        f"{'Wind:':<12}{windspeed[idx]:>6.1f} m/s\n"
        f"{'Wind Dir:':<12}{winddirection[idx]:>5}°\n"
        f"{'Cloud:':<12}{totalcloudcover[idx]:>5}%\n"
        f"{'Fog Prob:':<12}{fog_probability[idx]:>5}%\n"
        f"{'Visibility:':<12}{visibility[idx] / 1000:>5.1f} km\n"
        f"{'UV Index:':<12}{uvindex[idx]:>5}/11\n"
        f"{'Pollution:':<12}{airqualityindex[idx]:>5}/100"
    )
    dynamic_fontsize = max(8, 32 - num_intervals)  # Dynamically adjust font size
    ax.text(
        0.1, 0.5,  # Adjusted position for left alignment
        text_data,
        fontsize=dynamic_fontsize,
        ha="left",  # Left-align the text block
        va="center",  # Vertically center the block
        linespacing=1.5,
        bbox=dict(facecolor="white", edgecolor="black", pad=5)  # Add padding for aesthetics
    )
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 1)
    ax.axis("off")

# Plot rainspot grids (middle row)
for idx, (ax, rainspot, timestamp) in enumerate(zip(axes[1], rainspot_data, timestamps_3h)):
    grid_size = 7
    rows = [rainspot[i:i + grid_size] for i in range(0, len(rainspot), grid_size)][::-1]
    color_grid = [[colors[char] for char in row] for row in rows]

    # Plot the grid
    for y, row in enumerate(color_grid):
        for x, color in enumerate(row):
            ax.add_patch(plt.Rectangle((x, y), 1, 1, color=color))

    # Add concentric circles
    for i in range(1, 5):  # Number of circles
        circle = plt.Circle((3.5, 3.5), radius=i - 0.5, color='black', fill=False, linewidth=1)
        ax.add_patch(circle)

    # Add wind direction arrow
    wind_dir = winddirection[idx]
    arrow_length = grid_size / 2 * (1 - np.exp(-0.198 * windspeed[idx]))
    angle_rad = np.deg2rad(wind_dir)
    dx, dy = arrow_length * np.sin(angle_rad), arrow_length * np.cos(angle_rad)
    ax.arrow(
        3.5, 3.5,  # Start at the center of the grid
        dx, dy,  # Arrow components
        head_width=0.3, head_length=0.5, fc='black', ec='black'
    )

    # Configure the axis
    ax.set_xlim(0, grid_size)
    ax.set_ylim(0, grid_size)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')

# Plot hourly rainfall chunks (bottom row)
for idx, (ax, rainfall_chunk) in enumerate(zip(axes[2], rainfall_chunks)):
    bars = ax.bar(range(len(rainfall_chunk)), rainfall_chunk, color='blue', alpha=0.7, width=0.5)
    for bar, value in zip(bars, rainfall_chunk):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1, f"{value:.1f}", ha="center", va="bottom", fontsize=dynamic_fontsize - 2)
    ax.set_xticks(range(len(rainfall_chunk)))
    ax.set_xticklabels([hourly_timestamps[i].strftime("%H") for i in range(idx * 3, idx * 3 + 3)], fontsize=dynamic_fontsize - 10)
    ax.set_ylim(0, max(hourly_rainfall) + 1)
    ax.set_yticks([])

# Save and show
plt.tight_layout()
plt.savefig("rainspot_plot.png", dpi=300, bbox_inches="tight")
