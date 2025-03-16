import logging
from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models.image import Image
from app.domain.dto.image import CreateImage
from app.domain.repository.image import IImage


class ImageRepository(IImage):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def upload(self, image: CreateImage) -> Image:
        if not image.src:
            logging.error("Upload failed: src is empty")
            raise HTTPException(status_code=400, detail="File is empty")

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
            raise HTTPException(status_code=400, detail="Error uploading image")
        except SQLAlchemyError as e:
            await self.db.rollback()
            logging.error(f"Database error: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    async def get_sources_by_post_id(self, post_id: int) -> list[Image] | None:
        result = await self.db.execute(select(Image).where(Image.post_id == post_id))
        images = result.scalars().all()
        if not images:
            logging.warning(f"Images with post_id={post_id} not found")
            raise HTTPException(status_code=404, detail="Images not found")
        logging.info(f"Images with post_id={post_id} found")
        return list(images)