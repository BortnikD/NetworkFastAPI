from app.adapters.api.schemas.user import UserPublic


class ProfilePublic(UserPublic):
    followers_count: int
    followed_count: int