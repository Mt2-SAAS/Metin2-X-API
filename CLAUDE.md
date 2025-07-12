# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A FastAPI-based REST API implementing a sophisticated quad-database architecture for managing user accounts, players, guilds, and administrative features. The system separates modern application data from legacy account and player systems while adding a common database for administrative features, all maintaining seamless integration through custom base models.

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
docker-compose logs -f api
```

### Database Management
- The application uses a **quad MySQL database** architecture:
  - `application` (main app database) - connected via `DATABASE_URL_APP`
  - `srv1_account` (legacy account database) - connected via `DATABASE_URL_ACCOUNT`
  - `srv1_player` (legacy player/guild database) - connected via `DATABASE_URL_PLAYER`
  - `srv1_common` (administrative database) - connected via `DATABASE_URL_COMMON`
- Database connections are configured in `app/config.py` with environment variable support
- Uses SQLAlchemy with custom base models for each database
- All tables are created automatically on application startup via `metadata.create_all()`
- Echo mode enabled for development (shows SQL queries in logs)

## Architecture Overview

### Quad-Database Setup
The application implements a sophisticated four-database architecture:
- **Application Database** (`DATABASE_URL_APP`): Main application database with `BaseSaveModel` for modern features like download management
- **Account Database** (`DATABASE_URL_ACCOUNT`): Legacy account system with `BaseSaveAccountModel`  
- **Player Database** (`DATABASE_URL_PLAYER`): Legacy player and guild data with `BaseSavePlayerModel`
- **Common Database** (`DATABASE_URL_COMMON`): Administrative database with `BaseSaveCommonModel` for GM/admin management

### Core Components

**Database Layer (`app/database.py`)**:
- Four separate SQLAlchemy engines: `engine`, `account_engine`, `player_engine`, `common_engine`
- Four session makers: `SessionApp`, `SessionLocalAccount`, `SessionLocalPlayer`, `SessionLocalCommon`
- **TimestampMixin**: Provides automatic timestamp fields (`created_at`, `updated_at`) using SQLAlchemy's `func.now()`
- Four custom base models with built-in CRUD methods:
  - `BaseSaveModel` - inherits from `TimestampMixin`, for main app tables (downloads, sites, images, pages)
  - `BaseSaveAccountModel` - for account tables (no timestamps)
  - `BaseSavePlayerModel` - for player/guild tables (no timestamps)
  - `BaseSaveCommonModel` - for admin/GM tables (no timestamps)
- Dependency injection functions for each database session

**Models Architecture**:
- `Account` model extends `BaseSaveAccountModel` with authentication fields and status validation
- `Player` model extends `BaseSavePlayerModel` with game character data (account_id, name, job, level, exp)
- `Guild` model extends `BaseSavePlayerModel` with guild management data (name, master, level, exp, skills, war stats)
- `Download` model extends `BaseSaveModel` with file management and Site relationship (provider, size, link, category, published, site_id)
- `Site` model extends `BaseSaveModel` with website configuration (name, slug, levels, rates, social links, footer settings)
- `Image` model extends `BaseSaveModel` with image management (name, path, type, alt_text, file_size)
- `Pages` model extends `BaseSaveModel` with CMS functionality (slug, title, content, SEO fields)
- `GMList` model extends `BaseSaveCommonModel` with admin authorization (account_id, authority_level)
- All models inherit database-specific `.save()`, `.delete()`, `.filter()`, and `.query()` methods
- **Automatic Timestamps**: Models extending `BaseSaveModel` automatically include `created_at` and `updated_at` fields

**Authentication System**:
- JWT-based authentication using `python-jose`
- Login-based authentication (not email-based)
- Bearer token security with configurable expiration
- Password hashing using custom hashers in `app/core/hashers.py`
- Admin/GM authorization system with authority levels
- Role-based access control for administrative endpoints

**API Structure**:
- Modular router system with separate route files for accounts and game features
- Dependency injection for database sessions and authentication
- Consistent error handling with HTTP status codes
- CORS configured for localhost development

### Key Patterns

**Multi-Database CRUD Pattern**: Each model uses the appropriate database session based on its inheritance:
- `BaseSaveModel` → `SessionApp` (main application database)
- `BaseSaveAccountModel` → `SessionLocalAccount` (legacy account database)
- `BaseSavePlayerModel` → `SessionLocalPlayer` (legacy player database)
- `BaseSaveCommonModel` → `SessionLocalCommon` (administrative database)

**Dependency Injection**: Uses FastAPI's dependency system extensively:
- `get_db()`: Main application database session
- `get_acount_db()`: Account database session
- `get_player_db()`: Player database session
- `get_common_db()`: Common/administrative database session
- `crud_account_dependency`: Account CRUD operations
- `current_account_dependency`: Current authenticated account
- `require_gm_level_implementor`: GM/admin authorization dependency

**Configuration Management**: Uses `python-decouple` for environment-based configuration with sensible defaults.

## Database Connection Details

The application connects to four MySQL databases:
- Main App DB: `mysql+pymysql://user:pass@host:port/application`
- Account DB: `mysql+pymysql://user:pass@host:port/srv1_account`
- Player DB: `mysql+pymysql://user:pass@host:port/srv1_player`
- Common DB: `mysql+pymysql://user:pass@host:port/srv1_common`

Configure via environment variables:
- `DATABASE_URL_APP`
- `DATABASE_URL_ACCOUNT`
- `DATABASE_URL_PLAYER`
- `DATABASE_URL_COMMON`
- `SECRET_KEY`
- `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`

## API Endpoints

**Account Management** (`/api/account/`):
- `POST /register` - Create new account (with login and email validation)
- `POST /token` - Login and get access token (using login as username)
- `GET /me` - Get current account information
- `GET /me/is_admin` - Check if current account is admin/GM
- `PUT /me` - Update current account information (with social_id validation)
- `PUT /me/password` - Update account password with old password verification
- `GET /me/players` - Get all players for logged-in account

**Game Features** (`/api/game/`):
- `GET /players` - List all players with pagination (ordered by level)
- `GET /guilds` - List all guilds with pagination (ordered by level)
- Download management system with full CRUD operations and admin protection
- All admin-only endpoints require GM/admin authorization

## New Features

### Download Management System
A comprehensive file/content management system with the following capabilities:

**Public Endpoints:**
- `GET /api/game/downloads` - List downloads with pagination, search, and filtering
  - Query parameters: `page`, `per_page`, `category`, `provider`, `site_id`, `published_only`, `search`
  - Advanced search across provider, category, and link fields
  - Category, provider, and site-based filtering
  - Combined site+category filtering support
  - Published-only filtering option
  - Eager loading of Site relationship data

**Admin-Only Endpoints** (require GM/admin authorization):
- `GET /api/game/downloads/{id}` - Get specific download details
- `POST /api/game/downloads` - Create new download
- `PUT /api/game/downloads/{id}` - Update download
- `PATCH /api/game/downloads/{id}/publish` - Publish download
- `PATCH /api/game/downloads/{id}/unpublish` - Unpublish download
- `DELETE /api/game/downloads/{id}` - Delete download

**Features:**
- Full CRUD operations with validation
- Site relationship management with foreign key validation
- Publish/unpublish functionality  
- Advanced search across provider, category, and link fields
- Multiple filtering options (category, provider, site, published status)
- Combined filtering (site + category)
- Pagination with metadata (total, pages, navigation)
- Admin-only management endpoints with GM authorization
- Automatic timestamp tracking via BaseSaveModel (`created_at`, `updated_at`)
- Eager loading of Site data in all download responses

### Admin/GM Authorization System
Role-based access control system for administrative features:

**Features:**
- Authority level-based permissions
- Admin verification through `GMList` model
- Protected endpoints using `require_gm_level_implementor` dependency
- Integration with JWT authentication
- Centralized admin management via common database

**Usage:**
```python
from app.core.deps import require_gm_level_implementor
# Protect endpoints with GM authorization
@router.post("/admin-endpoint")
async def admin_only_endpoint(
    admin_account: require_gm_level_implementor
):
    # Admin-only logic here
    pass
```

### Enhanced Account System
Extended account management with comprehensive user operations:

**New Features:**
- Complete account registration with login and email validation
- Secure password update with old password verification
- Social ID validation (7-digit numeric format)
- Account status management (OK/BANNED)
- Admin verification endpoint
- Player-to-account relationship mapping

**Security Features:**
- JWT-based authentication with login as identifier
- Password hashing with custom hashers
- Role-based access control integration
- Account uniqueness validation (login and email)

## Model Schema Overview

**Account Model** (BaseSaveAccountModel):
- `id`, `login`, `password`, `social_id`, `email`, `status`
- Status validation with choices: "OK", "BANNED"
- Indexed on login (unique) and social_id

**Player Model** (BaseSavePlayerModel):
- `account_id` (PK), `name`, `job`, `level`, `exp`

**Guild Model** (BaseSavePlayerModel):
- `id` (PK), `name`, `sp`, `master`, `level`, `exp`
- `skill_point`, `skill`, `win`, `draw`, `loss`
- `ladder_point`, `gold`

**Download Model** (BaseSaveModel + TimestampMixin):
- `id` (PK), `provider`, `size` (STRING), `link` (TEXT), `category`
- `published` (BOOLEAN) - publication status for content management
- `site_id` (FK) - relationship to Site model with cascade delete
- `created_at`, `updated_at` (auto-managed timestamps)
- Relationship: `site` (many-to-one with Site)
- Full content management with publish/unpublish functionality
- Advanced search, filtering, and site-based organization

**Site Model** (BaseSaveModel + TimestampMixin):
- `id` (PK), `name`, `slug` (unique), `initial_level`, `max_level`
- `rates`, `facebook_url`, `facebook_enable`, `forum_url`
- `footer_info`, `footer_menu_enable`, `footer_info_enable`
- `last_online`, `is_active`, `maintenance_mode`
- `created_at`, `updated_at` (auto-managed timestamps)
- Relationships: `downloads` (one-to-many), `images` (many-to-many), `footer_menu` (many-to-many with Pages)

**Image Model** (BaseSaveModel + TimestampMixin):
- `id` (PK), `name`, `image_path`, `image_type` (ENUM: logo/bg)
- `alt_text`, `file_size`, `is_active`
- `created_at`, `updated_at` (auto-managed timestamps)
- Relationship: `sites` (many-to-many)

**Pages Model** (BaseSaveModel + TimestampMixin):
- `id` (PK), `slug`, `title`, `content`, `published`
- `meta_description`, `meta_keywords` (SEO fields)
- `created_at`, `updated_at` (auto-managed timestamps)
- Relationship: `sites_footer` (many-to-many with Site)

**GMList Model** (BaseSaveCommonModel):
- `account_id` (PK), `authority_level`
- Admin authorization and role-based access control

## Docker Configuration

The application includes a complete Docker setup with health checks and proper service orchestration:

**Docker Files:**
- `compose/api/Dockerfile`: Python 3.13 slim container with FastAPI application
- `docker-compose.yml`: Multi-service setup with api and MySQL database
- `compose/api/entrypoint.sh`: Service startup script with database wait logic
- `compose/api/init.sql`: Database initialization script for triple-database setup

**Docker Features:**
- **Health Checks**: MySQL service includes health check using `mysqladmin ping`
- **Service Dependencies**: API service waits for database to be healthy before starting
- **Environment Configuration**: Uses `.env` file for environment variables
- **Volume Persistence**: MySQL data persisted with named volume `mysql_data`
- **Port Mapping**: API on `localhost:8000`, MySQL on `localhost:3307`
- **Service Orchestration**: Proper startup sequence with dependency management

**Database Setup in Docker:**
- Creates database: `application` (other databases are external legacy systems)
- MySQL 5.7 with configurable authentication
- Automatic table creation on application startup for application databases
- Health check ensures database is ready before API service starts

**Docker Commands:**
```bash
# Build and run with compose
docker-compose up --build

# Run detached
docker-compose up -d

# View logs  
docker-compose logs -f api

# Stop services
docker-compose down

# Remove volumes (caution: deletes data)
docker-compose down -v
```

## Development Notes

- The application creates all tables automatically on startup via `BaseSaveModel.metadata.create_all(bind=engine)`
- Echo is enabled on all database engines for development (shows SQL queries)
- CORS is configured for `localhost:3000` and `localhost:8080`
- Docker setup includes proper service orchestration with health checks
- Environment variables can be configured via `.env` file for Docker deployment

## Current Development Status

**Recently Implemented:**
- Complete account management system with registration, login, and profile management
- Admin verification system with GM-level access control
- **Refactored Download API** with Site relationship integration:
  - Site-based filtering and organization
  - Combined site+category filtering
  - Site existence validation in CRUD operations
  - Eager loading of Site relationship data
  - Updated schemas to include site_id and site information
- **TimestampMixin Integration**: Automatic `created_at`/`updated_at` tracking for all BaseSaveModel entities
- **Multi-Model CMS System**: Site, Image, and Pages models with many-to-many relationships
- Advanced search and filtering capabilities for downloads
- Player listing with pagination and level-based ordering
- Guild management with comprehensive data display
- Role-based access control for administrative endpoints

**Active Features:**
- Multi-database architecture (4 databases: app, account, player, common)
- JWT-based authentication with login as identifier
- Custom base models with built-in CRUD methods
- Comprehensive API documentation with proper schemas
- Admin-only endpoints for content management
- Pagination with metadata for all list endpoints

## File Structure and Key Components

### Core Application Files
- `app/main.py`: FastAPI application entry point with router registration
- `app/config.py`: Configuration management using python-decouple
- `app/database.py`: Multi-database setup with three engines and session makers

### API Layer
- `app/api/deps.py`: Dependency injection for database sessions and authentication
- `app/api/routes/account.py`: Account management endpoints
- `app/api/routes/game.py`: Game-related endpoints (players, guilds)

### Data Layer
- `app/models/`: SQLAlchemy models extending database-specific base classes
  - `account.py`: Account model for authentication
  - `player.py`: Player and Guild models for game data
  - `application.py`: Download, Site, Image, and Pages models with relationships and TimestampMixin
  - `common.py`: GMList model for admin authorization
- `app/schemas/`: Pydantic schemas for request/response validation
  - `site.py`: Complete Site CRUD schemas
  - `download.py`: Updated Download schemas with site relationship
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
- Use `BaseSaveModel` for new application features (downloads, sites, images, pages) - includes automatic timestamps
- Use `BaseSaveAccountModel` for account-related operations
- Use `BaseSavePlayerModel` for player and guild operations  
- Use `BaseSaveCommonModel` for administrative features
- **TimestampMixin Behavior**: Models extending `BaseSaveModel` automatically get `created_at` (set on creation) and `updated_at` (updated on every save)
- **Relationship Management**: When working with foreign keys, ensure parent entities exist before creating relationships

### When Adding New Endpoints
- Follow the existing router pattern in `app/api/routes/`
- Use appropriate dependency injection from `app/api/deps.py`
- Implement corresponding Pydantic schemas in `app/schemas/`
- Add CRUD operations in `app/crud/` if needed

### Database Migrations
- Currently using `metadata.create_all()` for table creation
- For production, consider implementing proper migration system
- Test all database operations across all four databases

### Testing
- Set up test databases separate from development/production
- Test multi-database transactions carefully
- Verify JWT authentication flows

## Troubleshooting

### Common Issues
- **Database Connection Issues**: Check environment variables and database availability
- **Authentication Failures**: Verify JWT secret key and token expiration settings
- **Docker Issues**: Ensure MySQL service is healthy before API service starts
- **CORS Issues**: Verify allowed origins in FastAPI CORS middleware

### Debug Commands
```bash
# Check database connectivity
docker-compose exec api python -c "from app.database import engine; print(engine.execute('SELECT 1').scalar())"

# View application logs
docker-compose logs -f api

# Access MySQL shell
docker-compose exec db mysql -u root -p application
```