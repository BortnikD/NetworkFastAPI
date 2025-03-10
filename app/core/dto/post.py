from dataclasses import dataclass


@dataclass
class CreatePostDTO:
    user_id: int
    text_content: str
    is_repost: bool = False


@dataclass
class GetPostsDTO:
    user_id: int


@dataclass
class UpdatePostDTO:
    id: int
    text_content: str