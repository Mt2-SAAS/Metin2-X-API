"""CRUD Operaciones para manejar la entidad Image"""
from typing import List, Tuple, Optional
from sqlalchemy.orm import joinedload
from sqlalchemy import or_, and_
from pathlib import Path
import os

from app.models.application import Image
from app.schemas.image import ImageCreate, ImageUpdate
from app.crud.site import get_site


class CRUDImage:
    """CRUD operations for Image model"""

    def get(self, image_id: int) -> Optional[Image]:
        """Get image by ID with site relationship"""
        return (Image.filter(Image.id == image_id)
                .options(joinedload(Image.site))
                .first())

    def get_by_filename(self, filename: str, site_id: Optional[str] = None) -> Optional[Image]:
        """Get image by filename, optionally filtered by site"""
        query = Image.filter(Image.filename == filename)
        if site_id:
            query = query.filter(Image.site_id == site_id)
        return query.first()

    def get_paginated(
            self,
            page: int = 1,
            per_page: int = 20
        ) -> Tuple[List[Image], int]:
        """Get paginated images with site relationship"""
        query = Image.query().order_by(Image.created_at.desc())

        total = query.count()
        offset = (page - 1) * per_page
        images = query.options(
            joinedload(Image.site)
        ).offset(offset).limit(per_page).all()

        return images, total

    def get_by_site(
            self,
            site_id: str,
            page: int = 1,
            per_page: int = 20
        ) -> Tuple[List[Image], int]:
        """Get images filtered by site"""
        query = (Image.filter(Image.site_id == site_id)
                .order_by(Image.created_at.desc()))

        total = query.count()
        offset = (page - 1) * per_page
        images = query.options(
            joinedload(Image.site)
        ).offset(offset).limit(per_page).all()

        return images, total

    def get_by_type(
            self,
            image_type: str,
            page: int = 1,
            per_page: int = 20
        ) -> Tuple[List[Image], int]:
        """Get images filtered by type"""
        query = (Image.filter(Image.image_type == image_type)
                .order_by(Image.created_at.desc()))

        total = query.count()
        offset = (page - 1) * per_page
        images = query.options(
            joinedload(Image.site)
        ).offset(offset).limit(per_page).all()

        return images, total

    def get_all(self, page: int = 1, per_page: int = 20) -> Tuple[List[Image], int]:
        """Get all images with pagination"""
        query = Image.query().order_by(Image.created_at.desc())

        total = query.count()
        offset = (page - 1) * per_page
        images = query.options(joinedload(Image.site)).offset(offset).limit(per_page).all()

        return images, total

    def get_by_site_and_type(
            self,
            site_id: str,
            image_type: str,
            page: int = 1,
            per_page: int = 20
        ) -> Tuple[List[Image], int]:
        """Get images filtered by site and type"""
        query = (Image.filter(and_(
                    Image.site_id == site_id,
                    Image.image_type == image_type
                ))
                .order_by(Image.created_at.desc()))

        total = query.count()
        offset = (page - 1) * per_page
        images = query.options(
            joinedload(Image.site)
        ).offset(offset).limit(per_page).all()

        return images, total

    def search(
            self,
            search_term: str,
            page: int = 1,
            per_page: int = 20
        ) -> Tuple[List[Image], int]:
        """Search images by filename, original_filename, or file_path"""
        search_pattern = f"%{search_term}%"
        query = (Image.filter(or_(
                    Image.filename.ilike(search_pattern),
                    Image.original_filename.ilike(search_pattern),
                    Image.file_path.ilike(search_pattern)
                ))
                .order_by(Image.created_at.desc()))

        total = query.count()
        offset = (page - 1) * per_page
        images = query.options(joinedload(Image.site)).offset(offset).limit(per_page).all()

        return images, total

    def create(self, obj_in: ImageCreate) -> Image:
        """Create a new image"""
        # Verify that the site exists
        site_crud = get_site()
        if not site_crud.get(obj_in.site_id):
            raise ValueError(f"Site with ID {obj_in.site_id} does not exist")

        # Check if image filename already exists for this site
        existing_image = self.get_by_filename(obj_in.filename, obj_in.site_id)
        if existing_image:
            raise ValueError(f"Image with filename '{obj_in.filename}' already exists for this site")

        # Create new image
        db_obj = Image(
            filename=obj_in.filename,
            original_filename=obj_in.original_filename,
            file_path=obj_in.file_path,
            image_type=obj_in.image_type,
            file_size=obj_in.file_size,
            site_id=obj_in.site_id
        )
        db_obj.save()

        # Return with site relationship loaded
        return self.get(db_obj.id)

    def update(self, db_obj: Image, obj_in: ImageUpdate) -> Image:
        """Update an existing image metadata (not the file itself)"""
        update_data = obj_in.model_dump(exclude_unset=True)

        # If updating site_id, verify the site exists
        if "site_id" in update_data:
            site_crud = get_site()
            if not site_crud.get(update_data["site_id"]):
                raise ValueError(f"Site with ID {update_data['site_id']} does not exist")

        # Update fields
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db_obj.save()

        # Return with site relationship loaded
        return self.get(db_obj.id)

    def delete_file(self, db_obj: Image) -> None:
        """Delete the physical file from disk"""
        try:
            file_path = Path(db_obj.file_path)
            if file_path.exists():
                os.remove(file_path)
        except FileExistsError as e:
            # Log the error but don't fail the database deletion
            print(f"Warning: Could not delete file {db_obj.file_path}: {e}")

    def delete(self, db_obj: Image) -> None:
        """Delete an image and its file"""
        # Delete physical file first
        self.delete_file(db_obj)
        # Then delete from database
        db_obj.delete()

    def filename_exists(
            self,
            filename: str,
            site_id: str,
            exclude_id: Optional[int] = None
        ) -> bool:
        """Check if image filename exists for a specific site"""
        query = Image.filter(and_(
            Image.filename == filename,
            Image.site_id == site_id
        ))

        if exclude_id:
            query = query.filter(Image.id != exclude_id)

        return query.first() is not None


def get_image() -> CRUDImage:
    """Dependency to get Image CRUD instance"""
    return CRUDImage()
