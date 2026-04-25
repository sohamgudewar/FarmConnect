from sqlalchemy import Column, Integer, String, DateTime
from backend.database import Base
from datetime import datetime

class MarketPrice(Base):
    __tablename__ = "market_prices"

    id = Column(Integer, primary_key=True, index=True)
    state = Column(String, index=True)
    district = Column(String, index=True)
    market = Column(String, index=True)
    commodity = Column(String, index=True)
    variety = Column(String)
    min_price = Column(Integer)
    max_price = Column(Integer)
    modal_price = Column(Integer)
    arrival_date = Column(String)  # Usually provided as DD/MM/YYYY in government data
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
