"""Esquemas para la gestión de páginas usando Pydantic"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List


class PageBase(BaseModel):
    """Base esquema para la información de la página"""
    slug: str = Field(..., max_length=100, description="Slug único de la página")
    title: str = Field(..., max_length=100, description="Título de la página")
    content: str = Field(..., description="Contenido de la página")
    published: bool = Field(default=True, description="Indica si la página está publicada")
    site_id: str = Field(..., description="ID del sitio al que pertenece la página")

    @field_validator('slug')
    @classmethod
    def slug_must_not_be_empty(cls, v):
        """Valida que el slug no esté vacío y lo formatea"""
        if not v or not v.strip():
            raise ValueError('El slug no puede estar vacío')
        return v.strip().lower().replace(' ', '-')

    @field_validator('title')
    @classmethod
    def title_must_not_be_empty(cls, v):
        """Valida que el título no esté vacío"""
        if not v or not v.strip():
            raise ValueError('El título no puede estar vacío')
        return v.strip()

    @field_validator('content')
    @classmethod
    def content_must_not_be_empty(cls, v):
        """Valida que el contenido no esté vacío"""
        if not v or not v.strip():
            raise ValueError('El contenido no puede estar vacío')
        return v.strip()

    class Config:
        """Configura el modelo para permitir la creación desde atributos"""
        from_attributes = True


class PageCreate(PageBase):
    """Esquema para crear una nueva página"""


class PageUpdate(BaseModel):
    """Esquema para actualizar una página existente"""
    slug: Optional[str] = Field(None, max_length=100, description="Slug único de la página")
    title: Optional[str] = Field(None, max_length=100, description="Título de la página")
    content: Optional[str] = Field(None, description="Contenido de la página")
    published: Optional[bool] = Field(None, description="Indica si la página está publicada")
    site_id: Optional[str] = Field(None, description="ID del sitio al que pertenece la página")

    @field_validator('slug')
    @classmethod
    def slug_must_not_be_empty(cls, v):
        """Valida que el slug no esté vacío y lo formatea si se proporciona"""
        if v is not None and (not v or not v.strip()):
            raise ValueError('El slug no puede estar vacío')
        return v.strip().lower().replace(' ', '-') if v else v

    @field_validator('title')
    @classmethod
    def title_must_not_be_empty(cls, v):
        """Valida que el título no esté vacío si se proporciona"""
        if v is not None and (not v or not v.strip()):
            raise ValueError('El título no puede estar vacío')
        return v.strip() if v else v

    @field_validator('content')
    @classmethod
    def content_must_not_be_empty(cls, v):
        """Valida que el contenido no esté vacío si se proporciona"""
        if v is not None and (not v or not v.strip()):
            raise ValueError('El contenido no puede estar vacío')
        return v.strip() if v else v


class PagePublishUpdate(BaseModel):
    """Esquema para actualizar el estado de publicación de una página"""
    published: bool = Field(..., description="Estado de publicación de la página")


class Page(PageBase):
    """Esquema completo de la página incluyendo ID"""
    id: int = Field(..., description="ID único de la página")

    class Config:
        """Configura el modelo para permitir la creación desde atributos"""
        from_attributes = True


class PageInDB(Page):
    """Page esquema como se almacena en la base de datos"""


class PageResponse(BaseModel):
    """Respuesta esquema para las operaciones de página"""
    id: int
    slug: str
    title: str
    content: str
    published: bool
    site_id: str

    class Config:
        """Configura el modelo para permitir la creación desde atributos"""
        from_attributes = True


class PaginatedPageResponse(BaseModel):
    """Esquema para respuestas paginadas de páginas"""
    response: List[PageResponse]
    total: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_prev: bool
