from typing import Annotated
import requests
import os
from semantic_kernel.functions import kernel_function
from dotenv import load_dotenv

load_dotenv(override=True)

class WeatherPlugin:
    @kernel_function(
        name="get_future_weather_forecast",
        description="Get weather forecast for a specific location and number of days in the future"
    )
    async def get_future_weather_forecast(
        self,
        latitude: Annotated[float, "The latitude of the location"],
        longitude: Annotated[float, "The longitude of the location"],
        days: Annotated[int, "Number of days to forecast (1-16)"]
    ): 
        try:
            response = requests.get(url=f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,showers,snowfall,weather_code,wind_speed_10m,wind_direction_10m,wind_gusts_10m&hourly=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation_probability,precipitation,rain,showers,snowfall,weather_code,cloud_cover,wind_speed_10m,uv_index&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch&forecast_days={days}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error fetching weather data: {str(e)}"
        

    @kernel_function(
        name="get_past_weather_forecast",
        description="Get weather forecast for a specific location and number of days in the past"
    )
    async def get_past_weather_forecast(
        self,
        latitude: Annotated[float, "The latitude of the location"],
        longitude: Annotated[float, "The longitude of the location"],
        daysInPast: Annotated[int, "Number of days to forecast (1-16)"]
    ): 
        try:
            response = requests.get(url=f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=weather_code,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,sunrise,sunset,daylight_duration,uv_index_max,precipitation_sum,rain_sum,showers_sum,snowfall_sum,precipitation_hours,wind_speed_10m_max,wind_gusts_10m_max&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch&past_days={daysInPast}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error fetching weather data: {str(e)}"
        
    