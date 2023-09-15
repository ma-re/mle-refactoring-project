from sqlalchemy import Column, Integer, Float
from database import Base

class House(Base):
    __tablename__ = "houses"
    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float)
    bedrooms = Column(Integer)
    center_distance = Column(Float)
    last_known_change = Column(Integer)