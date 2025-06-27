# CRM Console App + FastAPI Microservice (Python + MongoDB)

A lightweight, modular CRM system that combines a clean **command-line interface** with a secure **FastAPI-based microservice**. Manage users and invoices locally—or integrate with external tools using API keys, usage limits, and request logging.

---

## 🚀 Features

### 🧑‍💼 CRM Console App

- User registration and validation  
- Invoice creation with status tracking  
- User search by name or email  
- Per-user invoice summary reports  
- Financial breakdowns by status  
- In-memory and mock data generation with Faker  
- Unit test coverage via `pytest`

### 🌐 FastAPI Public API

- `/auth/keys` endpoint for retrieving available key aliases (with optional trace logging)  
- Protected endpoints: `/usuarios`, `/facturas`, `/reportes`  
- Secure `.env`-based API key configuration  
- Rate limiting: 35 user creations per key per day  
- Automatic Swagger docs at startup

---

## 🗂️ Project Structure

```text
crm-console/
├── routes/
│   ├── auth_routes.py       # Public key discovery with usage logging
│   └── param_routes.py      # Protected endpoints (usuarios, facturas, reportes)
├── controllers/
│   ├── usuario_controller.py
│   ├── factura_controller.py
│   └── reportes_controller.py
├── models/
│   ├── usuario.py
│   └── factura.py
├── databases/
│   ├── api.py               # FastAPI launcher
│   ├── db.py
│   └── generate_data.py
├── reportes/
│   └── resumen_*.json       # Auto-exported summaries
├── .env
├── requirements.txt
└── README.md
```

---

## 🔧 Requirements

- Python 3.10 or higher  
- MongoDB (local or Atlas)  
- Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🧪 Generate Sample Data

```bash
python -m databases.generate_data
```

---

## 🖥️ Run the Console App

```bash
python -m src.main.py
```

---

## 🌐 Launch the FastAPI API

```bash
python databases/api.py
```

Swagger UI will auto-launch at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔐 Authentication & API Flow

### 1. Discover Available Keys

```http
GET /auth/keys?nombre=Santiago&app_id=my-app
```

Logs the request in the `log` collection (if query params are included).

### 2. Authorize in Swagger UI

Click the 🔒 “Authorize” button and enter:

```
x-api-key: key1
```

Required for all protected endpoints.

---

## 📤 Example API Usage

### ✅ Create a User

```http
POST /usuarios
Headers:
  Content-Type: application/json
  x-api-key: key1

Body:
{
  "nombre": "Lucía",
  "apellidos": "Martínez",
  "email": "lucia@email.com",
  "telefono": "+34...",
  "direccion": "Calle Mayor 5"
}
```

### 📄 Create an Invoice

```http
POST /facturas
Body:
{
  "cliente_email": "lucia@email.com",
  "descripcion": "Plan mensual",
  "importe": 120.0,
  "estado": "Pendiente"
}
```

### 🔎 Search Users or Invoices

```http
GET /usuarios?nombre=Lucía
GET /facturas?email=lucia@email.com
```

### 📊 Export Financial Summary

```http
GET /reportes?guardar=true
```

Saves a rounded, user-level financial summary to `/reportes/`.

---

## 💾 Sample Report Output

```json
{
  "timestamp": "2025-06-27 13:34:31",
  "resumen_general": {
    "total_usuarios": 48,
    "total_facturas": 103,
    "ingresos_totales": 53887.43,
    "ingresos_pagados": 17333.02,
    "ingresos_pendientes": 17661.09
  },
  "usuarios": [
    {
      "nombre": "Florinda Guijarro",
      "email": "florinda@email.com",
      "total_facturas": 1,
      "monto_total": 825.81,
      "monto_pagado": 0.0,
      "monto_pendiente": 0.0
    }
  ]
}
```

---

## 🧠 Data Models

**Usuario**  
- nombre  
- apellidos  
- email  
- telefono  
- direccion  
- fecha_creacion

**Factura**  
- numero  
- email_cliente  
- descripcion  
- importe  
- estado  
- fecha_emision

---

## ✅ Run Tests

```bash
pytest tests/
```

---

## ✍️ Author

**Santiago Quintanilla**  
GitHub: [https://github.com/SantiQ95](https://github.com/SantiQ95)
