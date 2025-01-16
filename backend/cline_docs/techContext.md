# Technology Context

## Core Technologies
- Python 3.x
- FastAPI (Web Framework)
- SQLAlchemy (ORM)
- Alembic (Migrations)
- Pydantic (Data Validation)
- Uvicorn (ASGI Server)

## Database
- SQLite (Development)
- SQLAlchemy ORM
- Alembic migrations

## Development Setup
1. Python Virtual Environment
2. Install dependencies: `pip install -r requirements.txt`
3. Database setup:
   - Initialize database: `alembic upgrade head`
   - Create migrations: `alembic revision --autogenerate`
4. Run development server: `uvicorn app.main:app --reload`

## Testing
- pytest framework
- Test files in tests/ directory
- Test coverage reporting

## API Documentation
- Automatic OpenAPI docs at /docs
- API spec in api-docs.yaml
