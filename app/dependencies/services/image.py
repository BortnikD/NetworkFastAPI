from fastapi import Depends

from app.services.core_services.image_service import ImageService
from app.infrastructure.database.repositories.image_repository import ImageRepository
from app.dependencies.db import get_db


def get_image_service(db=Depends(get_db)) -> ImageService:
    image_repo = ImageRepository(db)
    return ImageService(image_repo)