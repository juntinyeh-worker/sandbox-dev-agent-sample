# Membership & Inventory Management API

Flask REST API with MySQL, SQLAlchemy ORM, and Alembic migrations.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env  # edit DATABASE_URL
flask db upgrade      # run migrations
flask run
```

## API Endpoints

### Members
- `GET    /api/members/`          — list all members
- `POST   /api/members/`          — create member (email, name, tier)
- `GET    /api/members/<id>`      — get member
- `PUT    /api/members/<id>`      — update member
- `DELETE /api/members/<id>`      — delete member

### Inventory
- `GET    /api/inventory/`        — list items (?category=filter)
- `POST   /api/inventory/`        — create item (sku, name, price, quantity, category)
- `GET    /api/inventory/<id>`    — get item
- `PUT    /api/inventory/<id>`    — update item
- `DELETE /api/inventory/<id>`    — delete item

## DB Migrations

```bash
flask db migrate -m "description"   # generate migration
flask db upgrade                     # apply
flask db downgrade                   # rollback
```
