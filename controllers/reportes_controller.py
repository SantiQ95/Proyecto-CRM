from databases.db import usuarios_collection, facturas_collection
import json
import os
from datetime import datetime
from pathlib import Path

# controllers/reportes_controller.py
def mostrar_resumen_financiero(output_dir=None):
    print("\n=== RESUMEN FINANCIERO ===")

    if output_dir is None:
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "reportes"))

    os.makedirs(output_dir, exist_ok=True)

    # Human-readable timestamp for JSON content
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    usuarios = list(usuarios_collection.find())
    if not usuarios:
        print("No hay usuarios registrados.\n")
        return

    total_facturas = 0
    ingresos_totales = 0
    ingresos_pagados = 0
    ingresos_pendientes = 0
    resumen_por_usuario = []

    for usuario in usuarios:
        email = usuario["email"]
        nombre = f"{usuario['nombre']} {usuario['apellidos']}"
        facturas = list(facturas_collection.find({"email_cliente": email}))

        total = sum(f["monto"] for f in facturas)
        pagadas = sum(f["monto"] for f in facturas if f["estado"] == "Pagada")
        pendientes = sum(f["monto"] for f in facturas if f["estado"] == "Pendiente")

        print(f"\nUsuario: {nombre} ({email})")
        print(f"- Total facturas: {len(facturas)}")
        print(f"- Monto total: ${total:.2f}")
        print(f"- Facturas pagadas: ${pagadas:.2f}")
        print(f"- Facturas pendientes: ${pendientes:.2f}")

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

    print("\n--- RESUMEN GENERAL ---")
    print(f"Total usuarios: {len(usuarios)}")
    print(f"Total facturas emitidas: {total_facturas}")
    print(f"Ingresos totales: ${ingresos_totales:.2f}")
    print(f"Ingresos recibidos: ${ingresos_pagados:.2f}")
    print(f"Ingresos pendientes: ${ingresos_pendientes:.2f}\n")

    resumen_final = {
        "timestamp": timestamp,
        "resumen_general": {
            "total_usuarios": len(usuarios),
            "total_facturas": total_facturas,
            "ingresos_totales": ingresos_totales,
            "ingresos_pagados": ingresos_pagados,
            "ingresos_pendientes": ingresos_pendientes
        },
        "usuarios": resumen_por_usuario
    }

    # Generate safe, date-based filename and prevent overwrite by adding suffix if needed
    base_name = f"resumen_financiero_{datetime.now().strftime('%Y-%m-%d')}.json"
    filepath = Path(output_dir) / base_name
    counter = 1
    while filepath.exists():
        filepath = Path(output_dir) / f"resumen_financiero_{datetime.now().strftime('%Y-%m-%d')}_{counter}.json"
        counter += 1

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(resumen_final, f, ensure_ascii=False, indent=4)

    print(f"📂 Resumen financiero guardado en: {filepath}")
