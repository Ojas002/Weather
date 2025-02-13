import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Weather App", layout="wide")

# Custom CSS for background and styling
st.markdown(
    """
    <style>
    .stApp {
        background: url('https://upload.wikimedia.org/wikipedia/commons/2/2c/Rotating_earth_%28large%29.gif');
        background-size: cover;
    }
    .weather-card {
        background-color: transparent;
        padding: 20px;
        border-radius: 10px;
        margin: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("🌍 Global Weather App")

# Create columns for layout
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='weather-card'>", unsafe_allow_html=True)
    city = st.text_input("Enter City Name", "London")
    st.markdown("</div>", unsafe_allow_html=True)

# API key (replace with your own from OpenWeatherMap)
API_KEY = "a39236f6346c88dd4e106071548384c8"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_data(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        return data
    except:
        return None

if city:
    weather_data = get_weather_data(city)
    
    if weather_data and weather_data.get("cod") != "404":
        with col2:
            st.markdown("<div class='weather-card'>", unsafe_allow_html=True)
            st.subheader(f"Weather in {city}")
            
            # Display weather information
            temp = weather_data["main"]["temp"]
            humidity = weather_data["main"]["humidity"]
            pressure = weather_data["main"]["pressure"]
            wind_speed = weather_data["wind"]["speed"]
            description = weather_data["weather"][0]["description"]
            
            # Create metrics
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Temperature", f"{temp}°C")
            col_b.metric("Humidity", f"{humidity}%")
            col_c.metric("Wind Speed", f"{wind_speed} m/s")
            
            # Additional weather info
            st.write(f"**Condition:** {description.capitalize()}")
            st.write(f"**Pressure:** {pressure} hPa")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Create historical data visualization
            st.markdown("<div class='weather-card'>", unsafe_allow_html=True)
            st.subheader("24-Hour Forecast")
            
            # Simulate forecast data (replace with actual API data if available)
            forecast_temps = [temp + i * 0.5 for i in range(-12, 12)]
            forecast_hours = pd.date_range(start=datetime.now(), periods=24, freq='H')
            
            forecast_df = pd.DataFrame({
                'Time': forecast_hours,
                'Temperature': forecast_temps
            })
            
            fig = px.line(forecast_df, x='Time', y='Temperature',
                         title='Temperature Forecast')
            st.plotly_chart(fig)
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.error("City not found. Please try another city name.")