"""Database setup and session management using SQLAlchemy."""
from typing import Generator
from sqlalchemy import create_engine, Column, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session, Query
from sqlalchemy.sql import func
# Local Imports
from .config import settings


# Crear el engine de la base de datos
engine = create_engine(
    settings.DATABASE_URL_APP,
    echo=True  # Para desarrollo, muestra las queries SQL
)

# Crear el engine de la base de datos
account_engine = create_engine(
    settings.DATABASE_URL_ACCOUNT,
    echo=True  # Para desarrollo, muestra las queries SQL
)
player_engine = create_engine(
    settings.DATABASE_URL_PLAYER,
    echo=True  # Para desarrollo, muestra las queries SQL
)
common_engine = create_engine(
    settings.DATABASE_URL_COMMON,
    echo=True  # Para desarrollo, muestra las queries SQL
)

# Crear SessionApp class para cada base de datos
# Base de datos de la aplicación
SessionApp = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base de datos legacy
SessionLocalAccount = sessionmaker(autocommit=False, autoflush=False, bind=account_engine)
SessionLocalPlayer = sessionmaker(autocommit=False, autoflush=False, bind=player_engine)
SessionLocalCommon = sessionmaker(autocommit=False, autoflush=False, bind=common_engine)


def get_db() -> Generator[Session]:
    """Dependency para obtener sesión de base de datos account"""
    db_account = SessionApp()
    try:
        yield db_account
    finally:
        db_account.close()


def get_acount_db() -> Generator[Session]:
    """Dependency para obtener sesión de base de datos account"""
    db_account = SessionLocalAccount()
    try:
        yield db_account
    finally:
        db_account.close()


def get_player_db() -> Generator[Session]:
    """Dependency para obtener sesión de base de datos player"""
    db_player = SessionLocalPlayer()
    try:
        yield db_player
    finally:
        db_player.close()


def get_common_db() -> Generator[Session]:
    """Dependency para obtener sesión de base de datos account"""
    db_account = SessionLocalCommon()
    try:
        yield db_account
    finally:
        db_account.close()


class TimestampMixin:
    """Mixin para campos de timestamp automáticos"""
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


def get_base_save_model():
    """Obtener la sesión de base de datos para modelos que necesitan guardar datos"""
    base = declarative_base()
    base_account = declarative_base()
    base_player = declarative_base()
    base_common = declarative_base()

    session = SessionApp()
    session_account = SessionLocalAccount()
    session_player = SessionLocalPlayer()
    session_common = SessionLocalCommon()

    class BaseModel(base, TimestampMixin):
        """Clase base para modelos que necesitan guardar datos en la base de datos"""

        __abstract__ = True

        def save(self):
            """Guardar el modelo en la base de datos"""
            session.add(self)
            session.commit()
            session.refresh(self)
            return self

        def delete(self):
            """Eliminar el modelo de la base de datos"""
            session.delete(self)
            session.commit()

        @classmethod
        def filter(cls, *args, **kwargs):
            """Filtrar modelos por expresiones o atributos"""
            return session.query(cls).filter(*args, **kwargs)

        @classmethod
        def query(cls) -> Query:
            """Realizar una consulta a la base de datos
            Y devuelve una instancia de query para el modelo
            """
            return session.query(cls)

    class BaseAccountModel(base_account):
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

        @classmethod
        def query(cls, refresh=False) -> Query:
            """Realizar una consulta a la base de datos
            Y devuelve una instancia de query para el modelo
            Este metodo permite refrescar la sesión si es necesario
            Esto es porque algunos datos son creados por fuera de la sesión y no estan en el cache
            """
            if refresh:
                session_player.expire_all()
            return session_account.query(cls)

    class BasePlayerModel(base_player):
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

        @classmethod
        def query(cls, refresh=False) -> Query:
            """Realizar una consulta a la base de datos
            Y devuelve una instancia de query para el modelo
            Este metodo permite refrescar la sesión si es necesario
            Esto es porque algunos datos son creados por fuera de la sesión y no estan en el cache
            """
            if refresh:
                session_player.expire_all()
            return session_player.query(cls)

    class BaseCommonModel(base_common):
        """Clase base para modelos que necesitan guardar datos en la base de datos"""

        __abstract__ = True

        def save(self):
            """Guardar el modelo en la base de datos"""
            session_common.add(self)
            session_common.commit()
            session_common.refresh(self)
            return self

        def delete(self):
            """Eliminar el modelo de la base de datos"""
            session_common.delete(self)
            session_common.commit()

        @classmethod
        def filter(cls, *args, **kwargs):
            """Filtrar modelos por expresiones o atributos"""
            return session_common.query(cls).filter(*args, **kwargs)

        @classmethod
        def query(cls, refresh=False) -> Query:
            """Realizar una consulta a la base de datos
            Y devuelve una instancia de query para el modelo
            Este metodo permite refrescar la sesión si es necesario
            Esto es porque algunos datos son creados por fuera de la sesión y no estan en el cache
            """
            if refresh:
                session_player.expire_all()
            return session_common.query(cls)

    return (
        BaseModel,
        BaseAccountModel,
        BasePlayerModel,
        BaseCommonModel
    )


# Crear Base class and get session
BaseSaveModel,\
BaseSaveAccountModel,\
BaseSavePlayerModel, \
BaseSaveCommonModel = get_base_save_model() # Model of the account Session
