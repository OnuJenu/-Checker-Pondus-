# System Patterns

## Architecture
- FastAPI REST API
- Modular structure with clear separation of concerns
- Repository pattern implementation

## Key Components
1. Routes (app/routes/)
   - Handle HTTP requests
   - Implement business logic
   - Use services for core operations
2. Services (app/services/)
   - Contain business logic
   - Handle data processing
   - Interact with database models
3. Models (app/models/)
   - SQLAlchemy ORM models
   - Define database schema
   - Relationships between entities
4. Database (app/databases/)
   - Database configuration
   - Connection management
   - Migration setup

## Data Flow
1. HTTP Request → Route → Service → Database
2. Database Response → Service → Route → HTTP Response

## Key Patterns
- Dependency Injection (FastAPI)
- Repository Pattern
- RESTful API Design
- Media Upload Handling
- Authentication Middleware
