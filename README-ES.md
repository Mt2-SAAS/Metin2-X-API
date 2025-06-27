# Mi Proyecto FastAPI

[🇺🇸 English](README.md) | 🇪🇸 Español

Una API REST robusta construida con FastAPI y SQLAlchemy que implementa un sistema de gestión de cuentas de usuario, jugadores y gremios con autenticación JWT y una arquitectura sofisticada de triple base de datos.

## 🚀 Características

- **Autenticación JWT**: Sistema de autenticación seguro basado en tokens
- **Arquitectura de Triple Base de Datos**: Separa datos de aplicación principal, cuenta legacy y jugador/gremio legacy en bases de datos independientes
- **API RESTful**: Endpoints bien estructurados siguiendo las mejores prácticas
- **Paginación**: Paginación automática para listados que optimiza el rendimiento
- **Validación de Datos**: Esquemas Pydantic para validación robusta de entrada y salida
- **CORS Configurado**: Listo para integración con aplicaciones frontend
- **Documentación Automática**: Swagger UI y ReDoc incluidos

## 🛠️ Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM de Python con soporte multi-base de datos
- **MySQL**: Base de datos relacional
- **PyMySQL**: Conector MySQL para Python
- **JWT**: Autenticación basada en tokens
- **Pydantic**: Validación y serialización de datos
- **Uvicorn**: Servidor ASGI de alto rendimiento
- **Docker**: Plataforma de contenedorización
- **Docker Compose**: Orquestación multi-contenedor

## 📁 Estructura del Proyecto

```
app/
├── api/
│   ├── deps.py              # Inyección de dependencias
│   └── routes/
│       ├── account.py       # Endpoints de cuentas
│       ├── player.py        # Endpoints de jugadores
│       └── guild.py         # Endpoints de gremios
├── core/
│   ├── hashers.py          # Utilidades de hash de contraseñas
│   └── security.py         # JWT y seguridad
├── crud/
│   └── account.py          # Operaciones CRUD para cuentas
├── models/
│   ├── account.py          # Modelo de cuenta de usuario
│   ├── player.py           # Modelo de jugador
│   └── guild.py            # Modelo de gremio
├── schemas/
│   ├── account.py          # Esquemas Pydantic para cuentas
│   ├── player.py           # Esquemas de jugadores
│   └── guild.py            # Esquemas de gremios
├── config.py               # Configuración de la aplicación
├── database.py             # Configuración de base de datos
└── main.py                 # Punto de entrada de la aplicación
```

## 🚀 Instalación y Configuración

### Requisitos Previos

- Python 3.8+
- Servidor MySQL (para desarrollo local)
- Docker & Docker Compose (para despliegue en contenedores)
- pip (gestor de paquetes de Python)

### Inicio Rápido con Docker (Recomendado)

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd my_fastapi_project
   ```

2. **Crear archivo de entorno**
   ```bash
   cp .env.example .env
   # Editar .env con tu configuración
   ```

3. **Ejecutar con Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Acceder a la aplicación**
   - API: http://localhost:8000
   - Documentación API: http://localhost:8000/docs
   - MySQL: localhost:3307

### Instalación para Desarrollo Local

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd my_fastapi_project
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\\Scripts\\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno** (opcional)
   Crear un archivo `.env` en la raíz del proyecto:
   ```env
   DATABASE_URL_APP=mysql+pymysql://usuario:contraseña@host:puerto/application
   DATABASE_URL_ACCOUNT=mysql+pymysql://usuario:contraseña@host:puerto/srv1_account
   DATABASE_URL_PLAYER=mysql+pymysql://usuario:contraseña@host:puerto/srv1_player
   SECRET_KEY=tu-clave-secreta-muy-segura
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Crear bases de datos**
   ```sql
   CREATE DATABASE application;
   CREATE DATABASE srv1_account;
   CREATE DATABASE srv1_player;
   ```

6. **Ejecutar la aplicación**
   ```bash
   python -m app.main
   # O usar uvicorn directamente
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## 🐳 Configuración Docker

El proyecto incluye una configuración Docker completa con las siguientes características:

### Servicios Docker
- **Servicio Web**: Aplicación FastAPI ejecutándose en Python 3.13
- **Servicio Base de Datos**: MySQL 5.7 con verificaciones de salud
- **Dependencias de Servicios**: El servicio web espera a que la base de datos esté saludable

### Características Docker
- **Verificaciones de Salud**: El servicio MySQL incluye monitoreo automático de salud
- **Persistencia de Volúmenes**: Datos de base de datos persistidos con volúmenes nombrados
- **Configuración de Entorno**: Usa archivo `.env` para configuración
- **Orquestación de Servicios**: Secuencia de inicio adecuada con gestión de dependencias

### Comandos Docker
```bash
# Construir y ejecutar servicios
docker-compose up --build

# Ejecutar en modo separado
docker-compose up -d

# Ver logs
docker-compose logs -f web

# Detener servicios
docker-compose down

# Eliminar volúmenes (precaución: elimina datos)
docker-compose down -v
```

## 📚 Endpoints de la API

### Autenticación

#### Registro de Cuenta
```http
POST /api/account/register
Content-Type: application/json

{
  "login": "usuario123",
  "password": "contraseña_segura",
  "email": "usuario@ejemplo.com",
  "social_id": "1234567"
}
```

#### Inicio de Sesión
```http
POST /api/account/token
Content-Type: application/x-www-form-urlencoded

username=usuario123&password=contraseña_segura
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Gestión de Cuentas

#### Obtener Información Personal
```http
GET /api/account/me
Authorization: Bearer <token>
```

#### Actualizar Información
```http
PUT /api/account/me
Authorization: Bearer <token>
Content-Type: application/json

{
  "social_id": "7654321"
}
```

#### Cambiar Contraseña
```http
PUT /api/account/me/password
Authorization: Bearer <token>
Content-Type: application/json

{
  "old_password": "contraseña_actual",
  "new_password": "contraseña_nueva"
}
```

### Jugadores

#### Listar Jugadores
```http
GET /api/player/players?page=1&per_page=20
```

**Respuesta:**
```json
{
  "players": [
    {
      "account_id": 12345,
      "name": "MataDragones",
      "job": 1,
      "level": 85,
      "exp": 450000
    }
  ],
  "total": 150,
  "page": 1,
  "per_page": 20,
  "total_pages": 8,
  "has_next": true,
  "has_prev": false
}
```

### Gremios

#### Listar Gremios
```http
GET /api/guild/guilds?page=1&per_page=20
```

**Respuesta:**
```json
{
  "guilds": [
    {
      "id": 1,
      "name": "MataDragones",
      "master": 12345,
      "level": 50,
      "exp": 25000
    }
  ],
  "total": 150,
  "page": 1,
  "per_page": 20,
  "total_pages": 8,
  "has_next": true,
  "has_prev": false
}
```

## 🔧 Configuración

### Variables de Entorno

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `DATABASE_URL_APP` | URL de conexión de la base de datos principal | `mysql+pymysql://usuario:contraseña@HOSTNAME_IP:3306/application` |
| `DATABASE_URL_ACCOUNT` | URL de conexión de la base de datos de cuentas legacy | `mysql+pymysql://usuario:contraseña@HOSTNAME_IP:3306/account` |
| `DATABASE_URL_PLAYER` | URL de conexión de la base de datos de jugadores legacy | `mysql+pymysql://usuario:contraseña@HOSTNAME_IP:3306/player` |
| `SECRET_KEY` | Clave secreta JWT | `tu-clave-secreta` |
| `ALGORITHM` | Algoritmo de encriptación JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Tiempo de expiración del token (minutos) | `30` |

### Configuración CORS

La aplicación está configurada para aceptar solicitudes desde:
- `http://localhost:3000`
- `http://localhost:8080`

## 📖 Documentación de la API

Una vez que la aplicación esté ejecutándose, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔍 Endpoints de Salud

- **Verificación de Salud**: `GET /health` - Verificar estado de la aplicación
- **Raíz**: `GET /` - Mensaje de bienvenida

## 🏗️ Arquitectura

### Configuración de Triple Base de Datos

La aplicación usa tres bases de datos MySQL separadas:

1. **application**: Base de datos principal de la aplicación para nuevas características y datos
2. **srv1_account**: Base de datos legacy que almacena información de autenticación y cuentas de usuario
3. **srv1_player**: Base de datos legacy que maneja datos de jugadores y gremios

### Modelos Personalizados

Los modelos heredan de clases base personalizadas que corresponden a su base de datos objetivo:

- **BaseSaveModel**: Para tablas de la base de datos principal de la aplicación
- **BaseSaveAccountModel**: Para tablas de la base de datos de cuentas legacy
- **BaseSavePlayerModel**: Para tablas de la base de datos de jugadores/gremios legacy

Cada clase base incluye métodos convenientes:
- `.save()`: Guardar en la base de datos apropiada
- `.delete()`: Eliminar registro de la base de datos apropiada
- `.filter()`: Filtrar registros en la base de datos apropiada
- `.query()`: Realizar consultas en la base de datos apropiada

### Sistema de Dependencias

Usa el sistema de inyección de dependencias de FastAPI para:
- Gestión de sesiones multi-base de datos (bases de datos de aplicación, cuenta, jugador)
- Autenticación y autorización de usuarios
- Operaciones CRUD específicas de base de datos

## 🚀 Desarrollo

### Ejecutar en Modo Desarrollo
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Estructura de Respuestas

Las respuestas siguen un formato consistente:
- **Éxito**: Datos solicitados con códigos HTTP apropiados
- **Error**: Mensajes descriptivos con códigos de estado HTTP estándar
- **Paginación**: Metadatos completos de paginación incluidos

## 📝 Licencia

Este proyecto está licenciado bajo la Licencia MIT.

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Haz fork del proyecto
2. Crea una rama de característica (`git checkout -b feature/CaracteristicaIncreible`)
3. Confirma tus cambios (`git commit -m 'Agregar alguna CaracteristicaIncreible'`)
4. Empuja a la rama (`git push origin feature/CaracteristicaIncreible`)
5. Abre un Pull Request