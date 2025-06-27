import os
import json
import tempfile
from unittest.mock import patch
from controllers import reportes_controller

@patch("controllers.reportes_controller.usuarios_collection")
@patch("controllers.reportes_controller.facturas_collection")
def test_resumen_financiero_multi_usuario(mock_facturas, mock_usuarios):
    mock_usuarios.find.return_value = [
        {"nombre": "Ana", "apellidos": "López", "email": "ana@test.com"},
        {"nombre": "Luis", "apellidos": "Pérez", "email": "luis@test.com"},
        {"nombre": "Sofía", "apellidos": "Ramírez", "email": "sofia@test.com"},
    ]

    def fake_find(query):
        email = query.get("email_cliente", "")
        if email == "ana@test.com":
            return [
                {"monto": 100.0, "estado": "Pagada"},
                {"monto": 50.0, "estado": "Pendiente"},
            ]
        elif email == "luis@test.com":
            return [
                {"monto": 200.0, "estado": "Pagada"},
                {"monto": 100.0, "estado": "Cancelada"},
            ]
        elif email == "sofia@test.com":
            return []
        return []

    mock_facturas.find.side_effect = fake_find

    with tempfile.TemporaryDirectory() as tmpdir:
        with patch("builtins.print") as mock_print:
            reportes_controller.mostrar_resumen_financiero(output_dir=tmpdir)

            printed = [str(call) for call in mock_print.call_args_list]

            assert any("Monto total: $150.00" in call for call in printed)
            assert any("Facturas pagadas: $100.00" in call for call in printed)
            assert any("Facturas pendientes: $50.00" in call for call in printed)

            assert any("Monto total: $300.00" in call for call in printed)
            assert any("Facturas pagadas: $200.00" in call for call in printed)
            assert any("Monto total: $0.00" in call for call in printed)

            assert any("Total facturas emitidas: 4" in call for call in printed)
            assert any("Ingresos totales: $450.00" in call for call in printed)
            assert any("Ingresos recibidos: $300.00" in call for call in printed)
            assert any("Ingresos pendientes: $50.00" in call for call in printed)

            # Locate and verify the generated JSON file
            saved_path_line = next((call for call in printed if "Resumen financiero guardado en:" in call), None)
            assert saved_path_line is not None

            path_start = saved_path_line.find("en:") + 3
            file_path = saved_path_line[path_start:].strip().rstrip("')")

            assert os.path.isfile(file_path)

            with open(file_path, "r", encoding="latin-1") as f:
                resumen = json.load(f)

            assert "timestamp" in resumen
            assert "resumen_general" in resumen
            assert "usuarios" in resumen
            assert len(resumen["usuarios"]) == 3
