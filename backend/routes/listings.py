from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models.listing import Listing
from backend.models.user import User
from backend.schemas.listing import ListingCreate
from backend.routes.auth import get_current_user

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
    db_listing = Listing(**listing.model_dump(), owner_id=current_user.id)
    db.add(db_listing)
    db.commit()
    db.refresh(db_listing)
    return db_listing


@router.get("/listings")
def get_listings(db: Session = Depends(get_db)):
    return db.query(Listing).all()
