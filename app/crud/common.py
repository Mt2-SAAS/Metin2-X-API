
from typing import Optional

# Local Imports
from app.models.common import GMList
# from app.schemas.common import GMListBase


class CRUDGMList:
    
    def get_gm_by_account(self, account_login: str) -> Optional[GMList]:
        return GMList.filter(GMList.mAccount == account_login).first()
    
    def is_admin(self, account_login: str) -> bool:
        gm_record = self.get_gm_by_account(account_login)
        return gm_record is not None


def get_common() -> CRUDGMList:
    """Obtener una instancia del CRUDDownload"""
    """Esta función es útil para inyección de dependencias en FastAPI"""
    return CRUDGMList()
