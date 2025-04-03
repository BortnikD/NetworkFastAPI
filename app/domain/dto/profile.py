from app.domain.entities.user import User


class ProfilePublic(User):
    followers_count: int
    followed_count: int
