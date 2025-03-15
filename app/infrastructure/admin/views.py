from sqladmin import Admin

from app.infrastructure.admin import (
    UserAdmin,
    ChatAdmin,
    ChatMessageAdmin,
    CommentAdmin,
    ImageAdmin,
    LikeAdmin,
    PostAdmin,
    SubscriptionAdmin,
)


def setup_views(admin: Admin) -> None:
    admin.add_view(UserAdmin)
    admin.add_view(ChatAdmin)
    admin.add_view(ChatMessageAdmin)
    admin.add_view(CommentAdmin)
    admin.add_view(ImageAdmin)
    admin.add_view(LikeAdmin)
    admin.add_view(PostAdmin)
    admin.add_view(SubscriptionAdmin)
