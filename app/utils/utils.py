import uuid
from fastapi import UploadFile, HTTPException
from pathlib import Path
# local import UPLOAD_DIR
from app.config import UPLOAD_DIR

# Función para validar el tipo de imagen
def validate_image(file: UploadFile):
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400, 
            detail=f"Tipo de archivo no permitido. Tipos permitidos: {', '.join(allowed_types)}"
        )
    
    # Validar tamaño máximo (5MB)
    max_size = 5 * 1024 * 1024  # 5MB en bytes
    if file.size and file.size > max_size:
        raise HTTPException(
            status_code=400,
            detail="El archivo es demasiado grande. Tamaño máximo: 5MB"
        )

# Función para generar nombre único y guardar archivo
async def save_upload_file(file: UploadFile) -> tuple[str, str, int]:
    """
    Guarda el archivo en el filesystem y retorna:
    - filename: nombre único del archivo
    - file_path: ruta completa del archivo
    - file_size: tamaño del archivo
    - web_path: ruta accesible desde el navegador
    """
    # Generar nombre único manteniendo la extensión
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename
    web_path = f"/static/uploads/{unique_filename}"
    
    # Guardar archivo
    with open(file_path, "wb") as buffer:
        contents = await file.read()
        buffer.write(contents)
    
    return unique_filename, str(web_path), len(contents)
