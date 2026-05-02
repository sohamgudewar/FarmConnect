from pydantic import BaseModel
from typing import Optional


class ListingBase(BaseModel):
    crop_name: str
    quantity: str
    price: str
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    contact: str


class ListingCreate(ListingBase):
    pass


class ListingOut(ListingBase):
    id: int

    class Config:
        from_attributes = True
