# Inventory Management API

REST API sederhana untuk manajemen inventory menggunakan FastApi dan PostgreSQL.

## Features

* User Management
* Item Management
* Stock In
* Stock Out
* Stock Movement History
* PostgreSQL Database
* Swagger Documentation (OpenApi)
* Interactive Api Testing

## Technology Stack

* Python 3.12+
* Flask
* SQLAlchemy
* PostgreSQL
* uvicorn
* pydantic

---

## Installation

Clone repository:

```bash
git clone https://github.com/Agung199/kasir_sederhana.git

cd kasir_sederhana
```

Buat virtual environment:

```bash
python -m venv .venv
```

Aktivasi:

Windows:

```bash
.venv\Scripts\activate
```

Linux/Mac:

```bash
source .venv/bin/activate
```

Install dependency:

```bash
pip install -r requirements.txt
```

---

## Database Setup

Buat database PostgreSQL:

```sql
CREATE DATABASE sistem_inventory;
```
Buat user database:

```sql
CREATE USER inventory_user WITH PASSWORD 'password123';

GRANT ALL PRIVILEGES ON DATABASE sistem_inventory TO inventory_user;
```

Buat file `.env`

```env
DATABASE_URL=postgresql://inventory_user:password123@localhost:5432/sistem_inventory
```

---

## Run Application

Jalankan server:

```bash
uvicorn main:app --reload
```

Server akan berjalan pada:

```text
http://127.0.0.1:8000
```

---

## API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```
ReDoc:

```text
http://127.0.0.1:8000/redoc
```

OpenAPI Schema:

```text
http://127.0.0.1:8000/openapi.json
```

---

## Available Endpoints

### Items

| Method | Endpoint    |
| ------ | ----------- |
| GET    | /items      |
| POST   | /items      |
| GET    | /items/{id} |
| PUT    | /items/{id} |
| DELETE | /items/{id} |

### Stock

| Method | Endpoint   |
| ------ | ---------- |
| POST   | /stock-in  |
| POST   | /stock-out |
| GET    | /movements |

## Project Structure

```text
kasir_sederhana/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── config.py
│
├── app.py (File Sebelum penggunaan tecnologi fastapi menggunakan flask)
│
├── .env
├── 
├── .gitignore
├── requirements.txt
└── README.md
```
---

## Author

Agung199
