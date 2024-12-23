import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import json

from scipy.signal import argrelextrema
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="Temperature and Precipitation Visualization", layout="wide")

# Load the JSON weather data
with open('./meteoblue/weather_cache/weatherreport.json', 'r') as file:
    weather_data = json.load(file)


# Sample weather data (replace with real data as needed)
daily_data = [
    {"day": "Mon", "date": "Today", "temp": "19°C", "wind": "22 km/h", "precip": "5 h", "icon": "🌞"},
    {"day": "Tue", "date": "Tomorrow", "temp": "18°C", "wind": "14 km/h", "precip": "2 h", "icon": "⛈"},
    {"day": "Wed", "date": "12-25", "temp": "16°C", "wind": "10 km/h", "precip": "4 h", "icon": "🌞"},
    {"day": "Thu", "date": "12-26", "temp": "20°C", "wind": "14 km/h", "precip": "3 h", "icon": "🌦"},
    {"day": "Fri", "date": "12-27", "temp": "21°C", "wind": "11 km/h", "precip": "-", "icon": "🌞"},
    {"day": "Sat", "date": "12-28", "temp": "22°C", "wind": "17 km/h", "precip": "5 h", "icon": "🌤"},
    {"day": "Sun", "date": "12-29", "temp": "23°C", "wind": "12 km/h", "precip": "9 h", "icon": "🌞"},
]

# Layout for 7 boxes
st.title("7-Day Weather Forecast")

columns = st.columns(7)  # Create 7 equal columns

for i, col in enumerate(columns):
    with col:
        st.subheader(daily_data[i]["day"])
        st.text(daily_data[i]["date"])
        st.markdown(f"<h1 style='text-align: center;'>{daily_data[i]['icon']}</h1>", unsafe_allow_html=True)
        st.text(f"Temp: {daily_data[i]['temp']}")
        st.text(f"Wind: {daily_data[i]['wind']}")
        st.text(f"Precip: {daily_data[i]['precip']}")



# Extract temperature, precipitation, and datetime
temperature = np.array(weather_data['data_1h']['temperature'])
precipitation = np.array(weather_data['data_1h']['precipitation'])
time = pd.to_datetime(weather_data['data_1h']['time'])

current_datetime = pd.Timestamp(datetime.now())

# Create a DataFrame
df = pd.DataFrame({
    'Datetime': time,
    'Temperature': temperature,
    'Precipitation': precipitation
})

# Identify maximum and minimum
local_maxima = argrelextrema(temperature, np.greater)[0]
local_minima = argrelextrema(temperature, np.less)[0]

# Prepare Plotly figure
fig = go.Figure()

# Add precipitation bars
fig.add_trace(
    go.Bar(
        x=df['Datetime'],
        y=df['Precipitation'],
        name="Precipitation",
        marker=dict(color='blue', opacity=0.6),
        yaxis="y2"  # Secondary y-axis
    )
)

# Add line for temperature
fig.add_trace(
    go.Scatter(
        x=df['Datetime'],
        y=df['Temperature'],
        mode='lines',
        line=dict(color='green', width=2),
        name="Temperature",
    )
)

# Add maxima points
fig.add_trace(
    go.Scatter(
        x=df['Datetime'].iloc[local_maxima],
        y=df['Temperature'].iloc[local_maxima],
        mode='markers+text',
        marker=dict(size=10, color='orange', symbol='triangle-up'),
        text=[f"{temperature[_]:.2f}" for _ in local_maxima],
        textposition='top center',
        name="Maxima",
        showlegend=False
    )
)

# Add minima points
fig.add_trace(
    go.Scatter(
        x=df['Datetime'].iloc[local_minima],
        y=df['Temperature'].iloc[local_minima],
        mode='markers+text',
        marker=dict(size=10, color='blue', symbol='triangle-down'),
        text=[f"{temperature[_]:.2f}" for _ in local_minima],
        textposition='bottom center',
        name="Minima",
        showlegend=False
    )
)

# Configure layout with secondary y-axis
fig.update_layout(
    shapes=[
        dict(
            type='line',
            x0=current_datetime,
            x1=current_datetime,
            y0=df['Temperature'].min(),
            y1=df['Temperature'].max(),
            line=dict(color="red", width=2, dash="dash"),
            xref='x',
            yref='y'
        )
    ],
    title="Temperature and Precipitation Forecast",
    xaxis_title="Datetime",
    yaxis=dict(title="Temperature (°C)", side='left'),
    yaxis2=dict(title="Precipitation (mm)", overlaying='y', side='right'),
    template="plotly_white",
    xaxis=dict(
        range=[
            df['Datetime'].min(),  # Start date
            df['Datetime'].min() + pd.Timedelta(days=4)  # Start date + 4 days
        ]
    )
)

# Streamlit app
st.title("Temperature and Precipitation Forecast")
st.write("This plot shows temperature and precipitation data over time, with one maximum and minimum identified per 12-hour interval.")

# Display the plot
st.plotly_chart(fig, use_container_width=True)
