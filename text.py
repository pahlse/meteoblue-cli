import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# Data (example)
num_intervals = 3
precipitation = [1.2, 0.0, 3.4]
precipitation_probability = [80, 10, 50]
relativehumidity = [65, 40, 70]
felttemperature = [20, 22, 18]
windspeed = [2.0, 1.5, 3.0]
totalcloudcover = [40, 20, 70]
fog_probability = [5, 0, 10]
visibility = [9000, 10000, 8000]
uvindex = [5, 6, 4]
airqualityindex = [50, 45, 60]

# Create a blank figure
fig, ax = plt.subplots(figsize=(8, 6))
fig.patch.set_visible(False)
ax.axis("off")  # Turn off axes

# Render text for each interval
y_offset = 1  # Initial y position
line_spacing = 0.15  # Space between lines
for idx in range(num_intervals):
    text_data = (
        f"{'Rain:':<15}"
        f"{('<1 mm'.rjust(10) if precipitation[idx] < 1 else f'{int(precipitation[idx])}-{int(precipitation[idx]) + 1} mm'.rjust(10))}\n"
        f"{'Rain Prob:':<15}{str(precipitation_probability[idx]).rjust(5)}%\n"
        f"{'Humidity:':<15}{str(relativehumidity[idx]).rjust(5)}%\n"
        f"{'Temp:':<15}{str(felttemperature[idx]).rjust(5)}°C\n"
        f"{'Wind:':<15}{f'{windspeed[idx]*3.6:>.1f}'.rjust(6)} km/h\n"
        f"{'Cloud Cover:':<13}{str(totalcloudcover[idx]).rjust(4)}%\n"
        f"{'Fog Prob:':<15}{str(fog_probability[idx]).rjust(5)}%\n"
        f"{'Visibility:':<15}{f'{visibility[idx] / 1000:.1f}'.rjust(5)} km\n"
        f"{'UV Index:':<15}{str(uvindex[idx]).rjust(5)}/11\n"
        f"{'Pollution:':<15}{str(airqualityindex[idx]).rjust(5)}/100"
    )

    # Add text to the figure
    ax.text(
        0.1, y_offset,  # Position
        text_data,
        fontsize=10,
        ha="left", va="top", family="sans-serif"
    )
    y_offset -= len(text_data.split("\n")) * line_spacing  # Adjust y position

# Save to PNG
canvas = FigureCanvas(fig)
canvas.print_png("weather_summary.png")
print("Weather summary saved as weather_summary.png")
