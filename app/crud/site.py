from typing import Optional, List, Tuple
from math import ceil
from sqlalchemy.orm import joinedload
# Local Imports
from app.models.application import Site, Download, Image, Pages
from app.schemas.site import SiteCreate, SiteUpdate


class CRUDSite:
    """CRUD para manejar las operaciones de sitios"""

    def get(self, id: str) -> Optional[Site]:
        """Obtener un sitio por ID"""
        return Site.filter(Site.id == id).options(
            joinedload(Site.downloads),
            joinedload(Site.images),
            joinedload(Site.footer_menu)
        ).first()

    def get_by_slug(self, slug: str) -> Optional[Site]:
        """Obtener un sitio por slug"""
        return Site.filter(Site.slug == slug).options(
            joinedload(Site.downloads),
            joinedload(Site.images),
            joinedload(Site.footer_menu)
        ).first()

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[Site]:
        """Obtener múltiples sitios con paginación básica"""
        return Site.query().offset(skip).limit(limit).all()

    def get_paginated(self, page: int = 1, per_page: int = 20) -> Tuple[List[Site], int]:
        """Obtener sitios paginados con información de total"""
        query = Site.query()
        total = query.count()
        
        offset = (page - 1) * per_page
        sites = query.options(
            joinedload(Site.downloads),
            joinedload(Site.images),
            joinedload(Site.footer_menu)
        ).offset(offset).limit(per_page).all()
        
        return sites, total

    def get_active(self, page: int = 1, per_page: int = 20) -> Tuple[List[Site], int]:
        """Obtener solo los sitios activos con paginación"""
        query = Site.filter(Site.is_active == True)
        total = query.count()
        
        offset = (page - 1) * per_page
        sites = query.options(
            joinedload(Site.downloads),
            joinedload(Site.images),
            joinedload(Site.footer_menu)
        ).offset(offset).limit(per_page).all()
        
        return sites, total

    def get_in_maintenance(self, page: int = 1, per_page: int = 20) -> Tuple[List[Site], int]:
        """Obtener sitios en modo mantenimiento con paginación"""
        query = Site.filter(Site.maintenance_mode == True)
        total = query.count()
        
        offset = (page - 1) * per_page
        sites = query.options(
            joinedload(Site.downloads),
            joinedload(Site.images),
            joinedload(Site.footer_menu)
        ).offset(offset).limit(per_page).all()
        
        return sites, total

    def create(self, obj_in: SiteCreate) -> Site:
        """Crear un nuevo sitio"""
        # Verificar que el slug no exista
        if self.slug_exists(obj_in.slug):
            raise ValueError(f"Site with slug '{obj_in.slug}' already exists")
            
        db_obj = Site(
            name=obj_in.name,
            slug=obj_in.slug,
            initial_level=obj_in.initial_level,
            max_level=obj_in.max_level,
            rates=obj_in.rates,
            facebook_url=obj_in.facebook_url,
            facebook_enable=obj_in.facebook_enable,
            footer_info=obj_in.footer_info,
            footer_menu_enable=obj_in.footer_menu_enable,
            footer_info_enable=obj_in.footer_info_enable,
            forum_url=obj_in.forum_url,
            last_online=obj_in.last_online,
            is_active=obj_in.is_active,
            maintenance_mode=obj_in.maintenance_mode
        )
        return db_obj.save()

    def update(self, db_obj: Site, obj_in: SiteUpdate) -> Site:
        """Actualizar un sitio existente"""
        update_data = obj_in.model_dump(exclude_unset=True)
        
        # Verificar que el slug no exista si se está actualizando
        if "slug" in update_data and self.slug_exists(update_data["slug"], exclude_id=db_obj.id):
            raise ValueError(f"Site with slug '{update_data['slug']}' already exists")
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        return db_obj.save()

    def delete(self, db_obj: Site) -> None:
        """Eliminar un sitio"""
        db_obj.delete()

    def activate(self, db_obj: Site) -> Site:
        """Activar un sitio (cambiar is_active a True)"""
        db_obj.is_active = True
        return db_obj.save()

    def deactivate(self, db_obj: Site) -> Site:
        """Desactivar un sitio (cambiar is_active a False)"""
        db_obj.is_active = False
        return db_obj.save()

    def enable_maintenance(self, db_obj: Site) -> Site:
        """Habilitar modo mantenimiento"""
        db_obj.maintenance_mode = True
        return db_obj.save()

    def disable_maintenance(self, db_obj: Site) -> Site:
        """Deshabilitar modo mantenimiento"""
        db_obj.maintenance_mode = False
        return db_obj.save()

    def slug_exists(self, slug: str, exclude_id: Optional[str] = None) -> bool:
        """Verificar si un slug ya existe"""
        query = Site.filter(Site.slug == slug)
        if exclude_id:
            query = query.filter(Site.id != exclude_id)
        return query.first() is not None

    def count_total(self) -> int:
        """Contar total de sitios"""
        return Site.query().count()

    def count_active(self) -> int:
        """Contar sitios activos"""
        return Site.filter(Site.is_active == True).count()

    def count_in_maintenance(self) -> int:
        """Contar sitios en mantenimiento"""
        return Site.filter(Site.maintenance_mode == True).count()

    def search(self, query: str, page: int = 1, per_page: int = 20) -> Tuple[List[Site], int]:
        """Buscar sitios por texto en name, slug o footer_info"""
        search_query = Site.filter(
            (Site.name.like(f"%{query}%")) |
            (Site.slug.like(f"%{query}%")) |
            (Site.footer_info.like(f"%{query}%"))
        )
        total = search_query.count()
        
        offset = (page - 1) * per_page
        sites = search_query.options(
            joinedload(Site.downloads),
            joinedload(Site.images),
            joinedload(Site.footer_menu)
        ).offset(offset).limit(per_page).all()
        
        return sites, total

    def get_with_downloads_count(self, page: int = 1, per_page: int = 20) -> Tuple[List[tuple], int]:
        """Obtener sitios con el conteo de descargas"""
        from sqlalchemy import func
        
        query = Site.query().outerjoin(Download).group_by(Site.id).add_columns(
            func.count(Download.id).label('downloads_count')
        )
        
        total = Site.query().count()
        
        offset = (page - 1) * per_page
        result = query.offset(offset).limit(per_page).all()
        
        return result, total

    def get_sites_by_level_range(self, min_level: str, max_level: str, page: int = 1, per_page: int = 20) -> Tuple[List[Site], int]:
        """Obtener sitios por rango de niveles"""
        query = Site.filter(
            Site.initial_level >= min_level,
            Site.max_level <= max_level
        )
        total = query.count()
        
        offset = (page - 1) * per_page
        sites = query.options(
            joinedload(Site.downloads),
            joinedload(Site.images),
            joinedload(Site.footer_menu)
        ).offset(offset).limit(per_page).all()
        
        return sites, total


def get_site() -> CRUDSite:
    """Obtener una instancia del CRUDSite"""
    return CRUDSite()