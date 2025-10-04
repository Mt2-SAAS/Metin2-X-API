"""Modelo de la tabla 'account'."""
from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, Index, Enum
from sqlalchemy.orm import validates
# Local Imports
from app.database import BaseSaveAccountModel

# Status
class StatusType(PyEnum):
    """Enum para los estados de la cuenta."""
    OK = "OK" # Estado activo
    BANNED = "BANNED"


class Account(BaseSaveAccountModel):
    """Modelo de la tabla 'account'."""
    __tablename__ = 'account'

    __table_args__ = (
        Index('login', 'login', unique=True),
        Index('social_id', 'social_id'),
        {'comment': 'Tabla de cuentas de usuarios',
         'info': {'skip_autogenerate': True}},
    )

    id = Column(Integer, primary_key=True, autoincrement=True,
        comment='ID único de la cuenta'
    )
    login = Column(String(16),nullable=False,
        comment='LOGIN_MAX_LEN=30'
    )
    password = Column(String(42), nullable=False,
        comment='PASSWD_MAX_LEN=16; default 45 size'
    )
    social_id = Column(String(7), nullable=False,
        comment='ID de red social asociada'
    )
    email = Column(String(100),nullable=False, 
        comment='Email del usuario'
    )
    status = Column(Enum(StatusType), nullable=False,
        comment='Estado de la cuenta (OK, BANNED)'
    )

    def __repr__(self):
        return f"<Account(id={self.id}, login='{self.login}')>"
