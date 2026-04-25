from sqlalchemy import Column, Integer, String, ForeignKey
from backend.database import Base


class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    crop_name = Column(String)
    quantity = Column(String)
    price = Column(String)
    location = Column(String)
    contact = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"))

class AdditionalInfo(Base):
    __tablename__ = "additional_info"

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id"))
    soil_type = Column(String)
    irrigation_method = Column(String)
    fertilizer_used = Column(String)
