from pydantic import BaseModel

class HouseModel(BaseModel):
    id: int
    price: float
    bedrooms: int
    center_distance: float
    last_known_change: int

    class Config:
        orm_mode = True