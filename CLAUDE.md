# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Application
```bash
# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server
python -m app.main
# OR
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Database Management
- The application uses dual MySQL databases: `srv1_account` and `srv1_player`
- Database connections are configured in `app/config.py` with environment variable support
- Uses SQLAlchemy with custom base models for each database

## Architecture Overview

### Multi-Database Setup
The application implements a dual-database architecture:
- **Account Database**: Handles user authentication, login credentials, and account management
- **Player Database**: Manages game-related data like player stats, levels, and character information

### Core Components

**Database Layer (`app/database.py`)**:
- Two separate SQLAlchemy engines for account and player databases
- Custom base models `BaseSaveAccountModel` and `BaseSavePlayerModel` with built-in CRUD methods
- Dependency injection functions for database sessions

**Models**:
- `Account` model extends `BaseSaveAccountModel` with authentication fields and status validation
- `Player` model extends `BaseSavePlayerModel` with game character data
- Both models inherit `.save()`, `.delete()`, `.filter()`, and `.query()` methods

**Authentication System**:
- JWT-based authentication using `python-jose`
- Login-based authentication (not email-based)
- Bearer token security with configurable expiration
- Password hashing using custom hashers in `app/core/hashers.py`

**API Structure**:
- Modular router system with separate route files for accounts, players, and guilds
- Dependency injection for database sessions and authentication
- Consistent error handling with HTTP status codes

### Key Patterns

**CRUD Pattern**: Custom CRUD classes (like `CRUDAccount`) handle database operations with built-in authentication and validation.

**Dependency Injection**: Uses FastAPI's dependency system extensively:
- `crud_account_dependency`: Injects CRUD operations
- `current_account_dependency`: Injects authenticated user
- Database session dependencies for each database

**Configuration Management**: Uses `python-decouple` for environment-based configuration with sensible defaults.

## Database Connection Details

The application connects to MySQL databases with the following pattern:
- Account DB: `mysql+pymysql://user:pass@host:port/srv1_account`
- Player DB: `mysql+pymysql://user:pass@host:port/srv1_player`

Configure via environment variables:
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

**Player & Guild endpoints** are available under `/api/player/` and `/api/guild/` respectively.