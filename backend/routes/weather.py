from fastapi import APIRouter, HTTPException, Query
from backend.services.weather_service import get_weather_data
from backend.schemas.weather import WeatherResponse

router = APIRouter()

@router.get("/weather", response_model=WeatherResponse)
def get_weather(city: str = Query(..., description="City name to fetch weather for")):
    """
    Get current weather and 5-day forecast for a city.
    Includes automated alerts for rain/storms.
    """
    data = get_weather_data(city)
    if not data:
        raise HTTPException(status_code=404, detail=f"Weather data for '{city}' not found or service unavailable.")
    return data
