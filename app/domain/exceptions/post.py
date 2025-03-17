from app.domain.exceptions.base import DomainError


class PostCreateError(DomainError):
    pass


class PostDoesNotExist(DomainError):
    pass


class PostDeleteError(DomainError):
    pass


class PostUpdateError(DomainError):
    pass