from typing import Optional, List, Tuple
from math import ceil
from sqlalchemy.orm import joinedload
# Local Imports
from app.models.application import Download, Site
from app.schemas.download import DownloadCreate, DownloadUpdate


class CRUDDownload:
    """CRUD para manejar las operaciones de descargas"""

    def get(self, id: int) -> Optional[Download]:
        """Obtener una descarga por ID"""
        return Download.filter(Download.id == id).options(joinedload(Download.site)).first()

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[Download]:
        """Obtener múltiples descargas con paginación básica"""
        return Download.query().offset(skip).limit(limit).all()

    def get_paginated(self, page: int = 1, per_page: int = 20) -> Tuple[List[Download], int]:
        """Obtener descargas paginadas con información de total"""
        query = Download.query()
        total = query.count()
        
        offset = (page - 1) * per_page
        downloads = query.options(joinedload(Download.site)).offset(offset).limit(per_page).all()
        
        return downloads, total

    def get_by_category(self, category: str, page: int = 1, per_page: int = 20) -> Tuple[List[Download], int]:
        """Obtener descargas por categoría con paginación"""
        query = Download.filter(Download.category == category)
        total = query.count()
        
        offset = (page - 1) * per_page
        downloads = query.options(joinedload(Download.site)).offset(offset).limit(per_page).all()
        
        return downloads, total

    def get_published(self, page: int = 1, per_page: int = 20) -> Tuple[List[Download], int]:
        """Obtener solo las descargas publicadas con paginación"""
        query = Download.filter(Download.published == True)
        total = query.count()
        
        offset = (page - 1) * per_page
        downloads = query.options(joinedload(Download.site)).offset(offset).limit(per_page).all()
        
        return downloads, total

    def get_by_provider(self, provider: str, page: int = 1, per_page: int = 20) -> Tuple[List[Download], int]:
        """Obtener descargas por proveedor con paginación"""
        query = Download.filter(Download.provider == provider)
        total = query.count()
        
        offset = (page - 1) * per_page
        downloads = query.options(joinedload(Download.site)).offset(offset).limit(per_page).all()
        
        return downloads, total

    def create(self, obj_in: DownloadCreate) -> Download:
        """Crear una nueva descarga"""
        # Verificar que el sitio existe
        site = Site.filter(Site.id == obj_in.site_id).first()
        if not site:
            raise ValueError(f"Site with id {obj_in.site_id} not found")
            
        db_obj = Download(
            provider=obj_in.provider,
            size=obj_in.size,
            link=obj_in.link,
            category=obj_in.category,
            published=obj_in.published,
            site_id=obj_in.site_id
        )
        return db_obj.save()

    def update(self, db_obj: Download, obj_in: DownloadUpdate) -> Download:
        """Actualizar una descarga existente"""
        update_data = obj_in.model_dump(exclude_unset=True)
        
        # Verificar que el sitio existe si se está actualizando
        if "site_id" in update_data:
            site = Site.filter(Site.id == update_data["site_id"]).first()
            if not site:
                raise ValueError(f"Site with id {update_data['site_id']} not found")
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        return db_obj.save()

    def delete(self, db_obj: Download) -> None:
        """Eliminar una descarga"""
        db_obj.delete()

    def publish(self, db_obj: Download) -> Download:
        """Publicar una descarga (cambiar published a True)"""
        db_obj.published = True
        return db_obj.save()

    def unpublish(self, db_obj: Download) -> Download:
        """Despublicar una descarga (cambiar published a False)"""
        db_obj.published = False
        return db_obj.save()

    def get_by_site(self, site_id: int, page: int = 1, per_page: int = 20) -> Tuple[List[Download], int]:
        """Obtener descargas por sitio con paginación"""
        query = Download.filter(Download.site_id == site_id)
        total = query.count()
        
        offset = (page - 1) * per_page
        downloads = query.options(joinedload(Download.site)).offset(offset).limit(per_page).all()
        
        return downloads, total
        
    def get_by_site_and_category(self, site_id: int, category: str, page: int = 1, per_page: int = 20) -> Tuple[List[Download], int]:
        """Obtener descargas por sitio y categoría con paginación"""
        query = Download.filter(
            Download.site_id == site_id,
            Download.category == category
        )
        total = query.count()
        
        offset = (page - 1) * per_page
        downloads = query.options(joinedload(Download.site)).offset(offset).limit(per_page).all()
        
        return downloads, total

    def count_total(self) -> int:
        """Contar total de descargas"""
        return Download.query().count()

    def count_by_category(self, category: str) -> int:
        """Contar descargas por categoría"""
        return Download.filter(Download.category == category).count()

    def count_published(self) -> int:
        """Contar descargas publicadas"""
        return Download.filter(Download.published == True).count()

    def search(self, query: str, page: int = 1, per_page: int = 20) -> Tuple[List[Download], int]:
        """Buscar descargas por texto en provider, category o link"""
        search_query = Download.filter(
            (Download.provider.like(f"%{query}%")) |
            (Download.category.like(f"%{query}%")) |
            (Download.link.like(f"%{query}%"))
        )
        total = search_query.count()
        
        offset = (page - 1) * per_page
        downloads = search_query.options(joinedload(Download.site)).offset(offset).limit(per_page).all()
        
        return downloads, total

    def get_categories(self) -> List[str]:
        """Obtener lista única de categorías"""
        result = Download.query().distinct(Download.category).all()
        return [download.category for download in result]

    def get_providers(self) -> List[str]:
        """Obtener lista única de proveedores"""
        result = Download.query().distinct(Download.provider).all()
        return [download.provider for download in result]


def get_download() -> CRUDDownload:
    """Obtener una instancia del CRUDDownload"""
    """Esta función es útil para inyección de dependencias en FastAPI"""
    return CRUDDownload()