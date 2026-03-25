from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])

usuarios_db = []

class CredencialesIn(BaseModel):
    correo: str
    contraseña: str

@router.post("/register")
def register(credenciales: CredencialesIn):
    usuario = credenciales.dict()
    usuarios_db.append(usuario)
    return {"ok": True, "mensaje": "Usuario registrado exitosamente", "usuario": usuario}

@router.post("/login")
def login(credenciales: CredencialesIn):
    return {"ok": True, "mensaje": "Login exitoso", "usuario": credenciales.dict()}
