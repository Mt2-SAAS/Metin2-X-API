"""Configuración de la aplicación utilizando Pydantic y python-decouple."""
from decouple import config
from pathlib import Path

# Configuración de directorios
UPLOAD_DIR = Path("app/static/uploads")
# Crear directorio si no existe
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class Settings:
    """Clase de configuración para la aplicación."""
    DATABASE_URL_APP: str = config(
        "DATABASE_URL_APP", 
        default="mysql+pymysql://root:password@db:3306/application"
    )
    DATABASE_URL_ACCOUNT: str = config(
        "DATABASE_URL_ACCOUNT", 
        default="mysql+pymysql://username:password@HOSTNAME:PORT/srv1_account"
    )
    DATABASE_URL_PLAYER: str = config(
        "DATABASE_URL_PLAYER", 
        default="mysql+pymysql://username:password@HOSTNAME:PORT/srv1_player"
    )
    DATABASE_URL_COMMON: str = config(
        "DATABASE_URL_COMMON", 
        default="mysql+pymysql://username:password@HOSTNAME:PORT/srv1_common"
    )
    SECRET_KEY: str = config("SECRET_KEY", default="your-secret-key")
    ALGORITHM: str = config("ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config(
        "ACCESS_TOKEN_EXPIRE_MINUTES", 
        default=30,
        cast=int
    )

    class Config:
        """Configuración adicional para Pydantic."""
        case_sensitive = True

settings = Settings()
