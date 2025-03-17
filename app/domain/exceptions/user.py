from app.domain.exceptions.base import DomainError


class UserDoesNotExist(DomainError):
    pass


class UserIsAlreadyExist(DomainError):
    pass


class UserCreateError(DomainError):
    pass
