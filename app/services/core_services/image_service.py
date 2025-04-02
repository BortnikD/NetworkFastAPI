from app.domain.dto.image import CreateImage
from app.domain.entities.image import Image
from app.domain.repositories.image import IImage


class ImageService:
    def __init__(self, image_port: IImage):
        self.image_port = image_port

    async def upload(self, image: CreateImage) -> Image:
        return await self.image_port.upload(image)

    async def get_sources_by_post_id(self, post_id: int) -> list[Image]:
        return await self.image_port.get_sources_by_post_id(post_id)
