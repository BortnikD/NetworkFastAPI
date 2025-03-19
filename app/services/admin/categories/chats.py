from sqladmin import ModelView

from app.infrastructure.database.models import Chat, ChatMessage


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
        ChatMessage.sender_id,
        ChatMessage.text
    ]
    column_searchable_list = [
        ChatMessage.id,
        ChatMessage.chat_id,
        ChatMessage.sender_id
    ]
    column_sortable_list = [
        ChatMessage.created_at,
        ChatMessage.chat_id,
        ChatMessage.sender_id
    ]
    form_excluded_columns = [
        ChatMessage.created_at,
        ChatMessage.updated_at
    ]
    icon = 'fa-solid fa-comment'
    category = 'chats'