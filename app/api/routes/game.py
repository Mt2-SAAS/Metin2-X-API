from fastapi import APIRouter, Query, HTTPException, Depends
from math import ceil

# Local Imports
from app.api.deps import (
    require_gm_level_implementor
)
from app.models.player import Player, Guild
from app.crud.download import get_download, CRUDDownload
from app.crud.page import get_page, CRUDPage

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
from app.schemas.page import (
    PageCreate,
    PageUpdate,
    PageResponse,
    PaginatedPageResponse
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


# Page endpoints
@router.get("/pages", response_model=PaginatedPageResponse)
async def list_pages(
    page: int = Query(1, ge=1, description="Número de página"),
    per_page: int = Query(20, ge=1, le=100, description="Elementos por página"),
    published_only: bool = Query(False, description="Solo mostrar páginas publicadas"),
    search: str = Query(None, description="Buscar en título, slug o contenido"),
    crud: CRUDPage = Depends(get_page)
):
    """Listar páginas con paginación y filtros opcionales"""
    try:
        # Aplicar filtros y obtener datos paginados
        if search:
            pages, total = crud.search(search, page=page, per_page=per_page)
        elif published_only:
            pages, total = crud.get_published(page=page, per_page=per_page)
        else:
            pages, total = crud.get_paginated(page=page, per_page=per_page)
        
        # Calcular metadatos de paginación
        total_pages = ceil(total / per_page) if total > 0 else 1
        has_next = page < total_pages
        has_prev = page > 1
        
        return PaginatedPageResponse(
            response=pages,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
            has_next=has_next,
            has_prev=has_prev
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener páginas: {str(e)}")


@router.get("/pages/slug/{slug}", response_model=PageResponse)
async def get_page_by_slug(
    slug: str,
    crud: CRUDPage = Depends(get_page)
):
    """Obtener una página por slug"""
    page = crud.get_by_slug(slug)
    if not page:
        raise HTTPException(status_code=404, detail="Página no encontrada")
    
    # Si la página no está publicada, solo permite acceso a admins
    if not page.published:
        raise HTTPException(status_code=404, detail="Página no encontrada")
    
    return page


@router.get("/pages/{page_id}", response_model=PageResponse)
async def get_page_by_id(
    page_id: int,
    crud: CRUDPage = Depends(get_page)
):
    """Obtener una página por ID (solo admins)"""
    page = crud.get(page_id)
    if not page:
        raise HTTPException(status_code=404, detail="Página no encontrada")
    return page


@router.post("/pages", response_model=PageResponse)
async def create_page(
    _: require_gm_level_implementor,
    page: PageCreate,
    crud: CRUDPage = Depends(get_page)
):
    """Crear una nueva página"""
    try:
        # Verificar que el slug no exista
        if crud.slug_exists(page.slug):
            raise HTTPException(status_code=400, detail="Ya existe una página con este slug")
        
        new_page = crud.create(obj_in=page)
        return new_page
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear página: {str(e)}")


@router.put("/pages/{page_id}", response_model=PageResponse)
async def update_page(
    _: require_gm_level_implementor,
    page_id: int,
    page_update: PageUpdate,
    crud: CRUDPage = Depends(get_page)
):
    """Actualizar una página existente"""
    db_page = crud.get(page_id)
    if not db_page:
        raise HTTPException(status_code=404, detail="Página no encontrada")
    
    try:
        # Si se está actualizando el slug, verificar que no exista
        if page_update.slug and crud.slug_exists(page_update.slug, exclude_id=page_id):
            raise HTTPException(status_code=400, detail="Ya existe una página con este slug")
        
        updated_page = crud.update(db_obj=db_page, obj_in=page_update)
        return updated_page
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar página: {str(e)}")


@router.patch("/pages/{page_id}/publish", response_model=PageResponse)
async def publish_page(
    _: require_gm_level_implementor,
    page_id: int,
    crud: CRUDPage = Depends(get_page)
):
    """Publicar una página"""
    db_page = crud.get(page_id)
    if not db_page:
        raise HTTPException(status_code=404, detail="Página no encontrada")
    
    try:
        published_page = crud.publish(db_page)
        return published_page
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al publicar página: {str(e)}")


@router.patch("/pages/{page_id}/unpublish", response_model=PageResponse)
async def unpublish_page(
    _: require_gm_level_implementor,
    page_id: int,
    crud: CRUDPage = Depends(get_page)
):
    """Despublicar una página"""
    db_page = crud.get(page_id)
    if not db_page:
        raise HTTPException(status_code=404, detail="Página no encontrada")
    
    try:
        unpublished_page = crud.unpublish(db_page)
        return unpublished_page
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al despublicar página: {str(e)}")


@router.delete("/pages/{page_id}")
async def delete_page(
    _: require_gm_level_implementor,
    page_id: int,
    crud: CRUDPage = Depends(get_page)
):
    """Eliminar una página"""
    db_page = crud.get(page_id)
    if not db_page:
        raise HTTPException(status_code=404, detail="Página no encontrada")
    
    try:
        crud.delete(db_page)
        return {"message": "Página eliminada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar página: {str(e)}")

