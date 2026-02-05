from sqlalchemy.orm import Session
from models import Car
from schemas import CarCreate


def create_car(db: Session, car: CarCreate):
    existing_car = db.query(Car).filter(
        Car.name == car.name,
        Car.brand == car.brand
    ).first()

    if existing_car:
        return None

    new_car = Car(
        name=car.name,
        brand=car.brand,
        year=car.year,
        price=car.price
    )

    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car


def get_cars(
    db: Session,
    brand: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    skip: int = 0,
    limit: int = 10
):
    query = db.query(Car)

    if brand:
        query = query.filter(Car.brand == brand)

    cars = query.offset(skip).limit(limit).all()
    return cars


def get_car(db: Session, car_id: int):
    return db.query(Car).filter(Car.id == car_id).first()


def update_car(db: Session, car_id: int, car: CarCreate):
    db_car = db.query(Car).filter(Car.id == car_id).first()

    if db_car is None:
        return None

    db_car.name = car.name
    db_car.brand = car.brand
    db_car.year = car.year
    db_car.price = car.price

    db.commit()
    db.refresh(db_car)
    return db_car


def delete_car(db: Session, car_id: int):
    car = db.query(Car).filter(Car.id == car_id).first()

    if car is None:
        return False

    db.delete(car)
    db.commit()
    return True
