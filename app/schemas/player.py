from pydantic import BaseModel
from typing import List


class PlayerResponse(BaseModel):
    account_id: int
    name: str
    job: int
    level: int
    exp: int
    
    class Config:
        from_attributes = True

class PlayerUserResponse(BaseModel):
    players: List[PlayerResponse]

class PaginatedPlayersResponse(BaseModel):
    response: List[PlayerResponse]
    total: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_prev: bool

class GuildResponse(BaseModel):
    id: int
    name: str
    exp: int
    level: int
    
    class Config:
        from_attributes = True


class PaginatedGuildsResponse(BaseModel):
    response: List[GuildResponse]
    total: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_prev: bool
