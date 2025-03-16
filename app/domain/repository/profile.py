from abc import abstractmethod, ABC

from app.domain.dto.profile import ProfilePublic


class IProfile(ABC):
    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> ProfilePublic:
        raise NotImplementedError