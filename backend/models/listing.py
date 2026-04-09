from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    crop_name = Column(String)
    quantity = Column(String)
    price = Column(String)
    location = Column(String)
    contact = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"))
