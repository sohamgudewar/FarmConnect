from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.database import SessionLocal
from backend.models.market_price import MarketPrice
from backend.schemas.market_price import MarketPriceOut
from backend.services.price_sync import fetch_and_sync_prices, get_mock_maharashtra_data

router = APIRouter(tags=["Market Prices"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/prices", response_model=List[MarketPriceOut])
def get_latest_prices(
    district: Optional[str] = None,
    commodity: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(MarketPrice)
    if district:
        query = query.filter(MarketPrice.district.ilike(f"%{district}%"))
    if commodity:
        query = query.filter(MarketPrice.commodity.ilike(f"%{commodity}%"))
    
    return query.order_by(MarketPrice.updated_at.desc()).all()

@router.post("/prices/sync")
def sync_prices(db: Session = Depends(get_db)):
    """
    Manually triggers a sync with Agmarknet. 
    If API key is missing, it populates with mock Maharashtra data.
    """
    count = fetch_and_sync_prices(db)
    if count == 0:
        # If API fails (likely due to missing key), use mock data for hackathon demo
        count = get_mock_maharashtra_data(db)
        return {"message": "API Sync failed or returned no data. Populated with Mock Maharashtra data.", "count": count}
    
    return {"message": "Prices synced successfully from Agmarknet", "count": count}

@router.get("/prices/districts")
def get_available_districts(db: Session = Depends(get_db)):
    districts = db.query(MarketPrice.district).distinct().all()
    return [d[0] for d in districts]

@router.get("/prices/commodities")
def get_available_commodities(db: Session = Depends(get_db)):
    commodities = db.query(MarketPrice.commodity).distinct().all()
    return [c[0] for c in commodities]
