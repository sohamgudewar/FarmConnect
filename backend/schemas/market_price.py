from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MarketPriceBase(BaseModel):
    state: str
    district: str
    market: str
    commodity: str
    variety: str
    min_price: int
    max_price: int
    modal_price: int
    arrival_date: str

class MarketPriceOut(MarketPriceBase):
    id: int
    updated_at: datetime

    class Config:
        from_attributes = True
