from app.domain.exceptions.base import DomainError


class SubscriptionAlreadyExists(DomainError):
    pass


class SubscriptionDoesNotExist(DomainError):
    pass


class SubscriptionDeleteError(DomainError):
    pass