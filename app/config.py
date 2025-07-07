from decouple import config


class Settings:
    DATABASE_URL_APP: str = config("DATABASE_URL_APP", default="mysql+pymysql://username:password@HOSTNAME:PORT/application")
    DATABASE_URL_ACCOUNT: str = config("DATABASE_URL_ACCOUNT", default="mysql+pymysql://username:password@HOSTNAME:PORT/srv1_account")
    DATABASE_URL_PLAYER: str = config("DATABASE_URL_PLAYER", default="mysql+pymysql://username:password@HOSTNAME:PORT/srv1_player")
    DATABASE_URL_COMMON: str = config("DATABASE_URL_COMMON", default="mysql+pymysql://username:password@HOSTNAME:PORT/srv1_common")
    SECRET_KEY: str = config("SECRET_KEY", default="your-secret-key")
    ALGORITHM: str = config("ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30, cast=int)
    
    class Config:
        case_sensitive = True

settings = Settings()
