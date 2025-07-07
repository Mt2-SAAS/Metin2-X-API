from pydantic import BaseModel
from typing import Optional



class GMListBase(BaseModel):
    mAccount: str
    mName: Optional[str] = None
    mContactIP: Optional[str] = None
    mServerIP: Optional[str] = None
    mAuthority: int = 0

