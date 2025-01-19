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

## Authentication System
### User Model Methods
- create_user: Creates new user with username/email/password or OAuth details
- get_user_by_id: Retrieves user by their unique ID
- get_user_by_oauth: Retrieves user by OAuth provider and ID
- get_user_by_username: Retrieves user by username
- check_password: Verifies password against stored hash

### OAuth Providers
- Google
- Twitter
- Facebook/Instagram

### Authentication Flow
1. User initiates OAuth flow with provider
2. Redirect to provider's authorization page
3. User grants permissions
4. Callback to our API with authorization code
5. Exchange code for access token
6. Get user info from provider
7. Create or authenticate local user

### Token Management
- JWT-based authentication
- Access token (15 minutes expiration)
- Refresh token (7 days expiration)
- Bearer token type

### Password Authentication
- Username/password login
- Password hashing with bcrypt
- User lookup by username
- Password hash verification

### Security Features
- JWT secret key from settings
- Token expiration enforcement
- Secure OAuth redirect URIs
- Scope-limited OAuth permissions
- Unique username/email validation
