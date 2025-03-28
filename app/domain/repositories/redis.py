from abc import ABC, abstractmethod
from pydantic import BaseModel


class IRedis(ABC):
    @abstractmethod
    async def clear_cache(self, path: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_cache(self, path: str):
        raise NotImplementedError

    @abstractmethod
    async def set_cache(self, path: str, value: BaseModel) -> None:
        raise NotImplementedError
