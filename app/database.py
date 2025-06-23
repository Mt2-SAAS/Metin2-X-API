from typing import Any, Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session, Query
# Local Imports
from .config import settings

# Crear el engine de la base de datos
account_engine = create_engine(
    settings.DATABASE_URL_ACCOUNT,
    echo=True  # Para desarrollo, muestra las queries SQL
)
player_engine = create_engine(
    settings.DATABASE_URL_PLAYER,
    echo=True  # Para desarrollo, muestra las queries SQL
)

# Crear SessionLocal class
SessionLocalAccount = sessionmaker(autocommit=False, autoflush=False, bind=account_engine)
SessionLocalPlayer = sessionmaker(autocommit=False, autoflush=False, bind=player_engine)


def get_db(name: str = "account") -> Generator[Session]:
    """Dependency para obtener sesión de base de datos"""
    db_account = SessionLocalAccount()
    db_player = SessionLocalPlayer()
    try:
        if name == "account":
            yield db_account
        if name == "player":
            yield db_player
    finally:
        if name == "account":
            db_account.close()
        if name == "player":
            db_player.close()


def get_base_save_model():
    """Obtener la sesión de base de datos para modelos que necesitan guardar datos"""
    Base = declarative_base()
    session_account = SessionLocalAccount()
    session_player = SessionLocalPlayer()

    class BaseSaveAccountModel(Base):
        """Clase base para modelos que necesitan guardar datos en la base de datos"""
        
        __abstract__ = True

        def save(self):
            """Guardar el modelo en la base de datos"""
            session_account.add(self)
            session_account.commit()
            session_account.refresh(self)
            return self

        def delete(self):
            """Eliminar el modelo de la base de datos"""
            session_account.delete(self)
            session_account.commit()

        @classmethod
        def filter(cls, *args, **kwargs):
            """Filtrar modelos por expresiones o atributos"""
            return session_account.query(cls).filter(*args, **kwargs)
        
        @property
        @classmethod
        def query(cls) -> Query:
            """Realizar una consulta a la base de datos
            Y devuelve una instancia de query para el modelo
            """
            return session_account.query(cls)
    
    class BaseSavePlayerModel(Base):
        """Clase base para modelos que necesitan guardar datos en la base de datos"""
        
        __abstract__ = True

        def save(self):
            """Guardar el modelo en la base de datos"""
            session_player.add(self)
            session_player.commit()
            session_player.refresh(self)
            return self

        def delete(self):
            """Eliminar el modelo de la base de datos"""
            session_player.delete(self)
            session_player.commit()

        @classmethod
        def filter(cls, *args, **kwargs):
            """Filtrar modelos por expresiones o atributos"""
            return session_player.query(cls).filter(*args, **kwargs)
        
        @property
        @classmethod
        def query(cls) -> Query:
            """Realizar una consulta a la base de datos
            Y devuelve una instancia de query para el modelo
            """
            return session_player.query(cls)

    return BaseSaveAccountModel, BaseSavePlayerModel

# Crear Base class and get session
BaseSaveAccountModel,\
BaseSavePlayerModel  = get_base_save_model() # Model of the account Session
