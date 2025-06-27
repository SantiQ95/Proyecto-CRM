# CRM Console App + FastAPI Microservice (Python + MongoDB)

A lightweight, modular CRM system that combines a clean **command-line interface** with a secure **FastAPI-based user creation API**. Easily manage users and invoices through the terminal—or allow external systems to create users via API keys and usage limits.

---

## 🚀 Features

### 🧑‍💼 CRM Console App

- User registration and validation
- Invoice creation with status tracking
- User search by name or email
- Per-user invoice summary reports
- Financial breakdowns by status
- In-memory and mock data generation with Faker
- Test coverage via `pytest`

### 🌐 FastAPI Public API

- Public `/usuarios` endpoint for external user creation
- Simple key-based access control (API keys: `key1`, `key2`, `key3`)
- Rate limiting per key (35 user creations per day)
- Secure `.env`-based credential mapping

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

Install with:

```bash
pip install -r requirements.txt
```

---

## 🧪 Generate Sample Data

Populate your database with sample users and invoices:

```bash
python -m databases.generate_data
```

---

## 🖥️ Run the Console App

Launch the interactive terminal:

```bash
python -m src.main.py
```

---

## 🌐 FastAPI Public API

The backend also includes a public endpoint to create users externally with API key authentication.

### 🔐 Authentication

Use one of the following API keys in your request header:

- `key1`
- `key2`
- `key3`

**Header format:**

```
x-api-key: key1
```

> 🔒 Each key is limited to **35 user creations per day**

---

### 🧾 Endpoint: `/usuarios`

**POST /usuarios**  
Creates a new user in the database.

#### Headers

- `Content-Type: application/json`
- `x-api-key: <your_key>`

#### JSON Body

```json
{
  "nombre": "Lucía",
  "apellidos": "Martínez",
  "email": "lucia@email.com",
  "telefono": "+34...",
  "direccion": "Calle Mayor 5"
}
```

#### Example using `curl`

```bash
curl -X POST http://localhost:8000/usuarios \
  -H "Content-Type: application/json" \
  -H "x-api-key: key1" \
  -d '{"nombre":"Lucía", "apellidos":"Martínez", "email":"lucia@email.com", "telefono":"+34...", "direccion":"Calle Mayor 5"}'
```

#### Sample Response

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

## 💡 Tips

- Keep your `.env` file private—it stores API keys and DB credentials.
- Use the FastAPI microservice to integrate with external apps or services.
- Easily scale with per-key usage limits and public/private API separation.
