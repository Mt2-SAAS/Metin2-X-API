"""Dependencias comunes para las rutas de la API."""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from typing import Annotated
from sqlalchemy.orm import Session
# Local Imports
from app.config import settings
from app.crud.account import get_account, CRUDAccount
from app.crud.common import get_common
from app.models.account import Account, StatusType

from app.database  import get_acount_db, get_player_db, get_db
from app.core.security import AuthorityLevel

account = get_account()
common = get_common()
security = HTTPBearer()


def get_current_account(
    token: str = Depends(security)
) -> Account:
    """ 
        Verifica el token JWT y devuelve la cuenta actual.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        login: str = payload.get("sub")  # Cambiamos email por login
        if login is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc

    db_account = account.get_by_login(login=login)  # Buscamos por login en lugar de email
    if db_account is None:
        raise credentials_exception
    return db_account

def get_current_active_account(current_account: Account = Depends(get_current_account)) -> Account:
    """ 
        Verifica que la cuenta esté activa.
    """
    if current_account.status != StatusType.OK:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cuenta inactiva")
    return current_account

def require_admin_account(
    current_account: Account = Depends(get_current_account)
) -> Account:
    """
        Verifica que la cuenta tenga tiene personajes con nivel de acceso GM
        Deprecated: Use require_gm_level instead.
    """
    if not common.is_admin(current_account.login):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere nivel de autoridad o superior"
        )
    return current_account


def require_gm_level(required_level: AuthorityLevel):
    """ Verifica que la cuenta tenga el nivel de autoridad requerido o superior."""
    def authority_checker(current_account: Account = Depends(get_current_account)):
        """ Verifica que la cuenta tenga el nivel de autoridad requerido o superior.
        """
        admin_level = common.get_admin_level(current_account.login)

        if not AuthorityLevel.can_access(admin_level, required_level.value):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere nivel de autoridad {required_level.value} o superior. Tu nivel actual es {admin_level}"
            )
        return current_account
    return authority_checker


DatabaseDependency = Annotated[Session, Depends(get_db)]
DatabaseAccountDependency = Annotated[Session, Depends(get_acount_db)]
DatabasePlayerDependency = Annotated[Session, Depends(get_player_db)]
CrudAccountDependency = Annotated[CRUDAccount, Depends(get_account)]
CurrentAccountDependency = Annotated[Account, Depends(get_current_active_account)]

# Deprecated dependencies
RequireAuthorityLevel = Annotated[
    Account,
    Depends(require_admin_account)
] # Deprecated, use require_gm_level instead

# Anotated permission level dependencies
# Estos permisos son legacy y se hicieron asi porque en metin2 son asi.
RequireGMLevelImplementor = Annotated[
    Account,
    Depends(require_gm_level(AuthorityLevel.IMPLEMENTOR))
]
# Actualmente solo se esta usando este nivel de permisos, porque es el mas alto
# Si en su server en particular usan mas niveles de permisos, pueden usar los demas
# Un GM implementor normalmente es un administrador del servidor.

# Permiso para usuarios que son GM con el nivel mas alto
RequireGMLevelHighWizard = Annotated[
    Account, 
    Depends(require_gm_level(AuthorityLevel.HIGH_WIZARD))
]
# Permiso para usuarios que son GM con el nivel intermedio  
RequireGMLevelGod = Annotated[
    Account,
    Depends(require_gm_level(AuthorityLevel.GOD))
]
# Permiso para usuarios que son GM con el nivel mas bajo
RequireGMLevelLowWizard = Annotated[
    Account,
    Depends(require_gm_level(AuthorityLevel.LOW_WIZARD))
]
# Permiso para usuarios que no son GM, pero tienen cuenta registrada
RequirePlayerLevel = Annotated[
    Account,
    Depends(require_gm_level(AuthorityLevel.PLAYER))
]
