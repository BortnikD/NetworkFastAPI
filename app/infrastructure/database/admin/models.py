from sqladmin import Admin, ModelView

from app.infrastructure.database.models import *


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.username,
        User.email,
    ]
    icon = "fa-solid fa-user"
    category = "accounts"


class ChatAdmin(ModelView, model=Chat):
    column_list = [
        Chat.id,
        Chat.first_user_id,
        Chat.second_user_id
    ]
    icon = 'fa-solid fa-comment'
    category = 'chats'


class ChatMessageAdmin(ModelView, model=ChatMessage):
    column_list = [
        ChatMessage.id,
        ChatMessage.chat_id,
        ChatMessage.user_id,
        ChatMessage.text
    ]
    icon = 'fa-solid fa-comment'
    category = 'chats'


class CommentAdmin(ModelView, model=Comment):
    column_list = [
        Comment.id,
        Comment.user_id,
        Comment.post_id,
    ]
    icon = 'fa-solid fa-comment'
    category = 'posts'


class ImageAdmin(ModelView, model=Image):
    column_list = [
        Image.id,
        Image.user_id,
        Image.post_id,
        Image.src,
    ]
    icon = 'fa-solid fa-image'
    category = 'posts'


class LikeAdmin(ModelView, model=Like):
    column_list = [
        Like.id,
        Like.user_id,
        Like.post_id,
    ]
    category = 'posts'


class PostAdmin(ModelView, model=Post):
    column_list = [
        Post.id,
        Post.user_id,
        Post.text_content
    ]
    category = 'posts'


class SubscriptionAdmin(ModelView, model=Subscription):
    column_list = [
        Subscription.id,
        Subscription.follower_id,
        Subscription.followed_user_id,
    ]
    category = "accounts"


def setup_views(admin: Admin):
    admin.add_view(UserAdmin)
    admin.add_view(ChatAdmin)
    admin.add_view(ChatMessageAdmin)
    admin.add_view(CommentAdmin)
    admin.add_view(ImageAdmin)
    admin.add_view(LikeAdmin)
    admin.add_view(PostAdmin)
    admin.add_view(SubscriptionAdmin)
