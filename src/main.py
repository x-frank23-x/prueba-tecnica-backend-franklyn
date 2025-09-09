from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from models.car import Car, CarCreate, CarRead, CarUpdate
from config.db import create_db_and_tables, get_session
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

# Definimos el ciclo de vida de la app
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    print("App finalizada")


# Pasamos lifespan al constructor de FastAPI
app = FastAPI(lifespan=lifespan)


# 🚀 habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],   
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# ✅ Crear un carro
@app.post("/cars", response_model=CarRead)
def create_car(car: CarCreate, session: Session = Depends(get_session)):
    new_car = Car.from_orm(car)
    session.add(new_car)
    session.commit()
    session.refresh(new_car)
    return new_car


# ✅ Listar todos los carros
@app.get("/cars", response_model=list[CarRead])
def get_cars(session: Session = Depends(get_session)):
    return session.exec(select(Car)).all()


# ✅ Actualizar un carro
@app.patch("/cars/{car_id}", response_model=CarRead)
def update_car(car_id: int, car_update: CarUpdate, session: Session = Depends(get_session)):
    car = session.get(Car, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Carro no encontrado")

    car_data = car_update.dict(exclude_unset=True)
    for key, value in car_data.items():
        setattr(car, key, value)

    session.add(car)
    session.commit()
    session.refresh(car)
    return car


# ✅ Eliminar un carro
@app.delete("/cars/{car_id}")
def delete_car(car_id: int, session: Session = Depends(get_session)):
    car = session.get(Car, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Carro no encontrado")

    session.delete(car)
    session.commit()
    return {"message": f"Carro con id {car_id} eliminado"}
