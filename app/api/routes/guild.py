from fastapi import APIRouter, Query, HTTPException
from math import ceil

# Local Imports
# from app.api.deps import database_player_dependency
from app.models.guild import Guild
from app.schemas.guild import (
    PaginatedGuildsResponse,
)

router = APIRouter(prefix="/guild", tags=["guild"])


@router.get("/guilds", response_model=PaginatedGuildsResponse)
async def list_guilds(
    # db: database_player_dependency,
    page: int = Query(1, ge=1, description="Número de página"),
    per_page: int = Query(20, ge=1, le=100, description="Elementos por página"),
):
    try:
        query = Guild.query()

        # Contar total de registros
        total = query.count()

        offset = (page - 1) * per_page
        guilds = query.order_by(Guild.level.desc()).offset(offset).limit(per_page).all()
        # Calcular metadatos de paginación
        total_pages = ceil(total / per_page)
        has_next = page < total_pages
        has_prev = page > 1

        return PaginatedGuildsResponse(
            guilds=guilds,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
            has_next=has_next,
            has_prev=has_prev
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener gremios: {str(e)}")
