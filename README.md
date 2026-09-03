# FarmConnect

FarmConnect is a FastAPI backend prototype for a farming marketplace and advisory application. This description is based on the checked-in route and service code.

## Implemented route groups

* **Accounts:** registration and JWT login.
* **Listings:** create and list marketplace entries; full update/delete CRUD is not implemented.
* **Market prices:** list and sync price records. When the external API is unavailable or unconfigured, the sync route deliberately inserts mock Maharashtra data.
* **Location and weather:** nearby-place/listing and weather endpoints backed by service adapters.
* **Advisory:** disease-image and market-advisory endpoints.

## Limitations

This repository contains no frontend, production deployment configuration, or comprehensive automated test suite. `tests/__init__.py` contains null bytes in the audited revision, so a whole-tree Python compilation check fails until that file is repaired. Its default JWT secret is a development placeholder. External-data results depend on environment configuration, and mock market data must not be described as real-time market demand.

The application uses Python, FastAPI, SQLAlchemy, and a local SQLite default. Run the generated OpenAPI page to inspect the exact current request and response contracts.
