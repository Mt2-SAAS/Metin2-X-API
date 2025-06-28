from fastapi import APIRouter, Query, HTTPException
from math import ceil

# Local Imports
# from app.api.deps import database_player_dependency
from app.models.player import Player, Guild

from app.schemas.player import (
    PaginatedGuildsResponse,
    PaginatedPlayersResponse
)

router = APIRouter(prefix="/game", tags=["game"])


@router.get("/players", response_model=PaginatedPlayersResponse)
async def list_players(
    # db: database_player_dependency,
    page: int = Query(1, ge=1, description="Número de página"),
    per_page: int = Query(20, ge=1, le=100, description="Elementos por página"),
):
    try:
        query = Player.query()

        # Contar total de registros
        total = query.count()

        offset = (page - 1) * per_page
        players = query.order_by(Player.level.desc()).offset(offset).limit(per_page).all()
        # Calcular metadatos de paginación
        total_pages = ceil(total / per_page)
        has_next = page < total_pages
        has_prev = page > 1

        return PaginatedPlayersResponse(
            players=players,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
            has_next=has_next,
            has_prev=has_prev
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener jugadores: {str(e)}")


@router.get("/guilds", response_model=PaginatedGuildsResponse)
async def list_guilds(
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

