from pydantic import BaseModel, Field, validator
from typing import Optional, List


class PageBase(BaseModel):
    """Base schema for Page with common fields"""
    slug: str = Field(..., max_length=100, description="Slug único de la página")
    title: str = Field(..., max_length=100, description="Título de la página")
    content: str = Field(..., description="Contenido de la página")
    published: bool = Field(default=True, description="Indica si la página está publicada")

    @validator('slug')
    def slug_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('El slug no puede estar vacío')
        return v.strip().lower().replace(' ', '-')

    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('El título no puede estar vacío')
        return v.strip()

    @validator('content')
    def content_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('El contenido no puede estar vacío')
        return v.strip()

    class Config:
        from_attributes = True


class PageCreate(PageBase):
    """Schema for creating a new page"""
    pass


class PageUpdate(BaseModel):
    """Schema for updating page information"""
    slug: Optional[str] = Field(None, max_length=100, description="Slug único de la página")
    title: Optional[str] = Field(None, max_length=100, description="Título de la página")
    content: Optional[str] = Field(None, description="Contenido de la página")
    published: Optional[bool] = Field(None, description="Indica si la página está publicada")

    @validator('slug')
    def slug_must_not_be_empty(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('El slug no puede estar vacío')
        return v.strip().lower().replace(' ', '-') if v else v

    @validator('title')
    def title_must_not_be_empty(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('El título no puede estar vacío')
        return v.strip() if v else v

    @validator('content')
    def content_must_not_be_empty(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('El contenido no puede estar vacío')
        return v.strip() if v else v


class PagePublishUpdate(BaseModel):
    """Schema for updating page publication status"""
    published: bool = Field(..., description="Estado de publicación de la página")


class Page(PageBase):
    """Complete page schema including ID"""
    id: int = Field(..., description="ID único de la página")

    class Config:
        from_attributes = True


class PageInDB(Page):
    """Page schema as stored in database"""
    pass


class PageResponse(BaseModel):
    """Response schema for page operations"""
    id: int
    slug: str
    title: str
    content: str
    published: bool

    class Config:
        from_attributes = True


class PaginatedPageResponse(BaseModel):
    response: List[PageResponse]
    total: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_prev: bool