from app.domain.exceptions.base import DomainError


class AlreadyLikedPost(DomainError):
    pass


class LikeDoesNotExist(DomainError):
    pass


class LikeDeleteError(DomainError):
    pass
