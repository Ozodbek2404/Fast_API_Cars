from pydantic import BaseModel


class CarCreate(BaseModel):
    brand: str
    name: str
    car_type: str
    year: int
    country: str
    price: float


class CarResponse(CarCreate):
    id: int

    class Config:
        from_attributes = True
