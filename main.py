from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
import schemas
import crud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cars CRUD API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/cars/", response_model=schemas.CarResponse, status_code=status.HTTP_201_CREATED)
def create_car(car: schemas.CarCreate, db: Session = Depends(get_db)):
    created_car = crud.create_car(db, car)

    if created_car is None:
        raise HTTPException(
            status_code=400,
            detail="This car already exists"
        )

    return created_car


@app.get("/cars/", response_model=list[schemas.CarResponse])
def read_cars(
    brand: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    db: Session = Depends(get_db)
):
    cars = crud.get_cars(
        db=db,
        brand=brand,
        min_price=min_price,
        max_price=max_price
    )

    return cars


@app.get("/cars/{car_id}", response_model=schemas.CarResponse)
def read_car(car_id: int, db: Session = Depends(get_db)):
    car = crud.get_car(db, car_id)

    if car is None:
        raise HTTPException(
            status_code=404,
            detail="Car not found"
        )

    return car


@app.put("/cars/{car_id}", response_model=schemas.CarResponse)
def update_car(
    car_id: int,
    car: schemas.CarCreate,
    db: Session = Depends(get_db)
):
    updated_car = crud.update_car(db, car_id, car)

    if updated_car is None:
        raise HTTPException(
            status_code=404,
            detail="Car not found"
        )

    return updated_car


@app.delete("/cars/{car_id}", status_code=status.HTTP_200_OK)
def delete_car(car_id: int, db: Session = Depends(get_db)):
    is_deleted = crud.delete_car(db, car_id)

    if not is_deleted:
        raise HTTPException(
            status_code=404,
            detail="Car not found"
        )

    return {
        "success": True,
        "message": "Car deleted"
    }
