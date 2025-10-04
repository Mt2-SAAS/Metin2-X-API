""" Esquemas para la gestión de cuentas de usuario """
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum

class StatusType(str,Enum):
    """Enum para los estados del usuario"""
    ACCEPT = "OK"
    BANNED = "BANNED"


class AccountBase(BaseModel):
    """Esquema base para la cuenta"""
    login: str = Field(..., max_length=16, description="Login del usuario (máx. 16 caracteres)")
    email: EmailStr = Field(..., max_length=100, description="Email del usuario")
    social_id: str = Field(default="", max_length=7, description="ID social del usuario")
    status: StatusType = Field(..., description="Estado del usuario")

    class Config:
        """ Configuración para permitir la creación desde ORM """
        from_attributes = True  # Permite la creación desde ORM (antes llamada 'orm_mode')

class AccountCreate(AccountBase):
    """Esquema para la creación de una cuenta"""
    password: str = Field(..., max_length=42, description="Contraseña hasheada del usuario")

class AccountPasswordUpdate(BaseModel):
    """Esquema para actualizar la contraseña de la cuenta"""
    old_password: str = Field(
        ...,
        max_length=42,
        description="Contraseña actual del usuario"
    )
    new_password: str = Field(
        ...,
        max_length=42,
        description="Nueva contraseña hasheada del usuario"
    )

class Account(AccountCreate):
    """Esquema de la cuenta sin la contraseña"""

class AccountUpdate(BaseModel):
    """Esquema para actualizar la cuenta"""
    social_id: Optional[str] = Field(None, max_length=7, description="ID social del usuario")
    # email: EmailStr = Field(..., max_length=100, description="Email del usuario")

class AccountInDB(AccountBase):
    """Esquema completo de la cuenta en la base de datos"""
    id: int
    password: str = Field(..., max_length=42, description="Contraseña hasheada del usuario")

    class Config:
        """ Configuración para permitir la creación desde ORM """
        from_attributes = True
