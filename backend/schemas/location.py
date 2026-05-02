from pydantic import BaseModel
from typing import List, Optional


class LocationInfo(BaseModel):
    address: str
    latitude: float
    longitude: float


class NearbyPlace(BaseModel):
    name: str
    address: str
    latitude: float
    longitude: float
    distance_km: Optional[float] = None
    place_id: str


class NearbyPlacesResponse(BaseModel):
    places: List[NearbyPlace]
