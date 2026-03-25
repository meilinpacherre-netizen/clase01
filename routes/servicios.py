from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/servicios", tags=["servicios"])

servicios_db = [
    {"nombre": "consulta", "precio": 50},
    {"nombre": "baño", "precio": 60},
    {"nombre": "corte", "precio": 100}
]

class ServicioIn(BaseModel):
    nombre: str
    precio: float

@router.get("")
def listar_servicios():
    return {
        "servicios": servicios_db
    }

@router.post("/agregar")
def agregar_servicio(servicio: ServicioIn):
    nuevo = servicio.dict()
    servicios_db.append(nuevo)
    return {"ok": True, "servicio": nuevo}
