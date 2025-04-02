import logging

from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.image import Image as ImageEntity
from app.domain.dto.image import CreateImage
from app.domain.repositories.image import IImage
from app.domain.exceptions.image import (
    ImageIsEmptyError,
    ImageUploadError,
    ImageNotFoundError
)

from app.infrastructure.database.models.image import Image as ImageModel


class ImageRepository(IImage):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def upload(self, image: CreateImage) -> ImageEntity:
        if not image.src:
            logging.error("Upload failed: src is empty")
            raise ImageIsEmptyError("File is empty")

        db_image = ImageModel(
            user_id=image.user_id,
            post_id=image.post_id,
            src=image.src
        )
        self.db.add(db_image)
        try:
            await self.db.commit()
            await self.db.refresh(db_image)
            logging.info("Image uploaded successfully")
            return ImageEntity.model_validate(db_image)
        except IntegrityError as e:
            await self.db.rollback()
            logging.error(f"Integrity error: {str(e)}")
            raise ImageUploadError("Error uploading image")

    async def get_sources_by_post_id(self, post_id: int) -> list[ImageEntity]:
        result = await self.db.execute(select(ImageModel).where(ImageModel.post_id == post_id))
        db_images = result.scalars().all()
        if not db_images:
            logging.warning(f"Images with post_id={post_id} not found")
            raise ImageNotFoundError("Images not found")

        images = [ImageEntity.model_validate(db_image) for db_image in db_images]
        logging.info(f"Images with post_id={post_id} found")
        return images
