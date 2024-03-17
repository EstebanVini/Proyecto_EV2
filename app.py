import sqlite3
import datetime
import json
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.backend.users import crear_usuaio, login, eliminar_usuario
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Running"}

#____________________________________________Usuarios_______________________________________________________

@app.post("/crear_usuario")
async def guardar_usuario(usuario: dict):
    if crear_usuaio(usuario):
        return {"message": "Se ha creado el usuario exitosamente", "estado": True}
    else:
        return {"message": "No se ha podido crear el usuario", "estado": False}

@app.post("/inicio_sesion")
async def inicio_sesion(usuario: dict):
    if login(usuario):
        return {"message": "Inicio de sesión exitoso", "estado": True}
    else:
        return {"message": "No se ha podido iniciar sesión", "estado": False}

@app.delete("/eliminar_usuario/{username}")
async def eliminar_usuario_db(username: str):
    if eliminar_usuario(username):
        return {"message": "Se ha eliminado el usuario exitosamente"}
    else:
        return {"message": "No se ha podido eliminar el usuario"}


if __name__ == "__main__":


    uvicorn.run(app, host="0.0.0.0", port=8081)