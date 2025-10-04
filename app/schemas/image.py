"""Esquemas para la gestión de imágenes usando Pydantic"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from enum import Enum

# Local import
# from .site import SiteResponse


class ImageType(str, Enum):
    """Enum for image types"""
    LOGO = "logo"
    BACKGROUND = "bg"


class ImageBase(BaseModel):
    """Base schema for Image with common fields"""
    filename: str = Field(..., max_length=255, description="Nombre único del archivo")
    original_filename: Optional[str] = Field(
        None,
        max_length=255,
        description="Nombre original del archivo"
    )
    file_path: str = Field(..., max_length=500, description="Ruta completa del archivo")
    image_type: ImageType = Field(..., description="Tipo de imagen (logo/bg)")
    file_size: Optional[int] = Field(None, description="Tamaño del archivo en bytes")
    site_id: str = Field(..., description="ID del sitio al que pertenece la imagen")

    @field_validator('filename')
    @classmethod
    def filename_must_not_be_empty(cls, v):
        """Validate that filename is not empty or just whitespace"""
        if not v or not v.strip():
            raise ValueError('El nombre del archivo no puede estar vacío')
        return v.strip()

    @field_validator('file_path')
    @classmethod
    def file_path_must_not_be_empty(cls, v):
        """Validate that file_path is not empty or just whitespace"""
        if not v or not v.strip():
            raise ValueError('La ruta del archivo no puede estar vacía')
        return v.strip()

    @field_validator('file_size')
    @classmethod
    def file_size_must_be_positive(cls, v):
        """Validate that file_size is positive if provided"""
        if v is not None and v < 0:
            raise ValueError('El tamaño del archivo debe ser positivo')
        return v

    class Config:
        """Pydantic configuration"""
        from_attributes = True


class ImageCreate(BaseModel):
    """Schema for creating a new image (used internally after file upload)"""
    filename: str = Field(..., max_length=255, description="Nombre único del archivo")
    original_filename: str = Field(..., max_length=255, description="Nombre original del archivo")
    file_path: str = Field(..., max_length=500, description="Ruta completa del archivo")
    image_type: ImageType = Field(..., description="Tipo de imagen (logo/bg)")
    file_size: int = Field(..., description="Tamaño del archivo en bytes")
    site_id: str = Field(..., description="ID del sitio al que pertenece la imagen")

    class Config:
        """Pydantic configuration"""
        from_attributes = True


class ImageUpdate(BaseModel):
    """Schema for updating image metadata (not for file replacement)"""
    original_filename: Optional[str] = Field(
        None,
        max_length=255,
        description="Nombre original del archivo"
    )
    image_type: Optional[ImageType] = Field(None, description="Tipo de imagen (logo/bg)")
    site_id: Optional[str] = Field(None, description="ID del sitio al que pertenece la imagen")

    @field_validator('original_filename')
    @classmethod
    def original_filename_must_not_be_empty(cls, v):
        """Validate that original_filename is not empty or just whitespace if provided"""
        if v is not None and (not v or not v.strip()):
            raise ValueError('El nombre original no puede estar vacío')
        return v.strip() if v else v


class ImageUploadRequest(BaseModel):
    """Schema for image upload request"""
    image_type: ImageType = Field(..., description="Tipo de imagen (logo/bg)")
    site_id: str = Field(..., description="ID del sitio al que pertenece la imagen")

    class Config:
        """Pydantic configuration"""
        from_attributes = True


class Image(ImageBase):
    """Complete image schema including ID"""
    id: int = Field(..., description="ID único de la imagen")

    class Config:
        """Pydantic configuration"""
        from_attributes = True


class ImageInDB(Image):
    """Image schema as stored in database"""


class ImageResponse(BaseModel):
    """Response schema for image operations"""
    id: int
    filename: str
    original_filename: Optional[str] = None
    file_path: str
    image_type: ImageType
    file_size: Optional[int] = None
    site_id: str

    class Config:
        """Pydantic configuration"""
        from_attributes = True


class PaginatedImageResponse(BaseModel):
    """Schema for paginated image responses"""
    response: List[ImageResponse]
    total: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_prev: bool
