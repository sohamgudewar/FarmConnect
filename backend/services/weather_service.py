import requests
import os
import logging

logger = logging.getLogger(__name__)

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/"


def get_weather_data(city: str):
    """
    Fetches current weather and forecast for a given city.
    """
    if not OPENWEATHER_API_KEY:
        logger.error("OPENWEATHER_API_KEY not found in environment variables.")
        return None

    try:
        # Get Current Weather
        current_url = f"{BASE_URL}weather"
        params = {
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }
        current_res = requests.get(current_url, params=params)
        current_res.raise_for_status()
        current_data = current_res.json()

        # Get Forecast
        forecast_url = f"{BASE_URL}forecast"
        forecast_res = requests.get(forecast_url, params=params)
        forecast_res.raise_for_status()
        forecast_data = forecast_res.json()

        # Parse current weather
        current = {
            "temp": current_data["main"]["temp"],
            "feels_like": current_data["main"]["feels_like"],
            "humidity": current_data["main"]["humidity"],
            "description": current_data["weather"][0]["description"],
            "icon": current_data["weather"][0]["icon"],
            "wind_speed": current_data["wind"]["speed"],
            "city": current_data["name"]
        }

        # Parse forecast (next 5 intervals)
        forecast = []
        for item in forecast_data["list"][:5]:
            forecast.append({
                "dt_txt": item["dt_txt"],
                "temp": item["main"]["temp"],
                "description": item["weather"][0]["description"],
                "icon": item["weather"][0]["icon"]
            })

        # Basic "Alert" logic based on forecast (since One Call API for real alerts is often paid/restricted)
        alerts = []
        for item in forecast_data["list"][:8]: # Check next 24 hours
            desc = item["weather"][0]["description"].lower()
            if "rain" in desc or "storm" in desc:
                alerts.append(f"Precipitation expected at {item['dt_txt']}: {desc}")

        return {
            "current": current,
            "forecast": forecast,
            "alerts": list(set(alerts))  # Deduplicate
        }

    except Exception as e:
        logger.error(f"Error fetching weather data for {city}: {e}")
        return None
