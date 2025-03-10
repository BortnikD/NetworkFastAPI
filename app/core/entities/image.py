from dataclasses import dataclass


@dataclass
class Image:
    id: int
    user_id: int
    post_id: int
    src: str
