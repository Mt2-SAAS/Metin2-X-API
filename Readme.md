# My FastAPI Project

A robust REST API built with FastAPI and SQLAlchemy that implements a user account, player, and guild management system with JWT authentication and multi-database architecture.

## 🚀 Features

- **JWT Authentication**: Secure token-based authentication system
- **Multi-Database Architecture**: Separates account and player data into independent databases
- **RESTful API**: Well-structured endpoints following best practices
- **Pagination**: Automatic pagination for listings to optimize performance
- **Data Validation**: Pydantic schemas for robust input and output validation
- **CORS Configured**: Ready for frontend application integration
- **Automatic Documentation**: Swagger UI and ReDoc included

## 🛠️ Technologies

- **FastAPI**: Modern and fast web framework
- **SQLAlchemy**: Python ORM with multi-database support
- **MySQL**: Relational database
- **PyMySQL**: MySQL connector for Python
- **JWT**: Token-based authentication
- **Pydantic**: Data validation and serialization
- **Uvicorn**: High-performance ASGI server

## 📁 Project Structure

```
app/
├── api/
│   ├── deps.py              # Dependency injection
│   └── routes/
│       ├── account.py       # Account endpoints
│       ├── player.py        # Player endpoints
│       └── guild.py         # Guild endpoints
├── core/
│   ├── hashers.py          # Password hashing utilities
│   └── security.py         # JWT and security
├── crud/
│   └── account.py          # CRUD operations for accounts
├── models/
│   ├── account.py          # User account model
│   ├── player.py           # Player model
│   └── guild.py            # Guild model
├── schemas/
│   ├── account.py          # Pydantic schemas for accounts
│   ├── player.py           # Player schemas
│   └── guild.py            # Guild schemas
├── config.py               # Application configuration
├── database.py             # Database configuration
└── main.py                 # Application entry point
```

## 🚀 Installation and Setup

### Prerequisites

- Python 3.8+
- MySQL Server
- pip (Python package manager)

### Installation

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

4. **Configure environment variables** (optional)
   Create a `.env` file in the project root:
   ```env
   DATABASE_URL_ACCOUNT=mysql+pymysql://username:password@host:port/srv1_account
   DATABASE_URL_PLAYER=mysql+pymysql://username:password@host:port/srv1_player
   SECRET_KEY=your-very-secure-secret-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Create databases**
   ```sql
   CREATE DATABASE srv1_account;
   CREATE DATABASE srv1_player;
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
  "social_id": "7654321"
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

### Players

#### List Players
```http
GET /api/player/players?page=1&per_page=20
```

**Response:**
```json
{
  "players": [...],
  "total": 150,
  "page": 1,
  "per_page": 20,
  "total_pages": 8,
  "has_next": true,
  "has_prev": false
}
```

### Guilds

#### List Guilds
```http
GET /api/guild/guilds?page=1&per_page=20
```


**Response:**
```json
{
  "guilds": [...],
  "total": 150,
  "page": 1,
  "per_page": 20,
  "total_pages": 8,
  "has_next": true,
  "has_prev": false
}
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `DATABASE_URL_ACCOUNT` | Account database connection URL | `mysql+pymysql://root:Penagos0320@192.168.17.52:3306/srv1_account` |
| `DATABASE_URL_PLAYER` | Player database connection URL | `mysql+pymysql://root:Penagos0320@192.168.17.52:3306/srv1_player` |
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

### Dual Database Setup

The application uses two separate MySQL databases:

1. **srv1_account**: Stores authentication information and user accounts
2. **srv1_player**: Handles player and guild data

### Custom Models

Models inherit from custom base classes (`BaseSaveAccountModel` and `BaseSavePlayerModel`) that include convenient methods:

- `.save()`: Save to database
- `.delete()`: Delete record
- `.filter()`: Filter records
- `.query()`: Perform queries

### Dependency System

Uses FastAPI's dependency injection system for:
- Database session management
- User authentication
- CRUD operations

## 🚀 Development

### Run in Development Mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Response Structure

Responses follow a consistent format:
- **Success**: Requested data with appropriate HTTP codes
- **Error**: Descriptive messages with standard HTTP status codes
- **Pagination**: Complete pagination metadata included

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request