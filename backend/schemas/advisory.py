from pydantic import BaseModel
from typing import List, Optional

class MarketAdvisoryRequest(BaseModel):
    commodity: str
    city: str
    district: Optional[str] = None

class MarketAdvisoryResponse(BaseModel):
    commodity: str
    city: str
    current_price: Optional[int]
    price_trend: str # "Rising", "Falling", "Stable", or "Unknown"
    weather_summary: str
    advisory: str
    alerts: List[str]
