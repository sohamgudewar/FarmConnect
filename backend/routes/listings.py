from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models.listing import Listing
from backend.models.user import User
from backend.schemas.listing import ListingCreate
from backend.routes.auth import get_current_user
from backend.services.maps_service import maps_service

router = APIRouter(tags=["Listings"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/listings")
def create_listing(
    listing: ListingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    listing_data = listing.model_dump()
    
    # Auto-geocode if coordinates are missing
    if listing_data.get("latitude") is None or listing_data.get("longitude") is None:
        coords = maps_service.geocode_address(listing_data["location"])
        if coords:
            listing_data["latitude"], listing_data["longitude"] = coords

    db_listing = Listing(**listing_data, owner_id=current_user.id)
    db.add(db_listing)
    db.commit()
    db.refresh(db_listing)
    return db_listing


@router.get("/listings")
def get_listings(db: Session = Depends(get_db)):
    return db.query(Listing).all()
