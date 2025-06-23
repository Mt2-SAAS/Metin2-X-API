from sqlalchemy import Column, Integer, String, Index
from sqlalchemy.orm import validates
# Local Imports
from app.database import BaseSaveAccountModel

# Status
ACCEPT = "OK"
BANNED = "BANNED"


class Account(BaseSaveAccountModel):
    __tablename__ = 'account'
    
    __table_args__ = (
        Index('login', 'login', unique=True),
        Index('social_id', 'social_id'),
        {'comment': 'Tabla de cuentas de usuarios'}
    )

    # Definir las opciones de estado
    STATUS_ACCOUNT_CHOICES = [
        (ACCEPT, "Available"),
        (BANNED, "Banned"),
    ]
    
    id = Column(
        Integer,  # equivalente a INTEGER(11) en MySQL
        primary_key=True,
        autoincrement=True,
        comment='ID único de la cuenta'
    )
    login = Column(
        String(16),
        nullable=False,
        comment='LOGIN_MAX_LEN=30'
    )
    password = Column(
        String(42),
        nullable=False,
        comment='PASSWD_MAX_LEN=16; default 45 size'
    )
    social_id = Column(
        String(7),
        nullable=False,
        comment='ID de red social asociada'
    )
    email = Column(
        String(100),
        nullable=False,
        comment='Email del usuario'
    )
    status = Column(
        String(8), 
        default="OK",
        nullable=False
    )

    @validates('status')
    def validate_status(self, key, value):
        """Validar que el status sea uno de los valores permitidos"""
        valid_statuses = [choice[0] for choice in self.STATUS_ACCOUNT_CHOICES]
        if value not in valid_statuses:
            raise ValueError(f"Status must be one of: {valid_statuses}")
        return value
    
    def __repr__(self):
        return f"<Account(id={self.id}, login='{self.login}')>"
