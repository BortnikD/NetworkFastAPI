from app.domain.exceptions.base import DomainError


class ChatDoesNotExist(DomainError):
    pass


class ChatAlreadyExists(DomainError):
    pass


class MessageDoesNotExist(DomainError):
    pass


class MessageCreateError(DomainError):
    pass


class MessageUpdateError(DomainError):
    pass


class MessageDeleteError(DomainError):
    pass