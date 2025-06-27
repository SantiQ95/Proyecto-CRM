from fastapi import FastAPI, Header, HTTPException
from models.usuario import Usuario
from databases.db import usuarios_collection
from dotenv import load_dotenv
from datetime import datetime
import os

# Load environment variables
load_dotenv()

# Load API keys from .env
AUTHORIZED_KEYS = {
    os.getenv("API_PUBLIC_KEY"),
    os.getenv("API_PUBLIC_KEY1"),
    os.getenv("API_PUBLIC_KEY2")
}
AUTHORIZED_KEYS.discard(None)  # Remove any missing keys

app = FastAPI(
    title="EvolveCRM API",
    description="Allows external creation of users using public API keys, with daily limits",
    version="1.0.0"
)

def _today_range():
    """Returns UTC ISO date range for today's start and end."""
    today = datetime.utcnow().strftime("%Y-%m-%d")
    start = f"{today}T00:00:00Z"
    end = f"{today}T23:59:59Z"
    return start, end

@app.post("/usuarios", summary="Crear un nuevo usuario")
def crear_usuario(
    nombre: str,
    apellidos: str,
    email: str,
    telefono: str,
    direccion: str,
    x_api_key: str = Header(...)
):
    if x_api_key not in AUTHORIZED_KEYS:
        raise HTTPException(status_code=403, detail="🔐 Clave API inválida o ausente")

    now = datetime.utcnow()
    start, end = _today_range()

    # Check daily usage by this key
    usos_hoy = usuarios_collection.count_documents({
        "creado_por": x_api_key,
        "fecha_creacion": {"$gte": start, "$lte": end}
    })

    if usos_hoy >= 35:
        raise HTTPException(status_code=429, detail="🚫 Límite diario de 35 usuarios alcanzado para esta clave")

    # Create and store user
    usuario = Usuario(nombre, apellidos, email, telefono, direccion)
    usuario_dict = usuario.to_dict()
    usuario_dict["creado_por"] = x_api_key
    usuario_dict["fecha_creacion"] = now.isoformat()

    usuarios_collection.insert_one(usuario_dict)

    return {
        "message": f"✅ Usuario {nombre} {apellidos} creado correctamente.",
        "usuarios_creados_hoy_con_esta_clave": usos_hoy + 1,
        "limite_diario": 35
    }
