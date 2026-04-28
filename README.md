# Membership & Inventory Management API

A RESTful API built with Flask for managing members and inventory items, backed by MySQL with SQLAlchemy ORM and Alembic migrations.

## Tech Stack

- **Framework:** Flask 3.1.1
- **ORM:** Flask-SQLAlchemy 3.1.1
- **Migrations:** Flask-Migrate 4.1.0 (Alembic)
- **Database:** MySQL (via PyMySQL 1.1.1)
- **Serialization:** Marshmallow 3.23.2
- **Config:** python-dotenv 1.1.0

## Project Structure

```
├── app/
│   ├── __init__.py          # App factory, extensions
│   ├── models/
│   │   ├── member.py        # Member model
│   │   └── inventory.py     # InventoryItem model
│   └── routes/
│       ├── members.py       # /api/members endpoints
│       └── inventory.py     # /api/inventory endpoints
├── migrations/
│   ├── env.py
│   └── versions/            # Migration scripts
├── config.py                # App configuration
├── alembic.ini
├── requirements.txt
└── .env.example
```

## Getting Started

### Prerequisites

- Python 3.10+
- MySQL server

### Installation

```bash
# Clone and install dependencies
git clone https://github.com/juntinyeh-worker/sandbox-dev-agent-sample.git
cd sandbox-dev-agent-sample
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your DATABASE_URL

# Run migrations and start the server
flask db upgrade
flask run
```

## API Endpoints

### Health Check

| Method | Path      | Description          |
|--------|-----------|----------------------|
| GET    | `/health` | Returns server status |

### Members (`/api/members`)

| Method | Path                  | Description    | Required Fields        |
|--------|-----------------------|----------------|------------------------|
| GET    | `/api/members/`       | List all       | —                      |
| POST   | `/api/members/`       | Create member  | `email`, `name`        |
| GET    | `/api/members/<id>`   | Get by ID      | —                      |
| PUT    | `/api/members/<id>`   | Update member  | —                      |
| DELETE | `/api/members/<id>`   | Delete member  | —                      |

**Member fields:** `email` (unique), `name`, `tier` (basic/premium/vip), `active` (boolean)

### Inventory (`/api/inventory`)

| Method | Path                    | Description          | Required Fields            |
|--------|-------------------------|----------------------|----------------------------|
| GET    | `/api/inventory/`       | List items           | —                          |
| GET    | `/api/inventory/?category=X` | Filter by category | —                     |
| POST   | `/api/inventory/`       | Create item          | `sku`, `name`, `price`     |
| GET    | `/api/inventory/<id>`   | Get by ID            | —                          |
| PUT    | `/api/inventory/<id>`   | Update item          | —                          |
| DELETE | `/api/inventory/<id>`   | Delete item          | —                          |

**Inventory fields:** `sku` (unique), `name`, `price`, `quantity`, `category`

## Database Migrations

```bash
flask db migrate -m "description"   # Generate a new migration
flask db upgrade                     # Apply pending migrations
flask db downgrade                   # Rollback last migration
```

## Environment Variables

| Variable       | Description                  | Default                                                        |
|----------------|------------------------------|----------------------------------------------------------------|
| `FLASK_APP`    | Flask application entry      | `app`                                                          |
| `FLASK_ENV`    | Environment mode             | `development`                                                  |
| `DATABASE_URL` | MySQL connection string      | `mysql+pymysql://user:password@localhost:3306/membership_inventory` |
