from fastapi import APIRouter, Query, HTTPException, Depends
from math import ceil

# Local Imports
from app.api.deps import (
    require_gm_level_implementor
)
from app.models.player import Player, Guild
from app.crud.download import get_download, CRUDDownload
from app.crud.page import get_page, CRUDPage
from app.crud.site import get_site, CRUDSite

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
from app.schemas.site import (
    SiteCreate,
    SiteUpdate,
    SiteResponse,
    PaginatedSiteResponse
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
    site_id: int = Query(None, description="Filtrar por sitio"),
    published_only: bool = Query(False, description="Solo mostrar descargas publicadas"),
    search: str = Query(None, description="Buscar en provider, category o link"),
    crud: CRUDDownload = Depends(get_download)
):
    """Listar descargas con paginación y filtros opcionales"""
    try:
        # Aplicar filtros y obtener datos paginados
        if search:
            downloads, total = crud.search(search, page=page, per_page=per_page)
        elif site_id and category:
            downloads, total = crud.get_by_site_and_category(site_id, category, page=page, per_page=per_page)
        elif site_id:
            downloads, total = crud.get_by_site(site_id, page=page, per_page=per_page)
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


# Site endpoints
@router.get("/sites", response_model=PaginatedSiteResponse)
async def list_sites(
    page: int = Query(1, ge=1, description="Número de página"),
    per_page: int = Query(20, ge=1, le=100, description="Elementos por página"),
    active_only: bool = Query(False, description="Solo mostrar sitios activos"),
    maintenance_only: bool = Query(False, description="Solo mostrar sitios en mantenimiento"),
    search: str = Query(None, description="Buscar en nombre, slug o información de footer"),
    crud: CRUDSite = Depends(get_site)
):
    """Listar sitios con paginación y filtros opcionales"""
    try:
        # Aplicar filtros y obtener datos paginados
        if search:
            sites, total = crud.search(search, page=page, per_page=per_page)
        elif active_only:
            sites, total = crud.get_active(page=page, per_page=per_page)
        elif maintenance_only:
            sites, total = crud.get_in_maintenance(page=page, per_page=per_page)
        else:
            sites, total = crud.get_paginated(page=page, per_page=per_page)
        
        # Calcular metadatos de paginación
        total_pages = ceil(total / per_page) if total > 0 else 1
        has_next = page < total_pages
        has_prev = page > 1
        
        return PaginatedSiteResponse(
            response=sites,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
            has_next=has_next,
            has_prev=has_prev
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener sitios: {str(e)}")


@router.get("/sites/slug/{slug}", response_model=SiteResponse)
async def get_site_by_slug(
    slug: str,
    crud: CRUDSite = Depends(get_site)
):
    """Obtener un sitio por slug"""
    site = crud.get_by_slug(slug)
    if not site:
        raise HTTPException(status_code=404, detail="Sitio no encontrado")
    
    # Si el sitio no está activo, solo permite acceso a admins
    if not site.is_active:
        raise HTTPException(status_code=404, detail="Sitio no encontrado")
    
    return site


@router.get("/sites/{site_id}", response_model=SiteResponse)
async def get_site_by_id(
    _: require_gm_level_implementor,
    site_id: int,
    crud: CRUDSite = Depends(get_site)
):
    """Obtener un sitio por ID (solo admins)"""
    site = crud.get(site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Sitio no encontrado")
    return site


@router.post("/sites", response_model=SiteResponse)
async def create_site(
    _: require_gm_level_implementor,
    site: SiteCreate,
    crud: CRUDSite = Depends(get_site)
):
    """Crear un nuevo sitio"""
    try:
        new_site = crud.create(obj_in=site)
        return new_site
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear sitio: {str(e)}")


@router.put("/sites/{site_id}", response_model=SiteResponse)
async def update_site(
    _: require_gm_level_implementor,
    site_id: int,
    site_update: SiteUpdate,
    crud: CRUDSite = Depends(get_site)
):
    """Actualizar un sitio existente"""
    db_site = crud.get(site_id)
    if not db_site:
        raise HTTPException(status_code=404, detail="Sitio no encontrado")
    
    try:
        updated_site = crud.update(db_obj=db_site, obj_in=site_update)
        return updated_site
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar sitio: {str(e)}")


@router.patch("/sites/{site_id}/activate", response_model=SiteResponse)
async def activate_site(
    _: require_gm_level_implementor,
    site_id: int,
    crud: CRUDSite = Depends(get_site)
):
    """Activar un sitio"""
    db_site = crud.get(site_id)
    if not db_site:
        raise HTTPException(status_code=404, detail="Sitio no encontrado")
    
    try:
        activated_site = crud.activate(db_site)
        return activated_site
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al activar sitio: {str(e)}")


@router.patch("/sites/{site_id}/deactivate", response_model=SiteResponse)
async def deactivate_site(
    _: require_gm_level_implementor,
    site_id: int,
    crud: CRUDSite = Depends(get_site)
):
    """Desactivar un sitio"""
    db_site = crud.get(site_id)
    if not db_site:
        raise HTTPException(status_code=404, detail="Sitio no encontrado")
    
    try:
        deactivated_site = crud.deactivate(db_site)
        return deactivated_site
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al desactivar sitio: {str(e)}")


@router.patch("/sites/{site_id}/maintenance/enable", response_model=SiteResponse)
async def enable_maintenance_mode(
    _: require_gm_level_implementor,
    site_id: int,
    crud: CRUDSite = Depends(get_site)
):
    """Habilitar modo mantenimiento"""
    db_site = crud.get(site_id)
    if not db_site:
        raise HTTPException(status_code=404, detail="Sitio no encontrado")
    
    try:
        maintenance_site = crud.enable_maintenance(db_site)
        return maintenance_site
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al habilitar mantenimiento: {str(e)}")


@router.patch("/sites/{site_id}/maintenance/disable", response_model=SiteResponse)
async def disable_maintenance_mode(
    _: require_gm_level_implementor,
    site_id: int,
    crud: CRUDSite = Depends(get_site)
):
    """Deshabilitar modo mantenimiento"""
    db_site = crud.get(site_id)
    if not db_site:
        raise HTTPException(status_code=404, detail="Sitio no encontrado")
    
    try:
        normal_site = crud.disable_maintenance(db_site)
        return normal_site
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al deshabilitar mantenimiento: {str(e)}")


@router.delete("/sites/{site_id}")
async def delete_site(
    _: require_gm_level_implementor,
    site_id: int,
    crud: CRUDSite = Depends(get_site)
):
    """Eliminar un sitio"""
    db_site = crud.get(site_id)
    if not db_site:
        raise HTTPException(status_code=404, detail="Sitio no encontrado")
    
    try:
        crud.delete(db_site)
        return {"message": "Sitio eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar sitio: {str(e)}")


@router.get("/sites/{site_id}/stats")
async def get_site_stats(
    _: require_gm_level_implementor,
    site_id: int,
    crud: CRUDSite = Depends(get_site)
):
    """Obtener estadísticas de un sitio"""
    db_site = crud.get(site_id)
    if not db_site:
        raise HTTPException(status_code=404, detail="Sitio no encontrado")
    
    try:
        from app.crud.download import get_download
        download_crud = get_download()
        
        # Contar descargas del sitio
        downloads_list, downloads_total = download_crud.get_by_site(site_id, page=1, per_page=1000)
        downloads_published = len([d for d in downloads_list if d.published])
        
        return {
            "site_id": site_id,
            "site_name": db_site.name,
            "downloads_total": downloads_total,
            "downloads_published": downloads_published,
            "is_active": db_site.is_active,
            "maintenance_mode": db_site.maintenance_mode,
            "created_at": db_site.created_at,
            "updated_at": db_site.updated_at
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")

