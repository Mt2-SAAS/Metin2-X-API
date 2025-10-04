"""Esquemas para las operaciones relacionadas con jugadores y gremios"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class PlayerResponse(BaseModel):
    """Esquema para la información básica del jugador"""
    account_id: int
    name: str
    job: int
    level: int
    exp: int

    class Config:
        """Configura el modelo para permitir la creación desde atributos"""
        from_attributes = True

class PlayerDetailResponse(BaseModel):
    """Esquema para la información detallada del jugador"""
    account_id: int
    name: str
    job: int
    level: int
    exp: int
    last_play: Optional[datetime] = None

    class Config:
        """Configura el modelo para permitir la creación desde atributos"""
        from_attributes = True


class PlayerUserResponse(BaseModel):
    """Esquema para la información del usuario del jugador"""
    players: List[PlayerDetailResponse]

class PaginatedPlayersResponse(BaseModel):
    """E|squema para respuestas paginadas de jugadores"""
    response: List[PlayerResponse]
    total: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_prev: bool

class GuildResponse(BaseModel):
    """Esquema para la información del gremio"""
    id: int
    name: str
    exp: int
    level: int

    class Config:
        """Configura el modelo para permitir la creación desde atributos"""
        from_attributes = True


class PaginatedGuildsResponse(BaseModel):
    """Esquema para respuestas paginadas de gremios"""
    response: List[GuildResponse]
    total: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_prev: bool
