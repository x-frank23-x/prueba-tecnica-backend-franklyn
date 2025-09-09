from sqlmodel import SQLModel, Field
from typing import Optional

# Modelo base (solo definición de atributos)
class CarBase(SQLModel):
    brand: str
    branch: str
    applicant_name: str


# Tabla real en la base de datos
class Car(CarBase, table=True):
    __tablename__ = "cars"
    id: Optional[int] = Field(default=None, primary_key=True)


# Modelo para crear (sin id, porque es autoincremental)
class CarCreate(CarBase):
    pass


# Modelo para leer (incluye id)
class CarRead(CarBase):
    id: int


# Modelo para actualizar (todos opcionales)
class CarUpdate(SQLModel):
    brand: Optional[str] = None
    branch: Optional[str] = None
    applicant_name: Optional[str] = None
