from typing import Optional, List, Tuple
# Local Imports
from app.models.application import Pages
from app.schemas.page import PageCreate, PageUpdate


class CRUDPage:
    """CRUD para manejar las operaciones de páginas"""

    def get(self, id: int) -> Optional[Pages]:
        """Obtener una página por ID"""
        return Pages.filter(Pages.id == id).first()

    def get_by_slug(self, slug: str) -> Optional[Pages]:
        """Obtener una página por slug"""
        return Pages.filter(Pages.slug == slug).first()

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[Pages]:
        """Obtener múltiples páginas con paginación básica"""
        return Pages.query().offset(skip).limit(limit).all()

    def get_paginated(self, page: int = 1, per_page: int = 20) -> Tuple[List[Pages], int]:
        """Obtener páginas paginadas con información de total"""
        query = Pages.query().order_by(Pages.id.desc())
        total = query.count()
        
        offset = (page - 1) * per_page
        pages = query.offset(offset).limit(per_page).all()
        
        return pages, total

    def get_published(self, page: int = 1, per_page: int = 20) -> Tuple[List[Pages], int]:
        """Obtener solo las páginas publicadas con paginación"""
        query = Pages.filter(Pages.published == True).order_by(Pages.id.desc())
        total = query.count()
        
        offset = (page - 1) * per_page
        pages = query.offset(offset).limit(per_page).all()
        
        return pages, total

    def create(self, obj_in: PageCreate) -> Pages:
        """Crear una nueva página"""
        db_obj = Pages(
            slug=obj_in.slug,
            title=obj_in.title,
            content=obj_in.content,
            published=obj_in.published
        )
        return db_obj.save()

    def update(self, db_obj: Pages, obj_in: PageUpdate) -> Pages:
        """Actualizar una página existente"""
        update_data = obj_in.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        return db_obj.save()

    def delete(self, db_obj: Pages) -> None:
        """Eliminar una página"""
        db_obj.delete()

    def publish(self, db_obj: Pages) -> Pages:
        """Publicar una página (cambiar published a True)"""
        db_obj.published = True
        return db_obj.save()

    def unpublish(self, db_obj: Pages) -> Pages:
        """Despublicar una página (cambiar published a False)"""
        db_obj.published = False
        return db_obj.save()

    def count_total(self) -> int:
        """Contar total de páginas"""
        return Pages.query().count()

    def count_published(self) -> int:
        """Contar páginas publicadas"""
        return Pages.filter(Pages.published == True).count()

    def search(self, query: str, page: int = 1, per_page: int = 20) -> Tuple[List[Pages], int]:
        """Buscar páginas por texto en título, slug o contenido"""
        search_query = Pages.filter(
            (Pages.title.like(f"%{query}%")) |
            (Pages.slug.like(f"%{query}%")) |
            (Pages.content.like(f"%{query}%"))
        ).order_by(Pages.id.desc())
        total = search_query.count()
        
        offset = (page - 1) * per_page
        pages = search_query.offset(offset).limit(per_page).all()
        
        return pages, total

    def slug_exists(self, slug: str, exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe una página con el slug dado"""
        query = Pages.filter(Pages.slug == slug)
        if exclude_id:
            query = query.filter(Pages.id != exclude_id)
        return query.first() is not None


def get_page() -> CRUDPage:
    """Obtener una instancia del CRUDPage"""
    """Esta función es útil para inyección de dependencias en FastAPI"""
    return CRUDPage()