"""CRUD para manejar las operaciones de la cuenta"""
from typing import Optional
# Local Imports
from app.models.account import Account, StatusType
from app.schemas.account import AccountCreate, AccountUpdate
from app.core.hashers import make_password, validate_password

class CRUDAccount:
    """CRUD para manejar las operaciones de la cuenta"""

    def get(self, account_id: int) -> Optional[Account]:
        """Obtener una cuenta por ID"""
        return Account.filter(id=account_id).first()

    def get_by_login(self, login: str) -> Optional[Account]:
        """Obtener una cuenta por login"""
        return Account.filter(Account.login == login).first()

    def get_by_email(self, email: str) -> Optional[Account]:
        """Obtener una cuenta por email"""
        return Account.filter(Account.email == email).first()

    def create(self, obj_in: AccountCreate) -> Account:
        """Crear una nueva cuenta"""
        hashed_password = make_password(obj_in.password)
        db_obj = Account(
            login=obj_in.login,
            password=hashed_password,  # Asumo que el campo se llama 'password' en el modelo
            social_id=obj_in.social_id,
            email=obj_in.email
        )
        return db_obj.save()  # Utiliza el método save para insertar en la base de datos

    def update(self, db_obj: Account, obj_in: AccountUpdate) -> Account:
        """Actualizar una cuenta existente"""
        update_data = obj_in.model_dump(exclude_unset=True)

        if "password" in update_data:
            hashed_password = make_password(update_data["password"])
            update_data["password"] = hashed_password

        for field, value in update_data.items():
            setattr(db_obj, field, value)
        return db_obj.save()  # Utiliza el método save para actualizar en la base de datos

    def authenticate(self, login: str, password: str) -> Optional[Account]:
        """Autenticar un usuario por login y contraseña
           Tambien verifica que la cuenta no este baneada
        """
        account = self.get_by_login(login=login)
        if not account:
            return None
        if validate_password(
            account.password,
            password
            ) and self.is_active(account):  # Asume que verify_password puede comparar
            return account
        return None

    def update_password(self, db_obj: Account, new_password: str) -> Account:
        """Actualizar la contraseña de una cuenta existente"""
        hashed_password = make_password(new_password)
        db_obj.password = hashed_password
        return db_obj.save()

    def is_active(self, account: Account) -> bool:
        """Verificar si la cuenta está activa"""
        # Puedes añadir lógica adicional aquí si tu modelo tiene un campo 'is_active'
        if account.status == StatusType.OK:
            return True
        return False

    def is_superuser(self) -> bool:
        """Verificar si la cuenta es de superusuario"""
        # Puedes añadir lógica adicional aquí si tu modelo tiene un campo 'is_superuser'
        return False


def get_account() -> CRUDAccount:
    """
        Obtener una instancia del CRUDAccount
        Esta función es útil para inyección de dependencias en FastAPI
    """
    return CRUDAccount()
