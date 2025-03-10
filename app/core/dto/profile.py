from app.core.dto.user import UserPublic


class ProfilePublic(UserPublic):
    followers_count: int
    followed_count: int