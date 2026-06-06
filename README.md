# Sysnet Gov Django Boilerplate

Backendový boilerplate pro Gov.cz projekty postavený na Django 5.x.
Vychází z komponent a tokenů definovaných v [sysnet-gov-ui](../sysnet-gov-ui/).

## Stack
- **Framework:** Django 5.1
- **Database:** PostgreSQL + PostGIS
- **Auth:** JWT / Session (identity app)
- **UI:** Gov.cz Design System (v4)

## Setup
1. `uv venv .venv`
2. `source .venv/bin/activate`
3. `uv pip install -r pyproject.toml`
4. `cp .env.template .env`
5. `python manage.py migrate`

## Architecture
- `apps/identity`: Správa uživatelů a oprávnění
- `apps/audit`: Centrální auditní log
- `apps/common`: Sdílené utility a base modely
