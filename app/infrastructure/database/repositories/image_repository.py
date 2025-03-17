import logging

from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.dto.image import CreateImage
from app.domain.repositories.image import IImage
from app.domain.exceptions.image import (
    ImageIsEmptyError,
    ImageUploadError,
    ImageNotFoundError
)

from app.infrastructure.database.models.image import Image


class ImageRepository(IImage):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def upload(self, image: CreateImage) -> Image:
        if not image.src:
            logging.error("Upload failed: src is empty")
            raise ImageIsEmptyError("File is empty")

        db_image = Image(
            user_id=image.user_id,
            post_id=image.post_id,
            src=image.src
        )
        self.db.add(db_image)
        try:
            await self.db.commit()
            await self.db.refresh(db_image)
            logging.info("Image uploaded successfully")
            return db_image
        except IntegrityError as e:
            await self.db.rollback()
            logging.error(f"Integrity error: {str(e)}")
            raise ImageUploadError("Error uploading image")

    async def get_sources_by_post_id(self, post_id: int) -> list[Image] | None:
        result = await self.db.execute(select(Image).where(Image.post_id == post_id))
        images = result.scalars().all()
        if not images:
            logging.warning(f"Images with post_id={post_id} not found")
            raise ImageNotFoundError("Images not found")
        logging.info(f"Images with post_id={post_id} found")
        return list(images)