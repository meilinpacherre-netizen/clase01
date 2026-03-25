from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
app = FastAPI()
@app.get("/")
def saludar():
    return {"mensaje": "¡Hola! Bienvenido a mi API"}
@app.get("/bienvenido/{nombre}")
def saludar_persona(nombre: str):
    return {"mensaje": f"Hola {nombre}, ¡qué bueno verte por aquí!"}
@app.get("/favicon.ico")
def favicon():
    return FileResponse("path/a/favicon.ico")

servicios_db = [
    {"nombre": "consulta", "precio": 50},
    {"nombre": "baño", "precio": 60},
    {"nombre": "corte", "precio": 100}
]
@app.get("/servicios")
def listar_servicios():
    return {
        "servicios": servicios_db
    }

class ServicioIn(BaseModel):
    nombre: str
    precio: float

@app.post("/agregar-servicio")
def agregar_servicio(servicio: ServicioIn):
    nuevo = servicio.dict()
    servicios_db.append(nuevo)
    return {"ok": True, "servicio": nuevo}
