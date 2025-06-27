from fastapi import APIRouter, Header, HTTPException
from datetime import datetime
from models.usuario import Usuario
from models.factura import Factura
from controllers.usuario_controller import registrar_usuario_desde_api
from controllers.factura_controller import crear_factura_desde_api
from controllers.reportes_controller import obtener_resumen_financiero_json, guardar_resumen_en_archivo
from databases.db import usuarios_collection, facturas_collection
import os
from dotenv import load_dotenv

router = APIRouter()
load_dotenv()

AUTHORIZED_KEYS = {
    os.getenv("API_PUBLIC_KEY"),
    os.getenv("API_PUBLIC_KEY1"),
    os.getenv("API_PUBLIC_KEY2")
}
AUTHORIZED_KEYS.discard(None)

def _require_auth(x_api_key: str):
    if x_api_key not in AUTHORIZED_KEYS:
        raise HTTPException(status_code=403, detail="🔐 Clave API inválida o ausente")

@router.post("/usuarios", summary="Crear usuario público")
def crear_usuario_publico(
    nombre: str, apellidos: str, email: str,
    telefono: str = "", direccion: str = "",
    x_api_key: str = Header(...)
):
    _require_auth(x_api_key)

    now = datetime.utcnow()
    today = now.strftime("%Y-%m-%d")
    start = f"{today}T00:00:00Z"
    end = f"{today}T23:59:59Z"

    usos_hoy = usuarios_collection.count_documents({
        "creado_por": x_api_key,
        "fecha_creacion": {"$gte": start, "$lte": end}
    })
    if usos_hoy >= 35:
        raise HTTPException(status_code=429, detail="🚫 Límite diario alcanzado")

    usuario, error = registrar_usuario_desde_api(nombre, apellidos, email, telefono, direccion)
    if error:
        raise HTTPException(status_code=400, detail=f"❌ {error}")

    usuario_dict = usuario.to_dict()
    usuario_dict["creado_por"] = x_api_key
    usuario_dict["fecha_creacion"] = now.isoformat()
    usuarios_collection.insert_one(usuario_dict)

    return {
        "message": f"✅ Usuario {nombre} {apellidos} creado correctamente.",
        "usuarios_creados_hoy_con_esta_clave": usos_hoy + 1,
        "limite_diario": 35,
        "usando_api_key": x_api_key
    }

@router.post("/facturas", summary="Crear factura")
def crear_factura_api(
    cliente_email: str, descripcion: str,
    importe: float, estado: str,
    x_api_key: str = Header(...)
):
    _require_auth(x_api_key)

    factura, error = crear_factura_desde_api(cliente_email, descripcion, importe, estado)
    if error:
        raise HTTPException(status_code=404, detail=f"❌ {error}")

    return {
        "message": f"✅ Factura creada exitosamente para {cliente_email}",
        "numero": factura.numero,
        "estado": factura.estado,
        "fecha_emision": factura.fecha_emision,
        "usando_api_key": x_api_key
    }

@router.get("/usuarios", summary="Buscar usuario")
def buscar_usuario(email: str = None, nombre: str = None, x_api_key: str = Header(...)):
    _require_auth(x_api_key)
    if email:
        usuario = usuarios_collection.find_one({"email": email})
    elif nombre:
        usuario = usuarios_collection.find_one({"nombre": {"$regex": nombre, "$options": "i"}})
    else:
        raise HTTPException(status_code=400, detail="Debes proporcionar email o nombre")
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.get("/facturas", summary="Listar facturas de un usuario")
def obtener_facturas(email: str, x_api_key: str = Header(...)):
    _require_auth(x_api_key)
    usuario = usuarios_collection.find_one({"email": email})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    facturas = list(facturas_collection.find({"email_cliente": email}))
    return {
        "usuario": f"{usuario['nombre']} {usuario['apellidos']}",
        "total": len(facturas),
        "facturas": facturas,
        "usando_api_key": x_api_key
    }

@router.get("/reportes", summary="Resumen financiero")
def resumen_financiero(x_api_key: str = Header(...), guardar: bool = False):
    _require_auth(x_api_key)

    resumen, error = obtener_resumen_financiero_json()
    if error:
        raise HTTPException(status_code=404, detail=error)

    if guardar:
        guardar_resumen_en_archivo(resumen)

    return {
        "reporte": resumen,
        "usando_api_key": x_api_key
    }
