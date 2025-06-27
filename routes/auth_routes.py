from fastapi import APIRouter
from datetime import datetime
from databases.db import log_collection  # renamed from trazas_collection

router = APIRouter()

@router.get("/auth/keys", summary="Listar claves públicas disponibles")
def listar_claves_disponibles(nombre: str = None, correo: str = None, app_id: str = None):
    if any([nombre, correo, app_id]):
        log_collection.insert_one({
            "nombre": nombre,
            "correo": correo,
            "app_id": app_id,
            "timestamp": datetime.utcnow()
        })

    return {
        "claves_disponibles": [
            {"alias": "key1", "descripcion": "Clave pública 1 (API_PUBLIC_KEY)"},
            {"alias": "key2", "descripcion": "Clave pública 2 (API_PUBLIC_KEY1)"},
            {"alias": "key3", "descripcion": "Clave pública 3 (API_PUBLIC_KEY2)"}
        ],
        "nota": "Selecciona una clave y colócala en el header x-api-key al hacer tus solicitudes.",
        "rastreo": "Esta llamada ha sido registrada si se proporcionó nombre, correo o app_id."
    }
