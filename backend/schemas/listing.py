from pydantic import BaseModel


class ListingCreate(BaseModel):
    crop_name: str
    quantity: str
    price: str
    location: str
    contact: str


class ListingOut(ListingCreate):
    id: int

    class Config:
        from_attributes = True
