import requests
import os
from sqlalchemy.orm import Session
from backend.models.market_price import MarketPrice
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Data.gov.in API configuration
# Get your API key from https://data.gov.in/
OGD_API_KEY = os.getenv("OGD_API_KEY", "YOUR_API_KEY_HERE")
AGMARKNET_RESOURCE_ID = "9ef273d1-c142-454d-8061-cff5884610b1"
BASE_URL = "https://api.data.gov.in/resource/"
0
def fetch_and_sync_prices(db: Session, district: str = None):
    """
    Fetches latest prices from Agmarknet API and syncs with local database.
    Filters for Maharashtra by default.
    """
    params = {
        "api-key": OGD_API_KEY,
        "format": "json",
        "offset": 0,
        "limit": 100,
        "filters[state]": "Maharashtra"
    }
    
    if district:
        params["filters[district]"] = district

    url = f"{BASE_URL}{AGMARKNET_RESOURCE_ID}"
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        records = data.get("records", [])
        sync_count = 0
        
        for record in records:
            # Create or Update logic (Upsert)
            # We identify a unique record by market, commodity, variety, and arrival_date
            existing = db.query(MarketPrice).filter(
                MarketPrice.market == record["market"],
                MarketPrice.commodity == record["commodity"],
                MarketPrice.variety == record["variety"],
                MarketPrice.arrival_date == record["arrival_date"]
            ).first()
            
            if existing:
                existing.min_price = int(record["min_price"])
                existing.max_price = int(record["max_price"])
                existing.modal_price = int(record["modal_price"])
                existing.updated_at = datetime.utcnow()
            else:
                new_price = MarketPrice(
                    state=record["state"],
                    district=record["district"],
                    market=record["market"],
                    commodity=record["commodity"],
                    variety=record["variety"],
                    min_price=int(record["min_price"]),
                    max_price=int(record["max_price"]),
                    modal_price=int(record["modal_price"]),
                    arrival_date=record["arrival_date"]
                )
                db.add(new_price)
            sync_count += 1
            
        db.commit()
        logger.info(f"Successfully synced {sync_count} market price records.")
        return sync_count

    except Exception as e:
        logger.error(f"Error syncing prices: {e}")
        db.rollback()
        return 0

def get_mock_maharashtra_data(db: Session):
    """
    Populates the database with mock data for demonstration if API is unavailable.
    """
    mock_data = [
        {"market": "Lasalgaon", "district": "Nashik", "commodity": "Onion", "variety": "Red", "min_price": 1500, "max_price": 2200, "modal_price": 1900, "arrival_date": "25/04/2026"},
        {"market": "Pune", "district": "Pune", "commodity": "Tomato", "variety": "Local", "min_price": 800, "max_price": 1200, "modal_price": 1000, "arrival_date": "25/04/2026"},
        {"market": "Nagpur", "district": "Nagpur", "commodity": "Orange", "variety": "Mandarin", "min_price": 3000, "max_price": 4500, "modal_price": 4000, "arrival_date": "25/04/2026"},
        {"market": "Amravati", "district": "Amravati", "commodity": "Cotton", "variety": "Other", "min_price": 6500, "max_price": 7200, "modal_price": 6900, "arrival_date": "25/04/2026"}
    ]
    
    for item in mock_data:
        new_price = MarketPrice(
            state="Maharashtra",
            district=item["district"],
            market=item["market"],
            commodity=item["commodity"],
            variety=item["variety"],
            min_price=item["min_price"],
            max_price=item["max_price"],
            modal_price=item["modal_price"],
            arrival_date=item["arrival_date"]
        )
        db.add(new_price)
    
    db.commit()
    return len(mock_data)
