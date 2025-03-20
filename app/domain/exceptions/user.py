from app.domain.exceptions.base import DomainError


class UserDoesNotExist(DomainError):
    pass


class UserAlreadyExists(DomainError):
    pass


class UserCreateError(DomainError):
    pass
