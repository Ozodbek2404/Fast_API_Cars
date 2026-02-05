from sqlalchemy import Column, Integer, String, Float
from database import Base


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False)
    name = Column(String, nullable=False)
    car_type = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    country = Column(String, nullable=False)
    price = Column(Float, nullable=False)
