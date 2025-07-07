from sqlalchemy import Column, Integer, String, Boolean, Text, DECIMAL
from sqlalchemy.orm import validates
# Local Imports
from app.database import BaseSaveModel


class Download(BaseSaveModel):
    __tablename__ = 'downloads'
    
    __table_args__ = {
        'comment': 'Tabla de descargas del juego',
    }

    # Campos del modelo
    id = Column(Integer, primary_key=True, autoincrement=True, comment='ID único de la descarga')
    provider = Column(String(100), nullable=False, comment='Proveedor de la descarga (ej: Google Drive, Mega, etc.)')
    size = Column(DECIMAL(10, 2), nullable=False, comment='Peso de la descarga en MB')
    link = Column(Text, nullable=False, comment='URL del enlace de descarga')
    published = Column(Boolean, default=False, nullable=False, comment='Indica si la descarga ha sido publicada')
    category = Column(String(50), nullable=False, comment='Categoría de la descarga (ej: cliente, parches, herramientas)')

    def __repr__(self):
        return f"<Download(id={self.id}, provider='{self.provider}', category='{self.category}')>"
