from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, Table, Index, Enum
from sqlalchemy.orm import relationship
# Local Imports
from app.database import BaseSaveModel


# Enum para tipos de imagen (más robusto que strings)
class ImageType(PyEnum):
    LOGO = "logo"
    BACKGROUND = "bg"

# Tablas de asociación para relaciones ManyToMany
site_images = Table(
    'site_images',
    BaseSaveModel.metadata,
    Column('site_id', Integer, ForeignKey('sites.id', ondelete='CASCADE'), primary_key=True),
    Column('image_id', Integer, ForeignKey('images.id', ondelete='CASCADE'), primary_key=True),
    # Índice para optimizar consultas
    Index('idx_site_images_site_id', 'site_id'),
    Index('idx_site_images_image_id', 'image_id')
)


site_footer_menu = Table(
    'site_footer_menu',
    BaseSaveModel.metadata,
    Column('site_id', Integer, ForeignKey('sites.id', ondelete='CASCADE'), primary_key=True),
    Column('page_id', Integer, ForeignKey('pages.id', ondelete='CASCADE'), primary_key=True),
    Index('idx_site_footer_site_id', 'site_id'),
    Index('idx_site_footer_page_id', 'page_id')
)


class Download(BaseSaveModel):
    __tablename__ = 'downloads'
    
    __table_args__ = {
        'comment': 'Tabla de descargas del juego',
    }

    # Campos del modelo
    id = Column(Integer, primary_key=True, autoincrement=True, comment='ID único de la descarga')
    provider = Column(String(100), nullable=False, comment='Proveedor de la descarga (ej: Google Drive, Mega, etc.)')
    size = Column(String(100), nullable=False, comment='Peso de la descarga en MB')
    link = Column(Text, nullable=False, comment='URL del enlace de descarga')
    published = Column(Boolean, default=False, nullable=False, comment='Indica si la descarga ha sido publicada')
    category = Column(String(50), nullable=False, comment='Categoría de la descarga (ej: cliente, parches, herramientas)')

    # Relación con Site (muchas descargas pueden pertenecer a un sitio)
    site_id = Column(Integer, ForeignKey('sites.id', ondelete='CASCADE'), nullable=False, index=True)
    site = relationship("Site", back_populates="downloads")

    def __str__(self):
        return f"<Download ({self.link})>"
    
    def __repr__(self):
        return f"<Download(id={self.id}, provider='{self.provider}', category='{self.category}')>"


class Image(BaseSaveModel):
    __tablename__ = 'images'

    __table_args__ = {
        'comment': 'Tabla de images de la web',
    }
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    image_path = Column(String(500), nullable=False)  # Más espacio para rutas largas
    image_type = Column(Enum(ImageType), nullable=False, index=True)
    alt_text = Column(String(255))  # Para SEO y accesibilidad
    file_size = Column(Integer)  # Tamaño del archivo en bytes
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    
    # Relaciones
    sites = relationship("Site", secondary=site_images, back_populates="images")
    
    def __str__(self):
        return f"<Image ({self.name})>"
    
    def __repr__(self):
        return f"<Image(id={self.id}, name='{self.name}', type='{self.image_type.value}')>"



class Pages(BaseSaveModel):
    __tablename__ = 'pages'

    __table_args__ = {
        'comment': 'Tabla de paginas de la web',
    }
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(100), nullable=False)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    published = Column(Boolean, default=True, nullable=False)
    meta_description = Column(String(160))  # Para SEO
    meta_keywords = Column(String(255))  # Para SEO

    sites_footer = relationship("Site", secondary=site_footer_menu, back_populates="footer_menu")

    def __str__(self):
        return f"<Page ({self.title})>"

    def __repr__(self):
        return f"<Page(id={self.id}, title='{self.title}', slug='{self.slug}')>"


class Site(BaseSaveModel):
    __tablename__ = 'sites'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    
    # Configuración de niveles
    initial_level = Column(String(10), nullable=False)
    max_level = Column(String(10), nullable=False)
    rates = Column(String(255))
    
    # Configuración de redes sociales
    facebook_url = Column(String(500))  # URLs pueden ser largas
    facebook_enable = Column(Boolean, default=False, nullable=False)
    
    # Configuración de footer
    footer_info = Column(Text)  # Cambiar a Text para más flexibilidad
    footer_menu_enable = Column(Boolean, default=False, nullable=False)
    footer_info_enable = Column(Boolean, default=False, nullable=False)
    
    # Configuración adicional
    forum_url = Column(String(500))
    last_online = Column(Boolean, default=False, nullable=False)
    
    # Configuración general del sitio
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    maintenance_mode = Column(Boolean, default=False, nullable=False)
    
    # Relaciones
    images = relationship("Image", secondary=site_images, back_populates="sites")
    footer_menu = relationship("Pages", secondary=site_footer_menu, back_populates="sites_footer")
    downloads = relationship("Download", back_populates="site", cascade="all, delete-orphan")
    
    def __str__(self):
        return f"<Site ({self.name})>"
    
    def __repr__(self):
        return f"<Site(id={self.id}, name='{self.name}', slug='{self.slug}')>"


# Índices adicionales para optimizar consultas comunes
Index('idx_pages_published_slug', Pages.published, Pages.slug)
Index('idx_sites_active_slug', Site.is_active, Site.slug)
Index('idx_images_active_type', Image.is_active, Image.image_type)
Index('idx_downloads_site_published', Download.site_id, Download.published)
Index('idx_downloads_category_published', Download.category, Download.published)
