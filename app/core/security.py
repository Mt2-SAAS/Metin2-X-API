from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from enum import Enum
from ..config import settings

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


class AuthorityLevel(Enum):
    """Niveles de autoridad para el acceso a funcionalidades"""
    PLAYABLE = "PLAYABLE"

    # GM Levels
    PLAYER = "PLAYER"
    LOW_WIZARD = "LOW_WIZARD"
    HIGH_WIZARD = "HIGH_WIZARD"
    GOD = "GOD"
    IMPLEMENTOR = "IMPLEMENTOR"
    
    @classmethod
    def get_hierarchy_value(cls, level: str) -> int:
        """Obtiene el valor jerárquico del nivel"""
        # Jerarquía de niveles (mayor número = mayor autoridad)
        hierarchy_map = {
            "PLAYABLE": 0,
            "PLAYER": 1, # from here start GM levels, PLAYER is lower level
            "LOW_WIZARD": 2,
            "HIGH_WIZARD": 3,
            "GOD": 4,
            "IMPLEMENTOR": 5
        }
        return hierarchy_map.get(level, 0)
    
    @classmethod
    def is_valid_level(cls, level: str) -> bool:
        """Verifica si el nivel es válido"""
        return level in cls._hierarchy
    
    @classmethod
    def can_access(cls, user_level: str, required_level: str) -> bool:
        """Verifica si un usuario puede acceder a una funcionalidad"""
        user_hierarchy = cls.get_hierarchy_value(user_level)
        required_hierarchy = cls.get_hierarchy_value(required_level)
        return user_hierarchy >= required_hierarchy
    
    @classmethod
    def get_all_levels(cls) -> dict:
        """Retorna todos los niveles disponibles con su jerarquía"""
        return {level.value: cls._hierarchy[level.value] for level in cls}
    
    @classmethod
    def get_levels_list(cls) -> list:
        """Retorna lista de niveles ordenados por jerarquía"""
        return sorted(cls._hierarchy.keys(), key=lambda x: cls._hierarchy[x])
