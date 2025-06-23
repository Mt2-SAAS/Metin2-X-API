from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
# Local Imports
from app.core.security import create_access_token
from app.config import settings
from app.schemas.account import (
    AccountCreate, 
    AccountUpdate, 
    AccountBase, 
    AccountPasswordUpdate
)
from app.api.deps import (
    crud_account_dependency,
    current_account_dependency
)


router = APIRouter(prefix="/account", tags=["account"])


@router.post("/register", response_model=AccountBase)
def create_account(
    account_in: AccountCreate,
    account: crud_account_dependency,
):
    """Registrar nueva cuenta"""
    # Verificar si el login ya existe
    if account.get_by_login(login=account_in.login):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El login ya está registrado"
        )
    
    # Verificar si el email ya existe
    if account.get_by_email(email=account_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    return account.create(obj_in=account_in)

@router.post("/token")
def login_for_access_token(
    account: crud_account_dependency,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """Login y obtener token de acceso (usar login como username)"""
    db_account = account.authenticate(login=form_data.username, password=form_data.password)
    if not db_account:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_account.login},  # Usamos login como identificador
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=AccountBase)
def read_account_me(current_account: current_account_dependency):
    """Obtener información de la cuenta actual"""
    return current_account


@router.put("/me", response_model=AccountBase)
def update_account_me(
    account_in: AccountUpdate,
    account: crud_account_dependency,
    current_account: current_account_dependency,
):
    """Actualizar información de la cuenta actual"""
    # Verificar que el social_id sea un número de 7 dígitos
    if account_in.social_id:
        if not account_in.social_id.isdigit() or len(account_in.social_id) != 7:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El ID social debe tener exactamente 7 dígitos numéricos"
            )
    return account.update(db_obj=current_account, obj_in=account_in)


@router.put("/me/password", response_model=AccountBase)
def update_password_account_me(
    account: crud_account_dependency,
    account_in: AccountPasswordUpdate,
    current_account: current_account_dependency,
):
    """Metodo solo para actualizar la contraseña de la cuenta actual"""
    acc = account.authenticate(login=current_account.login, password=account_in.old_password)
    if not acc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Contraseña actual incorrecta",
            headers={"WWW-Authenticate": "Bearer"},
        )
    db_obj = account.update_password(db_obj=acc, new_password=account_in.new_password)
    return db_obj
