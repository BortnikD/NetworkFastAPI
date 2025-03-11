from app.core.dto.image import CreateImage
from app.core.interfaces.image import IImage
from app.infrastructure.database.models.image import Image


class ImageService:
    def __init__(self, image_port: IImage):
        self.image_port = image_port

    async def upload(self, image: CreateImage) -> Image | None:
        return await self.image_port.upload(image)

    async def get_sources_by_post_id(self, post_id: int) -> list[Image] | None:
        return await self.image_port.get_sources_by_post_id(post_id)