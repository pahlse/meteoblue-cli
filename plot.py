import pandas as pd
import matplotlib.pyplot as plt
import json

# Load the JSON weather data
with open('./meteoblue/weather_cache/weatherreport.json', 'r') as file:
    weather_data = json.load(file)

# Extract data
rainspot_data = weather_data['data_3h']['rainspot']
timestamps_3h = pd.to_datetime(weather_data['data_3h']['time'])
hourly_rainfall = weather_data['data_1h']['precipitation']
hourly_temp = weather_data['data_1h']['temperature']
hourly_timestamps = pd.to_datetime(weather_data['data_1h']['time'])

# Function to filter data dynamically based on input datetime and duration
# Function to filter data dynamically based on input datetime and duration
def get_data_from_datetime(input_datetime, duration_hours):
    num_intervals = max(1, duration_hours // 3)  # Calculate the number of 3-hour intervals
    input_datetime = pd.Timestamp(input_datetime)
    
    # Get the 3-hourly timestamps and data for the specified range
    valid_timestamps_3h = timestamps_3h[timestamps_3h >= input_datetime][:num_intervals]
    indices_3h = [timestamps_3h.get_loc(ts) for ts in valid_timestamps_3h]
    input_strings = [rainspot_data[i] for i in indices_3h]
    timestamps = valid_timestamps_3h

    # Get the hourly timestamps and data for the specified range
    start_index_hourly = hourly_timestamps.get_loc(hourly_timestamps[hourly_timestamps >= input_datetime][0])
    indices_hourly = range(start_index_hourly, start_index_hourly + max(3, duration_hours))
    hourly_rainfall_filtered = [hourly_rainfall[i] for i in indices_hourly]
    hourly_timestamps_filtered = hourly_timestamps[indices_hourly]

    return input_strings, timestamps, hourly_rainfall_filtered, hourly_timestamps_filtered, num_intervals

# Example usage
input_datetime = "2024-12-24T09:00:00"  # Input datetime
duration_hours = 9  # Number of hours to display (e.g., next 6 hours)
input_strings, timestamps, hourly_rainfall_filtered, hourly_timestamps_filtered, num_intervals = get_data_from_datetime(input_datetime, duration_hours)

# Define color mapping for rainspots
colors = {
    '0': '#f0f0f0',
    '1': '#7bccc4',
    '2': '#43a2ca',
    '3': '#0868ac',
    '9': '#a8ddb5'
}

# Split hourly rainfall into chunks of 3 for each rainspot grid
rainfall_chunks = [hourly_rainfall_filtered[i:i + 3] for i in range(0, len(hourly_rainfall_filtered), 3)]

# Plot rainspots and corresponding hourly rainfall dynamically
fig, axes = plt.subplots(2, num_intervals, figsize=(5 * num_intervals, 10), gridspec_kw={'height_ratios': [2, 1]})

if num_intervals == 1:
    axes = [[axes[0]], [axes[1]]]  # Wrap single Axes into lists for consistency

# Plot rainspot grids (top row)
for idx, (ax, input_string, timestamp) in enumerate(zip(axes[0], input_strings, timestamps)):
    grid_size = 7
    rows = [input_string[i:i + grid_size] for i in range(0, len(input_string), grid_size)][::-1]
    color_grid = [[colors[char] for char in row] for row in rows]

    # Plot the grid
    for y, row in enumerate(color_grid):
        for x, color in enumerate(row):
            ax.add_patch(plt.Rectangle((x, y), 1, 1, color=color))

    # Draw concentric circles
    for i in range(1, 5):
        circle = plt.Circle((3.5, 3.5), radius=i - 0.5, color='black', fill=False, linewidth=1)
        ax.add_patch(circle)

    # Add timestamp as title
    ax.set_title(timestamp.strftime("%Y-%m-%d %H:%M:%S"), fontsize=10)

    # Configure the axis
    ax.set_xlim(0, grid_size)
    ax.set_ylim(0, grid_size)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')

# Plot hourly rainfall chunks (bottom row)
for idx, (ax, rainfall_chunk) in enumerate(zip(axes[1], rainfall_chunks)):
    ax.bar(range(len(rainfall_chunk)), rainfall_chunk, color='blue', alpha=0.7, width=0.5)
    ax.set_xticks(range(len(rainfall_chunk)))
    ax.set_xticklabels([hourly_timestamps_filtered[i].strftime("%H:%M") for i in range(idx * 3, idx * 3 + 3)])
    ax.set_ylim(0, max(hourly_rainfall_filtered) + 1)  # Adjust y-axis based on max rainfall
    ax.set_ylabel("Rainfall (mm)", fontsize=8)
    ax.set_xlabel("Hour", fontsize=8)

# Adjust layout and show
# Adjust layout and save to file
plt.tight_layout()
plt.savefig("rainspot_plot.png", dpi=300, bbox_inches="tight")
# plt.show()
