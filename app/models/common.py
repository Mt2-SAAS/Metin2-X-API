"""Modelo SQLAlchemy para la tabla 'gmlist' en la base de datos."""
from sqlalchemy import Column, Integer, String
# Local Imports
from app.database import BaseSaveCommonModel


class GMList(BaseSaveCommonModel):
    """Modelo para la tabla 'gmlist' que almacena información sobre los Game Masters (GMs)."""
    __tablename__ = 'gmlist'

    __table_args__ = {'info': {'skip_autogenerate': True}}

    mID = Column(Integer, primary_key=True, autoincrement=True)
    mAccount = Column(String(16), nullable=False)  # Corresponde al login de Account
    mName = Column(String(50), nullable=True)
    mContactIP = Column(String(15), nullable=True)
    mServerIP = Column(String(15), nullable=True)
    mAuthority = Column(Integer, default=0)  # Nivel de autoridad
