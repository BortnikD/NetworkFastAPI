from dataclasses import dataclass


@dataclass
class Post:
    id: int
    follower_id: int
    followed_user_id: int
