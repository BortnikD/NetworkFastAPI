from sqladmin import ModelView

from app.infrastructure.database.models import Comment, Image, Post


class CommentAdmin(ModelView, model=Comment):
    column_list = [
        Comment.id,
        Comment.user_id,
        Comment.post_id,
        Comment.text_content
    ]
    column_searchable_list = [
        Comment.id,
        Comment.user_id,
        Comment.post_id,
    ]
    column_sortable_list = [
        Comment.created_at,
        Comment.id,
        Comment.user_id,
        Comment.post_id,
    ]
    form_excluded_columns = [
        Comment.created_at,
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
    column_searchable_list = [
        Image.id,
        Image.user_id,
        Image.post_id,
    ]
    column_sortable_list = [
        Image.created_at
    ]
    form_excluded_columns = [
        Image.created_at,
    ]
    icon = 'fa-solid fa-image'
    category = 'posts'


class LikeAdmin(ModelView, model=Like):
    column_list = [
        Like.id,
        Like.user_id,
        Like.post_id,
    ]
    column_searchable_list = [
        Like.id,
        Like.user_id,
        Like.post_id,
    ]
    column_sortable_list = [
        Like.created_at
    ]
    form_excluded_columns = [
        Like.created_at
    ]
    category = 'posts'


class PostAdmin(ModelView, model=Post):
    column_list = [
        Post.id,
        Post.user_id,
        Post.text_content
    ]
    column_searchable_list = [
        Post.id,
        Post.user_id,
        Post.text_content
    ]
    column_sortable_list = [
        Post.created_at,
        Post.id,
        Post.user_id,
    ]
    form_excluded_columns = [
        Post.created_at,
        Post.updated_at
    ]
    category = 'posts'