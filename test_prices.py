from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import Base
from backend.models.market_price import MarketPrice
from backend.services.price_sync import fetch_and_sync_prices, get_mock_maharashtra_data
import os

# Test setup: In-memory SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_temp.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def test_market_price_logic():
    # Create tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    print("Testing Mock Data Injection...")
    count = get_mock_maharashtra_data(db)
    print(f"Mock sync added {count} records.")

    prices = db.query(MarketPrice).all()
    for p in prices:
        print(f"Market: {p.market}, Commodity: {p.commodity}, Price: {p.modal_price}")

    assert count == 4
    assert len(prices) == 4

    print("Testing Filter logic...")
    onion = db.query(MarketPrice).filter(MarketPrice.commodity == "Onion").first()
    assert onion.market == "Lasalgaon"
    
    print("All internal logic tests passed! (API sync skipped due to key requirement)")
    
    db.close()
    # Cleanup
    os.remove("./test_temp.db")

if __name__ == "__main__":
    test_market_price_logic()
