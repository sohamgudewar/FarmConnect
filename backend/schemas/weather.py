from pydantic import BaseModel
from typing import List, Optional

class WeatherCurrent(BaseModel):
    temp: float
    feels_like: float
    humidity: int
    description: str
    icon: str
    wind_speed: float
    city: str

class WeatherForecast(BaseModel):
    dt_txt: str
    temp: float
    description: str
    icon: str

class WeatherResponse(BaseModel):
    current: WeatherCurrent
    forecast: List[WeatherForecast]
    alerts: List[str] = []
