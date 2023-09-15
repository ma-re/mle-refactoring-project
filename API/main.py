from fastapi import Depends, FastAPI, HTTPException 
import schemas
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
def index():
    return {"data": "house list"}

# get all user
@app.get("/houses", response_model=list[schemas.HouseModel])
def get_all_houses(db: Session = Depends(get_db)):
    house = db.query(models.House).all()
    if not house:
        raise HTTPException(status_code=404, detail="Houses not found")
    return house


# add user
@app.post("/houses", response_model=schemas.HouseModel)
def create_house(request: schemas.HouseModel, db: Session = Depends(get_db)):
    new_house = models.House(id=request.id, price=request.price, bedrooms=request.bedrooms, 
                             center_distance=request.center_distance, last_known_change=request.last_known_change)
    db.add(new_house)
    db.commit()
    db.refresh(new_house)
    return new_house