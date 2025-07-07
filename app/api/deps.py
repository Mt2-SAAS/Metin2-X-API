from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from typing import Annotated
from sqlalchemy.orm import Session
# Local Imports
from app.config import settings
from app.crud.account import get_account, CRUDAccount
from app.crud.common import get_common
from app.models.account import Account

from app.database  import get_acount_db, get_player_db, get_db

account = get_account()
common = get_common()
security = HTTPBearer()


def get_current_account(
    token: str = Depends(security)
) -> Account:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        login: str = payload.get("sub")  # Cambiamos email por login
        if login is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    db_account = account.get_by_login(login=login)  # Buscamos por login en lugar de email
    if db_account is None:
        raise credentials_exception
    return db_account

def get_current_active_account(current_account: Account = Depends(get_current_account)) -> Account:
    # Asumiendo que tu modelo Account tiene un campo is_active
    # Si no lo tiene, puedes omitir esta verificación o implementar otra lógica
    if current_account.status != "OK":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cuenta inactiva")
    return current_account

def require_admin_account(
    current_account: Account = Depends(get_current_account)
) -> Account:
    if not common.is_admin(current_account.login):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere nivel de autoridad o superior"
        )
    return current_account

database_dependency = Annotated[Session, Depends(get_db)]
database_account_dependency = Annotated[Session, Depends(get_acount_db)]
database_player_dependency = Annotated[Session, Depends(get_player_db)]
crud_account_dependency = Annotated[CRUDAccount, Depends(get_account)]
current_account_dependency = Annotated[Account, Depends(get_current_active_account)]
require_authority_level = Annotated[Account, Depends(require_admin_account)]
