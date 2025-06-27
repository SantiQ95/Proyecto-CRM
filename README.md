## 🌐 FastAPI Public API (EvolveCRM)

This project includes a FastAPI-based microservice that allows **external user creation** via API, with built-in daily usage limits and simple key-based access control.

---

### 🔐 Authentication

Clients must include a valid API key in every request using the `x-api-key` header. These keys are short, user-friendly identifiers (e.g. `key1`, `key2`) securely mapped to full credentials in your `.env` file.

**Header example:**

```
x-api-key: key1
```

> 🔒 Each API key is limited to **35 user creation requests per day**.

---

### 🧾 Endpoint: Create User

```http
POST /usuarios
```

Creates a new user entry in the database.

#### Required Headers:
- `Content-Type: application/json`
- `x-api-key: <your_key>`

#### Request Body:
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
  -d '{
    "nombre": "Lucía",
    "apellidos": "Martínez",
    "email": "lucia@email.com",
    "telefono": "+34...",
    "direccion": "Calle Mayor 5"
  }'
```

#### Sample Response:
```json
{
  "message": "✅ Usuario Lucía Martínez creado correctamente.",
  "usuarios_creados_hoy_con_esta_clave": 5,
  "limite_diario": 35
}
```
