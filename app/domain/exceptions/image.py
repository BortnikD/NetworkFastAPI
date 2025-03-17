from app.domain.exceptions.base import DomainError


class ImageIsEmptyError(DomainError):
    pass


class ImageUploadError(DomainError):
    pass

class ImageNotFoundError(DomainError):
    pass