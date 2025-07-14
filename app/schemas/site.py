from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

from .image import Image
from .page import Page
from .download import Download

class SiteBase(BaseModel):
    """Base schema for Site with common fields"""
    name: str = Field(..., max_length=255, description="Nombre del sitio")
    slug: str = Field(..., max_length=100, description="Slug único del sitio")
    initial_level: str = Field(..., max_length=10, description="Nivel inicial")
    max_level: str = Field(..., max_length=10, description="Nivel máximo")
    rates: Optional[str] = Field(None, max_length=255, description="Configuración de rates")
    facebook_url: Optional[str] = Field(None, max_length=500, description="URL de Facebook")
    facebook_enable: bool = Field(default=False, description="Habilitar enlace de Facebook")
    footer_info: Optional[str] = Field(None, description="Información del footer")
    footer_menu_enable: bool = Field(default=False, description="Habilitar menú en footer")
    footer_info_enable: bool = Field(default=False, description="Habilitar información en footer")
    forum_url: Optional[str] = Field(None, max_length=500, description="URL del foro")
    last_online: bool = Field(default=False, description="Mostrar último online")
    is_active: bool = Field(default=True, description="Sitio activo")
    maintenance_mode: bool = Field(default=False, description="Modo mantenimiento")

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip()

    @field_validator('slug')
    @classmethod
    def slug_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('El slug no puede estar vacío')
        return v.strip()

    @field_validator('initial_level')
    @classmethod
    def initial_level_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('El nivel inicial no puede estar vacío')
        return v.strip()

    @field_validator('max_level')
    @classmethod
    def max_level_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('El nivel máximo no puede estar vacío')
        return v.strip()

    class Config:
        from_attributes = True


class SiteCreate(SiteBase):
    """Schema for creating a new site"""
    pass


class SiteUpdate(BaseModel):
    """Schema for updating site information"""
    name: Optional[str] = Field(None, max_length=255, description="Nombre del sitio")
    slug: Optional[str] = Field(None, max_length=100, description="Slug único del sitio")
    initial_level: Optional[str] = Field(None, max_length=10, description="Nivel inicial")
    max_level: Optional[str] = Field(None, max_length=10, description="Nivel máximo")
    rates: Optional[str] = Field(None, max_length=255, description="Configuración de rates")
    facebook_url: Optional[str] = Field(None, max_length=500, description="URL de Facebook")
    facebook_enable: Optional[bool] = Field(None, description="Habilitar enlace de Facebook")
    footer_info: Optional[str] = Field(None, description="Información del footer")
    footer_menu_enable: Optional[bool] = Field(None, description="Habilitar menú en footer")
    footer_info_enable: Optional[bool] = Field(None, description="Habilitar información en footer")
    forum_url: Optional[str] = Field(None, max_length=500, description="URL del foro")
    last_online: Optional[bool] = Field(None, description="Mostrar último online")
    is_active: Optional[bool] = Field(None, description="Sitio activo")
    maintenance_mode: Optional[bool] = Field(None, description="Modo mantenimiento")

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('El nombre no puede estar vacío')
        return v.strip() if v else v

    @field_validator('slug')
    @classmethod
    def slug_must_not_be_empty(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('El slug no puede estar vacío')
        return v.strip() if v else v

    @field_validator('initial_level')
    @classmethod
    def initial_level_must_not_be_empty(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('El nivel inicial no puede estar vacío')
        return v.strip() if v else v

    @field_validator('max_level')
    @classmethod
    def max_level_must_not_be_empty(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('El nivel máximo no puede estar vacío')
        return v.strip() if v else v


class SiteResponseDetailed(BaseModel):
    """Response schema for site operations"""
    id: int
    name: str
    slug: str
    initial_level: str
    max_level: str
    rates: Optional[str] = None
    facebook_url: Optional[str] = None
    facebook_enable: bool
    footer_info: Optional[str] = None
    footer_menu_enable: bool
    footer_info_enable: bool
    forum_url: Optional[str] = None
    last_online: bool
    is_active: bool
    maintenance_mode: bool

    images: List[Image] = []
    footer_menu: List[Page] = []
    downloads: List[Download] = []

    class Config:
        from_attributes = True


class SiteResponse(BaseModel):
    """Response schema for site operations"""
    id: int
    name: str
    slug: str
    initial_level: str
    max_level: str
    rates: Optional[str] = None
    facebook_url: Optional[str] = None
    facebook_enable: bool
    footer_info: Optional[str] = None
    footer_menu_enable: bool
    footer_info_enable: bool
    forum_url: Optional[str] = None
    last_online: bool
    is_active: bool
    maintenance_mode: bool

    class Config:
        from_attributes = True


class Site(SiteBase):
    """Complete site schema including ID"""
    id: int = Field(..., description="ID único del sitio")

    class Config:
        from_attributes = True


class SiteInDB(Site):
    """Site schema as stored in database"""
    pass


class PaginatedSiteResponse(BaseModel):
    response: List[SiteResponse]
    total: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_prev: bool
