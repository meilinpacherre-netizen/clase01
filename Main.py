from fastapi import FastAPI
from fastapi.responses import FileResponse
from routes.servicios import router as servicios_router
from routes.auth import router as auth_router

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

# Incluir routers modularizados
app.include_router(servicios_router)
app.include_router(auth_router)
