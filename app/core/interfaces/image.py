from abc import ABC, abstractmethod

from app.core.dto.image import CreateImage, Image


class IImage(ABC):
    @abstractmethod
    async def upload(self, image: CreateImage) -> Image:
        raise NotImplementedError

    @abstractmethod
    async def get_sources_by_post_id(self, post_id: int) -> list[Image] | None:
        raise NotImplementedError