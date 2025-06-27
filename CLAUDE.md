# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A FastAPI-based REST API implementing a sophisticated triple-database architecture for managing user accounts, players, and guilds. The system separates modern application data from legacy account and player systems while maintaining seamless integration through custom base models.

## Development Commands

### Running the Application

**Local Development:**
```bash
# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server
python -m app.main
# OR
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Docker Development:**
```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f web
```

### Database Management
- The application uses a **triple MySQL database** architecture:
  - `application` (main app database) - connected via `DATABASE_URL_APP`
  - `srv1_account` (legacy account database) - connected via `DATABASE_URL_ACCOUNT`
  - `srv1_player` (legacy player/guild database) - connected via `DATABASE_URL_PLAYER`
- Database connections are configured in `app/config.py` with environment variable support
- Uses SQLAlchemy with custom base models for each database
- All tables are created automatically on application startup via `metadata.create_all()`
- Echo mode enabled for development (shows SQL queries in logs)

## Architecture Overview

### Triple-Database Setup
The application implements a sophisticated three-database architecture:
- **Application Database** (`DATABASE_URL_APP`): Main application database with `BaseSaveModel`
- **Account Database** (`DATABASE_URL_ACCOUNT`): Legacy account system with `BaseSaveAccountModel`  
- **Player Database** (`DATABASE_URL_PLAYER`): Legacy player and guild data with `BaseSavePlayerModel`

### Core Components

**Database Layer (`app/database.py`)**:
- Three separate SQLAlchemy engines: `engine`, `account_engine`, `player_engine`
- Three session makers: `SessionApp`, `SessionLocalAccount`, `SessionLocalPlayer`
- Three custom base models with built-in CRUD methods:
  - `BaseSaveModel` - for main app tables
  - `BaseSaveAccountModel` - for account tables
  - `BaseSavePlayerModel` - for player/guild tables
- Dependency injection functions for each database session

**Models Architecture**:
- `Account` model extends `BaseSaveAccountModel` with authentication fields and status validation
- `Player` model extends `BaseSavePlayerModel` with game character data (account_id, name, job, level, exp)
- `Guild` model extends `BaseSavePlayerModel` with guild management data (name, master, level, exp, skills, war stats)
- All models inherit database-specific `.save()`, `.delete()`, `.filter()`, and `.query()` methods

**Authentication System**:
- JWT-based authentication using `python-jose`
- Login-based authentication (not email-based)
- Bearer token security with configurable expiration
- Password hashing using custom hashers in `app/core/hashers.py`

**API Structure**:
- Modular router system with separate route files for accounts, players, and guilds
- Dependency injection for database sessions and authentication
- Consistent error handling with HTTP status codes
- Pagination support for list endpoints

### Key Patterns

**Multi-Database CRUD Pattern**: Each model uses the appropriate database session based on its inheritance:
- `BaseSaveModel` → `SessionApp` (main application database)
- `BaseSaveAccountModel` → `SessionLocalAccount` (legacy account database)
- `BaseSavePlayerModel` → `SessionLocalPlayer` (legacy player database)

**Dependency Injection**: Uses FastAPI's dependency system extensively:
- `crud_account_dependency`: Injects CRUD operations for accounts
- `current_account_dependency`: Injects authenticated user
- `database_account_dependency`: Account database session
- `database_player_dependency`: Player database session

**Configuration Management**: Uses `python-decouple` for environment-based configuration with sensible defaults.

## Database Connection Details

The application connects to three MySQL databases:
- Main App DB: `mysql+pymysql://user:pass@host:port/application`
- Account DB: `mysql+pymysql://user:pass@host:port/srv1_account`
- Player DB: `mysql+pymysql://user:pass@host:port/srv1_player`

Configure via environment variables:
- `DATABASE_URL_APP`
- `DATABASE_URL_ACCOUNT`
- `DATABASE_URL_PLAYER`
- `SECRET_KEY`
- `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`

## API Endpoints

**Account Management** (`/api/account/`):
- `POST /register` - Create new account
- `POST /token` - Login and get JWT token
- `GET /me` - Get current account info
- `PUT /me` - Update account details
- `PUT /me/password` - Change password

**Player Management** (`/api/player/`):
- `GET /players` - List players with pagination (ordered by level desc)

**Guild Management** (`/api/guild/`):
- `GET /guilds` - List guilds with pagination (ordered by level desc)

## Model Schema Overview

**Account Model** (BaseSaveAccountModel):
- `id`, `login`, `password`, `social_id`, `email`, `status`
- Status validation with choices: "OK", "BANNED"

**Player Model** (BaseSavePlayerModel):
- `account_id` (PK), `name`, `job`, `level`, `exp`

**Guild Model** (BaseSavePlayerModel):
- `id` (PK), `name`, `sp`, `master`, `level`, `exp`
- `skill_point`, `skill`, `win`, `draw`, `loss`
- `ladder_point`, `gold`

## Docker Configuration

The application includes a complete Docker setup with health checks and proper service orchestration:

**Docker Files:**
- `compose/api/Dockerfile`: Python 3.13 slim container with FastAPI application
- `docker-compose.yml`: Multi-service setup with web app and MySQL database
- `compose/api/entrypoint.sh`: Service startup script with database wait logic
- `compose/api/init.sql`: Database initialization script for triple-database setup
- `.dockerignore`: Optimizes build context by excluding unnecessary files

**Docker Features:**
- **Health Checks**: MySQL service includes health check using `mysqladmin ping`
- **Service Dependencies**: Web service waits for database to be healthy before starting
- **Environment Configuration**: Uses `.env` file for environment variables
- **Volume Persistence**: MySQL data persisted with named volume `mysql_data`
- **Port Mapping**: Web app on `localhost:8000`, MySQL on `localhost:3307`
- **Service Orchestration**: Proper startup sequence with dependency management

**Database Setup in Docker:**
- Creates database: `application` (other databases are external legacy systems)
- MySQL 5.7 with configurable authentication
- Automatic table creation on application startup
- Health check ensures database is ready before web service starts

**Docker Commands:**
```bash
# Build and run with compose
docker-compose up --build

# Run detached
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop services
docker-compose down

# Remove volumes (caution: deletes data)
docker-compose down -v
```

## Development Notes

- The application creates all tables automatically on startup via `BaseSaveModel.metadata.create_all(bind=engine)`
- Echo is enabled on all database engines for development (shows SQL queries)
- CORS is configured for `localhost:3000` and `localhost:8080`
- Pagination is implemented with `page`, `per_page`, `total_pages`, `has_next`, `has_prev` metadata
- Docker setup includes proper service orchestration with health checks
- Environment variables can be configured via `.env` file for Docker deployment

## File Structure and Key Components

### Core Application Files
- `app/main.py`: FastAPI application entry point with router registration
- `app/config.py`: Configuration management using python-decouple
- `app/database.py`: Multi-database setup with three engines and session makers

### API Layer
- `app/api/deps.py`: Dependency injection for database sessions and authentication
- `app/api/routes/account.py`: Account management endpoints (registration, login, profile)
- `app/api/routes/player.py`: Player listing and management endpoints
- `app/api/routes/guild.py`: Guild listing and management endpoints

### Data Layer
- `app/models/`: SQLAlchemy models extending database-specific base classes
- `app/schemas/`: Pydantic schemas for request/response validation
- `app/crud/`: CRUD operations abstraction layer

### Security Layer
- `app/core/security.py`: JWT token creation and validation
- `app/core/hashers.py`: Password hashing utilities

### Docker Infrastructure
- `compose/api/Dockerfile`: Multi-stage build for optimized Python container
- `compose/api/entrypoint.sh`: Container startup script with database connectivity checks
- `compose/api/init.sql`: Database initialization for Docker deployment
- `docker-compose.yml`: Service orchestration with health checks

## Best Practices for Development

### When Working with Models
- Always use the appropriate base class for each database
- Use `BaseSaveModel` for new application features
- Use `BaseSaveAccountModel` for account-related operations
- Use `BaseSavePlayerModel` for player and guild operations

### When Adding New Endpoints
- Follow the existing router pattern in `app/api/routes/`
- Use appropriate dependency injection from `app/api/deps.py`
- Implement corresponding Pydantic schemas in `app/schemas/`
- Add CRUD operations in `app/crud/` if needed

### Database Migrations
- Currently using `metadata.create_all()` for table creation
- For production, consider implementing proper migration system
- Test all database operations across all three databases

### Testing
- Set up test databases separate from development/production
- Test multi-database transactions carefully
- Verify JWT authentication flows
- Test pagination functionality

## Troubleshooting

### Common Issues
- **Database Connection Issues**: Check environment variables and database availability
- **Authentication Failures**: Verify JWT secret key and token expiration settings
- **Docker Issues**: Ensure MySQL service is healthy before web service starts
- **CORS Issues**: Verify allowed origins in FastAPI CORS middleware

### Debug Commands
```bash
# Check database connectivity
docker-compose exec web python -c "from app.database import engine; print(engine.execute('SELECT 1').scalar())"

# View application logs
docker-compose logs -f web

# Access MySQL shell
docker-compose exec db mysql -u root -p application
```