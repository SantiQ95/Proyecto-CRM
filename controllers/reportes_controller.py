from databases.db import usuarios_collection, facturas_collection
import json
import os
from datetime import datetime
from pathlib import Path

# ——— Shared Logic ———

def _calcular_resumen_financiero():
    usuarios = list(usuarios_collection.find())
    if not usuarios:
        return None, "No hay usuarios registrados."

    total_facturas = ingresos_totales = ingresos_pagados = ingresos_pendientes = 0
    resumen_por_usuario = []

    for usuario in usuarios:
        email = usuario["email"]
        nombre = f"{usuario['nombre']} {usuario['apellidos']}"
        facturas = list(facturas_collection.find({"email_cliente": email}))

        total = sum(f["monto"] for f in facturas)
        pagadas = sum(f["monto"] for f in facturas if f["estado"] == "Pagada")
        pendientes = sum(f["monto"] for f in facturas if f["estado"] == "Pendiente")

        resumen_por_usuario.append({
            "nombre": nombre,
            "email": email,
            "total_facturas": len(facturas),
            "monto_total": total,
            "monto_pagado": pagadas,
            "monto_pendiente": pendientes
        })

        total_facturas += len(facturas)
        ingresos_totales += total
        ingresos_pagados += pagadas
        ingresos_pendientes += pendientes

    resumen_final = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "resumen_general": {
            "total_usuarios": len(usuarios),
            "total_facturas": total_facturas,
            "ingresos_totales": ingresos_totales,
            "ingresos_pagados": ingresos_pagados,
            "ingresos_pendientes": ingresos_pendientes
        },
        "usuarios": resumen_por_usuario
    }

    return resumen_final, None

# ——— CLI Version ———

def mostrar_resumen_financiero(output_dir=None):
    print("\n=== RESUMEN FINANCIERO ===")
    resumen_final, error = _calcular_resumen_financiero()
    if error:
        print(f"❌ {error}\n")
        return

    for usuario in resumen_final["usuarios"]:
        print(f"\nUsuario: {usuario['nombre']} ({usuario['email']})")
        print(f"- Total facturas: {usuario['total_facturas']}")
        print(f"- Monto total: ${usuario['monto_total']:.2f}")
        print(f"- Facturas pagadas: ${usuario['monto_pagado']:.2f}")
        print(f"- Facturas pendientes: ${usuario['monto_pendiente']:.2f}")

    g = resumen_final["resumen_general"]
    print("\n--- RESUMEN GENERAL ---")
    print(f"Total usuarios: {g['total_usuarios']}")
    print(f"Total facturas emitidas: {g['total_facturas']}")
    print(f"Ingresos totales: ${g['ingresos_totales']:.2f}")
    print(f"Ingresos recibidos: ${g['ingresos_pagados']:.2f}")
    print(f"Ingresos pendientes: ${g['ingresos_pendientes']:.2f}\n")

    guardar_resumen_en_archivo(resumen_final, output_dir)

# ——— API Version ———

def obtener_resumen_financiero_json():
    return _calcular_resumen_financiero()

def guardar_resumen_en_archivo(resumen, output_dir=None):
    if output_dir is None:
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "reportes"))

    os.makedirs(output_dir, exist_ok=True)
    filename = f"resumen_financiero_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    filepath = Path(output_dir) / filename

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(resumen, f, ensure_ascii=False, indent=4)

    return str(filepath)
