# Inventory Management API

REST API sederhana untuk manajemen inventory menggunakan Flask dan PostgreSQL.

## Features

* User Management
* Item Management
* Stock In
* Stock Out
* Stock Movement History
* PostgreSQL Database
* Swagger Documentation

## Technology Stack

* Python 3.12+
* Flask
* SQLAlchemy
* PostgreSQL
* Flasgger (Swagger UI)

---

## Installation

Clone repository:

```bash
git clone https://github.com/USERNAME/inventory-system.git

cd inventory-system
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

Buat file `.env`

```env
DATABASE_URL=postgresql://inventory_user:password123@localhost:5432/sistem_inventory
```

---

## Run Application

```bash
python app.py
```

Server akan berjalan pada:

```text
http://127.0.0.1:5000
```

---

## Swagger Documentation

Buka:

```text
http://127.0.0.1:5000/apidocs
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

---

## Author

Agung199
