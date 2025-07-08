from fastapi import APIRouter, Query, HTTPException, Depends
from math import ceil

# Local Imports
from app.api.deps import (
    require_gm_level_implementor
)
from app.models.player import Player, Guild
from app.crud.download import get_download, CRUDDownload

from app.schemas.player import (
    PaginatedGuildsResponse,
    PaginatedPlayersResponse
)
from app.schemas.download import (
    DownloadCreate,
    DownloadUpdate,
    DownloadResponse,
    PaginatedDownloadResponse
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
            response=players,
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
            response=guilds,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
            has_next=has_next,
            has_prev=has_prev
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener gremios: {str(e)}")


# Download endpoints
@router.get("/downloads", response_model=PaginatedDownloadResponse)
async def list_downloads(
    page: int = Query(1, ge=1, description="Número de página"),
    per_page: int = Query(20, ge=1, le=100, description="Elementos por página"),
    category: str = Query(None, description="Filtrar por categoría"),
    provider: str = Query(None, description="Filtrar por proveedor"),
    published_only: bool = Query(False, description="Solo mostrar descargas publicadas"),
    search: str = Query(None, description="Buscar en provider, category o link"),
    crud: CRUDDownload = Depends(get_download)
):
    """Listar descargas con paginación y filtros opcionales"""
    try:
        # Aplicar filtros y obtener datos paginados
        if search:
            downloads, total = crud.search(search, page=page, per_page=per_page)
        elif category:
            downloads, total = crud.get_by_category(category, page=page, per_page=per_page)
        elif provider:
            downloads, total = crud.get_by_provider(provider, page=page, per_page=per_page)
        elif published_only:
            downloads, total = crud.get_published(page=page, per_page=per_page)
        else:
            downloads, total = crud.get_paginated(page=page, per_page=per_page)
        
        # Calcular metadatos de paginación
        total_pages = ceil(total / per_page) if total > 0 else 1
        has_next = page < total_pages
        has_prev = page > 1
        
        return PaginatedDownloadResponse(
            response=downloads,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
            has_next=has_next,
            has_prev=has_prev
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener descargas: {str(e)}")


@router.get("/downloads/{download_id}", response_model=DownloadResponse)
async def get_download_by_id(
    _: require_gm_level_implementor,
    download_id: int,
    crud: CRUDDownload = Depends(get_download)
):
    """Obtener una descarga por ID"""
    download = crud.get(download_id)
    if not download:
        raise HTTPException(status_code=404, detail="Descarga no encontrada")
    return download


@router.post("/downloads", response_model=DownloadResponse)
async def create_download(
    _: require_gm_level_implementor,
    download: DownloadCreate,
    crud: CRUDDownload = Depends(get_download)
):
    """Crear una nueva descarga"""
    try:
        new_download = crud.create(obj_in=download)
        return new_download
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear descarga: {str(e)}")


@router.put("/downloads/{download_id}", response_model=DownloadResponse)
async def update_download(
    _: require_gm_level_implementor,
    download_id: int,
    download_update: DownloadUpdate,
    crud: CRUDDownload = Depends(get_download)
):
    """Actualizar una descarga existente"""
    db_download = crud.get(download_id)
    if not db_download:
        raise HTTPException(status_code=404, detail="Descarga no encontrada")
    
    try:
        updated_download = crud.update(db_obj=db_download, obj_in=download_update)
        return updated_download
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar descarga: {str(e)}")


@router.patch("/downloads/{download_id}/publish", response_model=DownloadResponse)
async def publish_download(
    _: require_gm_level_implementor,
    download_id: int,
    crud: CRUDDownload = Depends(get_download)
):
    """Publicar una descarga"""
    db_download = crud.get(download_id)
    if not db_download:
        raise HTTPException(status_code=404, detail="Descarga no encontrada")
    
    try:
        published_download = crud.publish(db_download)
        return published_download
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al publicar descarga: {str(e)}")


@router.patch("/downloads/{download_id}/unpublish", response_model=DownloadResponse)
async def unpublish_download(
    _: require_gm_level_implementor,
    download_id: int,
    crud: CRUDDownload = Depends(get_download)
):
    """Despublicar una descarga"""
    db_download = crud.get(download_id)
    if not db_download:
        raise HTTPException(status_code=404, detail="Descarga no encontrada")
    
    try:
        unpublished_download = crud.unpublish(db_download)
        return unpublished_download
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al despublicar descarga: {str(e)}")


@router.delete("/downloads/{download_id}")
async def delete_download(
    _: require_gm_level_implementor,
    download_id: int,
    crud: CRUDDownload = Depends(get_download)
):
    """Eliminar una descarga"""
    db_download = crud.get(download_id)
    if not db_download:
        raise HTTPException(status_code=404, detail="Descarga no encontrada")
    
    try:
        crud.delete(db_download)
        return {"message": "Descarga eliminada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar descarga: {str(e)}")

