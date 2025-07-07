from pydantic import BaseModel, Field, validator
from typing import Optional, List


class DownloadBase(BaseModel):
    """Base schema for Download with common fields"""
    provider: str = Field(..., max_length=100, description="Proveedor de la descarga")
    size: float = Field(..., gt=0, description="Peso de la descarga en MB")
    link: str = Field(..., description="URL del enlace de descarga")
    category: str = Field(..., max_length=50, description="Categoría de la descarga")
    published: bool = Field(default=False, description="Indica si la descarga está publicada")

    @validator('provider')
    def provider_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('El proveedor no puede estar vacío')
        return v.strip()

    @validator('link')
    def link_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('El enlace no puede estar vacío')
        return v.strip()

    @validator('category')
    def category_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('La categoría no puede estar vacía')
        return v.strip()

    class Config:
        from_attributes = True


class DownloadCreate(DownloadBase):
    """Schema for creating a new download"""
    pass


class DownloadUpdate(BaseModel):
    """Schema for updating download information"""
    provider: Optional[str] = Field(None, max_length=100, description="Proveedor de la descarga")
    size: Optional[float] = Field(None, gt=0, description="Peso de la descarga en MB")
    link: Optional[str] = Field(None, description="URL del enlace de descarga")
    category: Optional[str] = Field(None, max_length=50, description="Categoría de la descarga")
    published: Optional[bool] = Field(None, description="Indica si la descarga está publicada")

    @validator('provider')
    def provider_must_not_be_empty(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('El proveedor no puede estar vacío')
        return v.strip() if v else v

    @validator('link')
    def link_must_not_be_empty(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('El enlace no puede estar vacío')
        return v.strip() if v else v

    @validator('category')
    def category_must_not_be_empty(cls, v):
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
        from_attributes = True


class DownloadInDB(Download):
    """Download schema as stored in database"""
    pass


class DownloadResponse(BaseModel):
    """Response schema for download operations"""
    id: int
    provider: str
    size: float
    link: str
    category: str
    published: bool

    class Config:
        from_attributes = True


class PaginatedDownloadResponse(BaseModel):
    response: List[DownloadResponse]
    total: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_prev: bool
