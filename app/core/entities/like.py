from dataclasses import dataclass


@dataclass
class Like:
    id: int
    user_id: int
    post_id: int