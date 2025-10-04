"""Esquemas para la gestión de descargas usando Pydantic"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
# Local import
# from .site import SiteResponse


class DownloadBase(BaseModel):
    """Base schema for Download with common fields"""
    provider: str = Field(..., max_length=100, description="Proveedor de la descarga")
    size: str = Field(..., max_length=100, description="Peso de la descarga")
    link: str = Field(..., description="URL del enlace de descarga")
    category: str = Field(..., max_length=50, description="Categoría de la descarga")
    published: bool = Field(default=False, description="Indica si la descarga está publicada")
    site_id: str = Field(..., description="ID del sitio al que pertenece la descarga")

    @field_validator('provider')
    @classmethod
    def provider_must_not_be_empty(cls, v):
        """Ensure provider is not empty or just whitespace"""
        if not v or not v.strip():
            raise ValueError('El proveedor no puede estar vacío')
        return v.strip()

    @field_validator('link')
    @classmethod
    def link_must_not_be_empty(cls, v):
        """Ensure link is not empty or just whitespace"""
        if not v or not v.strip():
            raise ValueError('El enlace no puede estar vacío')
        return v.strip()

    @field_validator('category')
    @classmethod
    def category_must_not_be_empty(cls, v):
        """Ensure category is not empty or just whitespace"""
        if not v or not v.strip():
            raise ValueError('La categoría no puede estar vacía')
        return v.strip()

    class Config:
        """Pydantic configuration to allow ORM mode"""
        from_attributes = True


class DownloadCreate(DownloadBase):
    """Schema for creating a new download"""


class DownloadUpdate(BaseModel):
    """Schema for updating download information"""
    provider: Optional[str] = Field(None, max_length=100, description="Proveedor de la descarga")
    size: Optional[str] = Field(None, max_length=100, description="Peso de la descarga")
    link: Optional[str] = Field(None, description="URL del enlace de descarga")
    category: Optional[str] = Field(None, max_length=50, description="Categoría de la descarga")
    published: Optional[bool] = Field(None, description="Indica si la descarga está publicada")
    site_id: Optional[str] = Field(None, description="ID del sitio al que pertenece la descarga")

    @field_validator('provider')
    @classmethod
    def provider_must_not_be_empty(cls, v):
        """Ensure provider is not empty or just whitespace if provided"""
        if v is not None and (not v or not v.strip()):
            raise ValueError('El proveedor no puede estar vacío')
        return v.strip() if v else v

    @field_validator('link')
    @classmethod
    def link_must_not_be_empty(cls, v):
        """Ensure link is not empty or just whitespace if provided"""
        if v is not None and (not v or not v.strip()):
            raise ValueError('El enlace no puede estar vacío')
        return v.strip() if v else v

    @field_validator('category')
    @classmethod
    def category_must_not_be_empty(cls, v):
        """Ensure category is not empty or just whitespace if provided"""
        if v is not None and (not v or not v.strip()):
            raise ValueError('La categoría no puede estar vacía')
        return v.strip() if v else v


class DownloadPublishUpdate(BaseModel):
    """Schema for updating download publication status"""
    published: bool = Field(..., description="Estado de publicación de la descarga")


class Download(DownloadBase):
    """Complete download schema including ID"""
    id: int = Field(..., description="ID único de la descarga")

    class Config:
        """Pydantic configuration to allow ORM mode"""
        from_attributes = True


class DownloadInDB(Download):
    """Download schema as stored in database"""


class DownloadResponse(BaseModel):
    """Response schema for download operations"""
    id: int
    provider: str
    size: str
    link: str
    category: str
    published: bool
    site_id: str
    # site: Optional[SiteResponse] = None

    class Config:
        """Pydantic configuration to allow ORM mode"""
        from_attributes = True


class PaginatedDownloadResponse(BaseModel):
    """Schema for paginated download responses"""
    response: List[DownloadResponse]
    total: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_prev: bool
