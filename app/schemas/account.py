from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum

class StatusType(str,Enum):
    ACCEPT = "OK"
    BANNED = "BANNED"


class AccountBase(BaseModel):
    """Base schema for Account with common fields"""
    login: str = Field(..., max_length=16, description="Login del usuario (máx. 16 caracteres)")
    email: EmailStr = Field(..., max_length=100, description="Email del usuario")
    social_id: str = Field(default="", max_length=7, description="ID social del usuario")
    status: StatusType = Field(..., description="Estado del usuario")

    class Config:
        from_attributes = True  # Permite la creación desde ORM (antes llamada 'orm_mode')

class AccountCreate(AccountBase):
    """Schema for creating a new account"""
    password: str = Field(..., max_length=42, description="Contraseña hasheada del usuario")

class AccountPasswordUpdate(BaseModel):
    """Schema for updating account password"""
    old_password: str = Field(..., max_length=42, description="Contraseña actual del usuario")
    new_password: str = Field(..., max_length=42, description="Nueva contraseña hasheada del usuario")

class Account(AccountCreate):
    pass

class AccountUpdate(BaseModel):
    """Schema for updating account information"""
    social_id: Optional[str] = Field(None, max_length=7, description="ID social del usuario")
    # email: EmailStr = Field(..., max_length=100, description="Email del usuario")

class AccountInDB(AccountBase):
    """Complete account schema including database fields"""
    id: int
    password: str = Field(..., max_length=42, description="Contraseña hasheada del usuario")

    class Config:
        from_attributes = True
