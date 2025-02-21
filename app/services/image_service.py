from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.image import Image
from app.repositories.image_repository import ImageRepository


class ImageService:
    def __init__(self, db: AsyncSession):
        self.image_repository = ImageRepository(db)

    async def upload_image(self, src: str, user_id: int, post_id: int) -> Image | None:
        return await self.image_repository.upload_image(src, user_id, post_id)

    async def get_sources_by_post_id(self, post_id: int) -> list[Image] | None:
        return await self.image_repository.get_sources_by_post_id(post_id)