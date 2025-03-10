import logging
from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.image import Image


class ImageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def upload_image(self, src: str, user_id: int, post_id: int) -> Image | None:
        if not src:
            logging.error('Upload failed: src is empty')
            raise HTTPException(status_code=400, detail="file is empty")

        image = Image(user_id=user_id,
                      post_id=post_id,
                      src=src
                      )
        self.db.add(image)
        try:
            await self.db.commit()
            await self.db.refresh(image)
            logging.info('Image is uploaded success')
            return image
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
            logging.warning(f'image with post_id={post_id} is not found')
            raise HTTPException(status_code=404, detail="image is not found")
        logging.info(f'images with post_id={post_id} is found')
        return list(images)