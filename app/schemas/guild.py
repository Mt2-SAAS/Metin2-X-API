from pydantic import BaseModel
from typing import List


class GuildResponse(BaseModel):
    id: int
    name: str
    exp: int
    level: int
    
    class Config:
        from_attributes = True


class PaginatedGuildsResponse(BaseModel):
    guilds: List[GuildResponse]
    total: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_prev: bool
