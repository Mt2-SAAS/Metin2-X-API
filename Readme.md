# My FastAPI Project

🇺🇸 English | [🇪🇸 Español](README-ES.md)

A robust REST API built with FastAPI and SQLAlchemy that implements a user account, player, guild, and download management system with JWT authentication, admin authorization, and sophisticated quad-database architecture.

## 🚀 Features

- **JWT Authentication**: Secure token-based authentication system
- **Quad-Database Architecture**: Separates main application, legacy account, legacy player/guild, and administrative data into independent databases
- **Admin Authorization**: Role-based access control with authority levels
- **Download Management**: Complete file/content management system with publish/unpublish functionality
- **RESTful API**: Well-structured endpoints following best practices
- **Custom Base Models**: Database-specific CRUD operations with built-in methods
- **Data Validation**: Pydantic schemas for robust input and output validation
- **CORS Configured**: Ready for frontend application integration
- **Automatic Documentation**: Swagger UI and ReDoc included
- **Docker Support**: Complete containerization with health checks

## 🛠️ Technologies

- **FastAPI**: Modern and fast web framework
- **SQLAlchemy**: Python ORM with multi-database support
- **MySQL**: Relational database
- **PyMySQL**: MySQL connector for Python
- **JWT**: Token-based authentication
- **Pydantic**: Data validation and serialization
- **Uvicorn**: High-performance ASGI server
- **Docker**: Containerization platform
- **Docker Compose**: Multi-container orchestration

## 📁 Project Structure

```
my_fastapi_project/
├── app/
│   ├── api/
│   │   ├── deps.py              # Dependency injection
│   │   └── routes/
│   │       ├── account.py       # Account endpoints
│   │       └── game.py          # Game endpoints (players, guilds)
│   ├── core/
│   │   ├── hashers.py          # Password hashing utilities
│   │   └── security.py         # JWT and security
│   ├── crud/
│   │   ├── account.py          # CRUD operations for accounts
│   │   ├── download.py         # CRUD operations for downloads
│   │   └── common.py           # CRUD operations for admin features
│   ├── models/
│   │   ├── account.py          # User account model
│   │   ├── player.py           # Player and guild models
│   │   ├── application.py      # Download and application models
│   │   └── common.py           # Admin/GM models
│   ├── schemas/
│   │   ├── account.py          # Pydantic schemas for accounts
│   │   ├── player.py           # Player schemas
│   │   ├── download.py         # Download schemas
│   │   └── common.py           # Admin schemas
│   ├── config.py               # Application configuration
│   ├── database.py             # Multi-database configuration
│   └── main.py                 # Application entry point
├── compose/
│   └── api/
│       ├── Dockerfile          # Docker image definition
│       ├── entrypoint.sh       # Container startup script
│       └── init.sql            # Database initialization
├── docker-compose.yml          # Service orchestration
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── .gitignore                  # Git ignore rules
├── .dockerignore              # Docker ignore rules
├── CLAUDE.md                   # Development guidance
├── README.md                   # Project documentation (English)
└── README-ES.md               # Project documentation (Spanish)
```

## 🚀 Installation and Setup

### Prerequisites

- Python 3.8+
- MySQL Server (for local development)
- Docker & Docker Compose (for containerized deployment)
- pip (Python package manager)

### Quick Start with Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd my_fastapi_project
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - MySQL: localhost:3307

### Local Development Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd my_fastapi_project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the project root:
   ```env
   DATABASE_URL_APP=mysql+pymysql://username:password@host:port/application
   DATABASE_URL_ACCOUNT=mysql+pymysql://username:password@host:port/srv1_account
   DATABASE_URL_PLAYER=mysql+pymysql://username:password@host:port/srv1_player
   DATABASE_URL_COMMON=mysql+pymysql://username:password@host:port/common
   SECRET_KEY=your-very-secure-secret-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Create databases**
   ```sql
   CREATE DATABASE application;
   ```

6. **Run the application**
   ```bash
   python -m app.main
   # Or use uvicorn directly
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## 📚 API Endpoints

### Authentication

#### Account Registration
```http
POST /api/account/register
Content-Type: application/json

{
  "login": "user123",
  "password": "secure_password",
  "email": "user@example.com",
  "social_id": "1234567"
}
```

#### Login
```http
POST /api/account/token
Content-Type: application/x-www-form-urlencoded

username=user123&password=secure_password
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Account Management

#### Get Personal Information
```http
GET /api/account/me
Authorization: Bearer <token>
```

#### Update Information
```http
PUT /api/account/me
Authorization: Bearer <token>
Content-Type: application/json

{
  "social_id": "7654321",
  "email": "newemail@example.com"
}
```

#### Change Password
```http
PUT /api/account/me/password
Authorization: Bearer <token>
Content-Type: application/json

{
  "old_password": "current_password",
  "new_password": "new_password"
}
```

### Game Features

#### List Players
```http
GET /api/game/players
```

**Response:**
```json
{
  "players": [
    {
      "account_id": 12345,
      "name": "DragonSlayer",
      "job": 1,
      "level": 85,
      "exp": 450000
    }
  ]
}
```

#### List Guilds
```http
GET /api/game/guilds
```

**Response:**
```json
{
  "guilds": [
    {
      "id": 1,
      "name": "DragonSlayers",
      "master": 12345,
      "level": 50,
      "exp": 25000,
      "win": 15,
      "draw": 3,
      "loss": 2
    }
  ]
}
```

### Download Management

#### List Downloads
```http
GET /api/game/downloads?page=1&per_page=10&category=cliente&published=true
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 10, max: 100)
- `category`: Filter by category (optional)
- `published`: Filter by publication status (optional)

**Response:**
```json
{
  "response": [
    {
      "id": 1,
      "provider": "Google Drive",
      "size": 512.5,
      "link": "https://drive.google.com/file/d/123456789/view",
      "category": "cliente",
      "published": true
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 10,
  "total_pages": 1,
  "has_next": false,
  "has_prev": false
}
```

#### Get Download by ID
```http
GET /api/game/downloads/{download_id}
```

#### Create Download (Admin Only)
```http
POST /api/game/downloads
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "provider": "Google Drive",
  "size": 512.5,
  "link": "https://drive.google.com/file/d/123456789/view",
  "category": "cliente",
  "published": false
}
```

#### Update Download (Admin Only)
```http
PUT /api/game/downloads/{download_id}
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "provider": "Mega",
  "size": 600.0,
  "link": "https://mega.nz/file/abcdef123456789",
  "category": "parches",
  "published": true
}
```

#### Publish Download (Admin Only)
```http
PATCH /api/game/downloads/{download_id}/publish
Authorization: Bearer <admin_token>
```

#### Unpublish Download (Admin Only)
```http
PATCH /api/game/downloads/{download_id}/unpublish
Authorization: Bearer <admin_token>
```

#### Delete Download (Admin Only)
```http
DELETE /api/game/downloads/{download_id}
Authorization: Bearer <admin_token>
```

#### Get Current User's Players
```http
GET /api/account/me/players
Authorization: Bearer <token>
```

**Response:**
```json
{
  "players": [
    {
      "account_id": 12345,
      "name": "PlayerName",
      "job": 1,
      "level": 85,
      "exp": 450000
    }
  ]
}
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `DATABASE_URL_APP` | Main application database connection URL | `mysql+pymysql://username:password@HOSTNAME:PORT/application` |
| `DATABASE_URL_ACCOUNT` | Legacy account database connection URL | `mysql+pymysql://username:password@HOSTNAME:PORT/srv1_account` |
| `DATABASE_URL_PLAYER` | Legacy player database connection URL | `mysql+pymysql://username:password@HOSTNAME:PORT/srv1_player` |
| `DATABASE_URL_COMMON` | Administrative database connection URL | `mysql+pymysql://username:password@HOSTNAME:PORT/common` |
| `SECRET_KEY` | JWT secret key | `your-secret-key` |
| `ALGORITHM` | JWT encryption algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time (minutes) | `30` |

### CORS Configuration

The application is configured to accept requests from:
- `http://localhost:3000`
- `http://localhost:8080`

## 📖 API Documentation

Once the application is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔍 Health Endpoints

- **Health Check**: `GET /health` - Check application status
- **Root**: `GET /` - Welcome message

## 🏗️ Architecture

### Quad Database Setup

The application uses four separate MySQL databases:

1. **application**: Main application database for new features and data (downloads, etc.)
2. **srv1_account**: Legacy database storing authentication information and user accounts
3. **srv1_player**: Legacy database handling player and guild data
4. **common**: Administrative database for GM/admin management and authorization

### Custom Models

Models inherit from custom base classes that correspond to their target database:

- **BaseSaveModel**: For main application database tables (downloads, etc.)
- **BaseSaveAccountModel**: For legacy account database tables  
- **BaseSavePlayerModel**: For legacy player/guild database tables
- **BaseSaveCommonModel**: For administrative database tables (GM/admin management)

Each base class includes convenient methods:
- `.save()`: Save to appropriate database
- `.delete()`: Delete record from appropriate database
- `.filter()`: Filter records in appropriate database
- `.query()`: Perform queries on appropriate database

### Dependency System

Uses FastAPI's dependency injection system for:
- Multi-database session management (application, account, player, common databases)
- User authentication and authorization
- Admin role-based access control
- Database-specific CRUD operations

## 🐳 Docker Configuration

The project includes complete Docker support with:

- **Multi-service setup**: API and MySQL database
- **Health checks**: Database readiness verification  
- **Volume persistence**: Data survives container restarts
- **Environment configuration**: Flexible deployment options

### Docker Services
- **API**: FastAPI application on port 8000
- **Database**: MySQL 5.7 on port 3307

### Docker Commands

```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f api  

# Stop services
docker-compose down

# Remove volumes (caution: deletes data)
docker-compose down -v
```

## 🚀 Development

### Run in Development Mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Development Features

- **Automatic Table Creation**: Tables are created on application startup
- **SQL Query Logging**: Echo mode enabled for debugging
- **Hot Reload**: Automatic restart on code changes (with --reload)

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request