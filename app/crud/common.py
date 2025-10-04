"""CRUD para manejar las operaciones comunes, como la verificación de niveles de autoridad."""
from typing import Optional

# Local Imports
from app.models.common import GMList
from app.core.security import AuthorityLevel
# from app.schemas.common import GMListBase


class CRUDGMList:
    """CRUD para manejar las operaciones comunes, como la verificación de niveles de autoridad."""

    def get_gm_by_account(self, account_login: str) -> Optional[GMList]:
        """Obtener el registro de GM por login de cuenta"""
        return GMList.filter(GMList.mAccount == account_login).first()

    def is_admin(self, account_login: str) -> bool:
        """Verifica si el usuario es un administrador (tiene un registro en GMList)"""
        gm_record = self.get_gm_by_account(account_login)
        return gm_record is not None

    def get_admin_level(self, account_login: str) -> str:
        """Obtiene el nivel de autoridad del usuario, o 'PLAYABLE' si no es admin"""
        gm_record = self.get_gm_by_account(account_login)
        # if no GM record, return PLAYABLE level
        return gm_record.mAuthority if gm_record else AuthorityLevel.PLAYABLE.value 

    def has_authority_level(self, account_login: str, required_level: AuthorityLevel) -> bool:
        """Verifica si el usuario tiene el nivel de autoridad requerido o superior"""
        current_level = self.get_admin_level(account_login)
        return AuthorityLevel.can_access(current_level, required_level.value)

    def get_authority_hierarchy(self, account_login: str) -> int:
        """Obtiene el valor jerárquico del nivel de autoridad del usuario"""
        level = self.get_admin_level(account_login)
        return AuthorityLevel.get_hierarchy_value(level)


def get_common() -> CRUDGMList:
    """
        Obtener una instancia del CRUDDownload
        Esta función es útil para inyección de dependencias en FastAPI
    """
    return CRUDGMList()
