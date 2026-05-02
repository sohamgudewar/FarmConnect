from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from backend.services.maps_service import maps_service
from backend.schemas.location import NearbyPlace, NearbyPlacesResponse
from backend.database import SessionLocal
from backend.models.listing import Listing
from backend.schemas.listing import ListingOut
from sqlalchemy.orm import Session
from math import radians, cos, sin, asin, sqrt

router = APIRouter(tags=["Location"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

@router.get("/nearby-apmcs", response_model=NearbyPlacesResponse)
def get_nearby_apmcs(
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    address: Optional[str] = None,
    radius: int = 50000
):
    if address:
        coords = maps_service.geocode_address(address)
        if not coords:
            raise HTTPException(status_code=400, detail="Could not geocode address")
        lat, lng = coords
    
    if lat is None or lng is None:
        raise HTTPException(status_code=400, detail="Latitude and longitude or address required")
    
    places = maps_service.get_nearby_places(lat, lng, query="APMC", radius=radius)
    return {"places": places}

@router.get("/nearby-listings", response_model=List[ListingOut])
def get_nearby_listings(
    lat: float,
    lng: float,
    radius_km: float = 50.0,
    db: Session = Depends(get_db)
):
    # This is a naive implementation. For large datasets, use PostGIS.
    all_listings = db.query(Listing).filter(Listing.latitude != None, Listing.longitude != None).all()
    
    nearby = []
    for listing in all_listings:
        dist = haversine(lng, lat, listing.longitude, listing.latitude)
        if dist <= radius_km:
            # We can't easily add distance to the ListingOut schema without refactoring
            # so we just return the listings for now.
            nearby.append(listing)
    
    return nearby
