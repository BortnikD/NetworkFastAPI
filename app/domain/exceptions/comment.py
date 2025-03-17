from app.domain.exceptions.base import DomainError


class CommentDoesNotExist(DomainError):
    pass


class CommentCreateError(DomainError):
    pass


class CommentUpdateError(DomainError):
    pass


class CommentDeleteError(DomainError):
    pass