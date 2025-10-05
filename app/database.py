"""Database setup and session management using SQLAlchemy."""
from typing import Generator
import logging
from sqlalchemy import create_engine, Column, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session, Query
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
# Local Imports
from .config import settings

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
    """Obtener clases base mejoradas con manejo de errores y sesiones por operación"""
    base = declarative_base()
    base_account = declarative_base()
    base_player = declarative_base()
    base_common = declarative_base()

    class BaseModel(base, TimestampMixin):
        """Clase base mejorada para modelos con manejo de errores y sesiones por operación"""

        __abstract__ = True

        def save(self):
            """Guardar el modelo en la base de datos con manejo de errores"""
            session = SessionApp()
            try:
                session.add(self)
                session.commit()
                session.refresh(self)
                logger.info(f"Modelo {self.__class__.__name__} guardado exitosamente")
                return self
            except IntegrityError as e:
                session.rollback()
                logger.error(f"Error de integridad al guardar {self.__class__.__name__}: {str(e)}")
                raise ValueError(f"Error de integridad: {str(e)}")
            except OperationalError as e:
                session.rollback()
                logger.error(f"Error operacional al guardar {self.__class__.__name__}: {str(e)}")
                raise RuntimeError(f"Error de conexión: {str(e)}")
            except SQLAlchemyError as e:
                session.rollback()
                logger.error(f"Error de base de datos al guardar {self.__class__.__name__}: {str(e)}")
                raise RuntimeError(f"Error de base de datos: {str(e)}")
            except Exception as e:
                session.rollback()
                logger.error(f"Error inesperado al guardar {self.__class__.__name__}: {str(e)}")
                raise RuntimeError(f"Error inesperado: {str(e)}")
            finally:
                session.close()

        def delete(self):
            """Eliminar el modelo de la base de datos con manejo de errores"""
            session = SessionApp()
            try:
                session.delete(self)
                session.commit()
                logger.info(f"Modelo {self.__class__.__name__} eliminado exitosamente")
            except IntegrityError as e:
                session.rollback()
                logger.error(f"Error de integridad al eliminar {self.__class__.__name__}: {str(e)}")
                raise ValueError(f"Error de integridad: {str(e)}")
            except OperationalError as e:
                session.rollback()
                logger.error(f"Error operacional al eliminar {self.__class__.__name__}: {str(e)}")
                raise RuntimeError(f"Error de conexión: {str(e)}")
            except SQLAlchemyError as e:
                session.rollback()
                logger.error(f"Error de base de datos al eliminar {self.__class__.__name__}: {str(e)}")
                raise RuntimeError(f"Error de base de datos: {str(e)}")
            except Exception as e:
                session.rollback()
                logger.error(f"Error inesperado al eliminar {self.__class__.__name__}: {str(e)}")
                raise RuntimeError(f"Error inesperado: {str(e)}")
            finally:
                session.close()

        @classmethod
        def filter(cls, *args, **kwargs):
            """Filtrar modelos por expresiones o atributos usando sesión por operación"""
            session = SessionApp()
            try:
                return session.query(cls).filter(*args, **kwargs)
            finally:
                session.close()

        @classmethod
        def query(cls) -> Query:
            """Realizar una consulta a la base de datos usando sesión por operación"""
            session = SessionApp()
            return session.query(cls)

    class BaseAccountModel(base_account):
        """Clase base mejorada para modelos de account con manejo de errores"""

        __abstract__ = True

        def save(self):
            """Guardar el modelo en la base de datos account con manejo de errores"""
            session = SessionLocalAccount()
            try:
                session.add(self)
                session.commit()
                session.refresh(self)
                logger.info(f"Modelo Account {self.__class__.__name__} guardado exitosamente")
                return self
            except IntegrityError as e:
                session.rollback()
                logger.error(f"Error de integridad al guardar Account {self.__class__.__name__}: {str(e)}")
                raise ValueError(f"Error de integridad: {str(e)}")
            except OperationalError as e:
                session.rollback()
                logger.error(f"Error operacional al guardar Account {self.__class__.__name__}: {str(e)}")
                raise RuntimeError(f"Error de conexión: {str(e)}")
            except SQLAlchemyError as e:
                session.rollback()
                logger.error(f"Error de base de datos al guardar Account {self.__class__.__name__}: {str(e)}")
                raise RuntimeError(f"Error de base de datos: {str(e)}")
            except Exception as e:
                session.rollback()
                logger.error(f"Error inesperado al guardar Account {self.__class__.__name__}: {str(e)}")
                raise RuntimeError(f"Error inesperado: {str(e)}")
            finally:
                session.close()

        def delete(self):
            """Eliminar el modelo de la base de datos account con manejo de errores"""
            session = SessionLocalAccount()
            try:
                session.delete(self)
                session.commit()
                logger.info(f"Modelo Account {self.__class__.__name__} eliminado exitosamente")
            except IntegrityError as e:
                session.rollback()
                logger.error(f"Error de integridad al eliminar Account {self.__class__.__name__}: {str(e)}")
                raise ValueError(f"Error de integridad: {str(e)}")
            except OperationalError as e:
                session.rollback()
                logger.error(f"Error operacional al eliminar Account {self.__class__.__name__}: {str(e)}")
                raise RuntimeError(f"Error de conexión: {str(e)}")
            except SQLAlchemyError as e:
                session.rollback()
                logger.error(f"Error de base de datos al eliminar Account {self.__class__.__name__}: {str(e)}")
                raise RuntimeError(f"Error de base de datos: {str(e)}")
            except Exception as e:
                session.rollback()
                logger.error(f"Error inesperado al eliminar Account {self.__class__.__name__}: {str(e)}")
                raise RuntimeError(f"Error inesperado: {str(e)}")
            finally:
                session.close()

        @classmethod
        def filter(cls, *args, **kwargs):
            """Filtrar modelos por expresiones o atributos usando sesión por operación"""
            session = SessionLocalAccount()
            try:
                return session.query(cls).filter(*args, **kwargs)
            finally:
                session.close()

        @classmethod
        def query(cls, refresh=False) -> Query:
            """Realizar una consulta a la base de datos con opción de refresh"""
            session = SessionLocalAccount()
            if refresh:
                session.expire_all()
            return session.query(cls)

    class BasePlayerModel(base_player):
        """Clase base mejorada para modelos de player con manejo de errores"""

        __abstract__ = True

        def save(self):
            """Guardar el modelo en la base de datos player con manejo de errores"""
            session = SessionLocalPlayer()
            try:
                session.add(self)
                session.commit()
                session.refresh(self)
                logger.info(f"Modelo Player {self.__class__.__name__} guardado exitosamente")
                return self
            except IntegrityError as e:
                session.rollback()
                logger.error(f"Error de integridad al guardar Player {self.__class__.__name__}: {str(e)}")
                raise ValueError(f"Error de integridad: {str(e)}")
            except OperationalError as e:
                session.rollback()
                logger.error(f"Error operacional al guardar Player {self.__class__.__name__}: {str(e)}")
                raise RuntimeError(f"Error de conexión: {str(e)}")
            except SQLAlchemyError as e:
                session.rollback()
                logger.error(f"Error de base de datos al guardar Player {self.__class__.__name__}: {str(e)}")
                raise RuntimeError(f"Error de base de datos: {str(e)}")
            except Exception as e:
                session.rollback()
                logger.error(f"Error inesperado al guardar Player {self.__class__.__name__}: {str(e)}")
                raise RuntimeError(f"Error inesperado: {str(e)}")
            finally:
                session.close()

        def delete(self):
            """Eliminar el modelo de la base de datos player con manejo de errores"""
            session = SessionLocalPlayer()
            try:
                session.delete(self)
                session.commit()
                logger.info(f"Modelo Player {self.__class__.__name__} eliminado exitosamente")
            except IntegrityError as e:
                session.rollback()
                logger.error(f"Error de integridad al eliminar Player {self.__class__.__name__}: {str(e)}")
                raise ValueError(f"Error de integridad: {str(e)}")
            except OperationalError as e:
                session.rollback()
                logger.error(f"Error operacional al eliminar Player {self.__class__.__name__}: {str(e)}")
                raise RuntimeError(f"Error de conexión: {str(e)}")
            except SQLAlchemyError as e:
                session.rollback()
                logger.error(f"Error de base de datos al eliminar Player {self.__class__.__name__}: {str(e)}")
                raise RuntimeError(f"Error de base de datos: {str(e)}")
            except Exception as e:
                session.rollback()
                logger.error(f"Error inesperado al eliminar Player {self.__class__.__name__}: {str(e)}")
                raise RuntimeError(f"Error inesperado: {str(e)}")
            finally:
                session.close()

        @classmethod
        def filter(cls, *args, **kwargs):
            """Filtrar modelos por expresiones o atributos usando sesión por operación"""
            session = SessionLocalPlayer()
            try:
                return session.query(cls).filter(*args, **kwargs)
            finally:
                session.close()

        @classmethod
        def query(cls, refresh=False) -> Query:
            """Realizar una consulta a la base de datos con opción de refresh"""
            session = SessionLocalPlayer()
            if refresh:
                session.expire_all()
            return session.query(cls)

    class BaseCommonModel(base_common):
        """Clase base mejorada para modelos de common con manejo de errores"""

        __abstract__ = True

        def save(self):
            """Guardar el modelo en la base de datos common con manejo de errores"""
            session = SessionLocalCommon()
            try:
                session.add(self)
                session.commit()
                session.refresh(self)
                logger.info(f"Modelo Common {self.__class__.__name__} guardado exitosamente")
                return self
            except IntegrityError as e:
                session.rollback()
                logger.error(f"Error de integridad al guardar Common {self.__class__.__name__}: {str(e)}")
                raise ValueError(f"Error de integridad: {str(e)}")
            except OperationalError as e:
                session.rollback()
                logger.error(f"Error operacional al guardar Common {self.__class__.__name__}: {str(e)}")
                raise RuntimeError(f"Error de conexión: {str(e)}")
            except SQLAlchemyError as e:
                session.rollback()
                logger.error(f"Error de base de datos al guardar Common {self.__class__.__name__}: {str(e)}")
                raise RuntimeError(f"Error de base de datos: {str(e)}")
            except Exception as e:
                session.rollback()
                logger.error(f"Error inesperado al guardar Common {self.__class__.__name__}: {str(e)}")
                raise RuntimeError(f"Error inesperado: {str(e)}")
            finally:
                session.close()

        def delete(self):
            """Eliminar el modelo de la base de datos common con manejo de errores"""
            session = SessionLocalCommon()
            try:
                session.delete(self)
                session.commit()
                logger.info(f"Modelo Common {self.__class__.__name__} eliminado exitosamente")
            except IntegrityError as e:
                session.rollback()
                logger.error(f"Error de integridad al eliminar Common {self.__class__.__name__}: {str(e)}")
                raise ValueError(f"Error de integridad: {str(e)}")
            except OperationalError as e:
                session.rollback()
                logger.error(f"Error operacional al eliminar Common {self.__class__.__name__}: {str(e)}")
                raise RuntimeError(f"Error de conexión: {str(e)}")
            except SQLAlchemyError as e:
                session.rollback()
                logger.error(f"Error de base de datos al eliminar Common {self.__class__.__name__}: {str(e)}")
                raise RuntimeError(f"Error de base de datos: {str(e)}")
            except Exception as e:
                session.rollback()
                logger.error(f"Error inesperado al eliminar Common {self.__class__.__name__}: {str(e)}")
                raise RuntimeError(f"Error inesperado: {str(e)}")
            finally:
                session.close()

        @classmethod
        def filter(cls, *args, **kwargs):
            """Filtrar modelos por expresiones o atributos usando sesión por operación"""
            session = SessionLocalCommon()
            try:
                return session.query(cls).filter(*args, **kwargs)
            finally:
                session.close()

        @classmethod
        def query(cls, refresh=False) -> Query:
            """Realizar una consulta a la base de datos con opción de refresh"""
            session = SessionLocalCommon()
            if refresh:
                session.expire_all()
            return session.query(cls)

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
