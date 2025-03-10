from abc import abstractmethod, ABC

from app.core.dto.profile import ProfilePublic


class IProfile(ABC):
    @abstractmethod
    async def get_user_id(self, user_id: int) -> ProfilePublic:
        raise NotImplementedError