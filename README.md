# CRM Console App + FastAPI Microservice (Python + MongoDB)

A lightweight, modular CRM system that combines a rich **command-line interface** with a secure **FastAPI-based user creation API**. Easily manage users and invoices through the terminal—or let authorized external systems create users with API keys and usage limits.

---

## 🚀 Features

### 🧑‍💼 CRM Console App

- Register and validate users
- Generate and track invoices
- Search users by name or email
- Summarize invoices by user or status
- Simulate real-world data using Faker
- Test coverage with `pytest`

### 🌐 FastAPI Microservice

- Public `/usuarios` endpoint for external user creation
- API key access (with per-key usage limits)
- Easy key setup via environment variables
- Daily write limit per key (default: 35 users/day)

---

## 🗂️ Project Structure

```
crm-console/
├── controllers/
│   ├── usuario_controller.py
│   └── factura_controller.py
├── models/
│   ├── usuario.py
│   └── factura.py
├── databases/
│   ├── db.py
│   └── generate_data.py
├── src/
│   └── main.py
├── api.py           ← FastAPI app
├── .env             ← Environment variables (API keys, DB URI)
├── requirements.txt
└── README.md
```

---

## 🔧 Requirements

- Python 3.10 or higher
- MongoDB (local or Atlas)
- Dependencies listed in `requirements.txt`

Install them with:

```bash
pip install -r requirements.txt
```

---

## 🧪 Generate Sample Data

Create 20–30 random users, each with up to 5 random invoices:

```bash
python -m databases.generate_data
```

---

## 🖥️ Run the Console App

Launch the interactive CRM terminal:

```bash
python -m src.main.py
```

---

## 🌐 FastAPI Public API

External tools can create users via a single secure endpoint.

### 🔐 Authentication

Use the `x-api-key` header with one of your authorized keys (`key1`, `key2`, etc.).

Example:

```
x-api-key: key1
```

Each key is limited to **35 users/day**.

---

### 🧾 Endpoint: `/usuarios`

**POST /usuarios**

Creates a new user in the database.

#### Headers:

- `Content-Type: application/json`
- `x-api-key: <your_key>`

#### Body:

```json
{
  "nombre": "Lucía",
  "apellidos": "Martínez",
  "email": "lucia@email.com",
  "telefono": "+34...",
  "direccion": "Calle Mayor 5"
}
```

#### Example using `curl`:

```bash
curl -X POST http://localhost:8000/usuarios \
  -H "Content-Type: application/json" \
  -H "x-api-key: key1" \
  -d '{"nombre":"Lucía", "apellidos":"Martínez", "email":"lucia@email.com", "telefono":"+34...", "direccion":"Calle Mayor 5"}'
```

---

### ✅ Sample Response:

```json
{
  "message": "✅ Usuario Lucía Martínez creado correctamente.",
  "usuarios_creados_hoy_con_esta_clave": 5,
  "limite_diario": 35
}
```

---

## 🧠 Data Models

- **Usuario:**  
  `ID`, `nombre`, `apellidos`, `email`, `telefono`, `direccion`, `fecha_creacion`

- **Factura:**  
  `Número`, `cliente_email`, `descripcion`, `importe`, `estado`, `fecha_emision`

---

## 🧪 Tests

Run unit tests with:

```bash
pytest tests/
```

---
