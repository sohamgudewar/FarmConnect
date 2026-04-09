from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.listing import Listing
from schemas.listing import ListingCreate

router = APIRouter(prefix="/api", tags=["Listings"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/listings")
def create_listing(
    listing: ListingCreate,
    user_id: int,   # 👈 pass from frontend for now
    db: Session = Depends(get_db)
):
    db_listing = Listing(**listing.model_dump(), owner_id=user_id)
    db.add(db_listing)
    db.commit()
    db.refresh(db_listing)
    return db_listing


@router.get("/listings")
def get_listings(db: Session = Depends(get_db)):
    return db.query(Listing).all()
