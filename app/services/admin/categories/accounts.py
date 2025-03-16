from sqladmin import ModelView

from app.infrastructure.database.models import User, Subscription


class UserAdmin(ModelView, model=User):
    can_create = False
    can_edit = False
    column_list = [
        User.id,
        User.username,
        User.email,
    ]
    column_searchable_list = [
        User.id,
        User.username,
        User.email,
    ]
    column_sortable_list = [
        User.date_joined
    ]
    icon = "fa-solid fa-user"
    category = "accounts"


class SubscriptionAdmin(ModelView, model=Subscription):
    column_list = [
        Subscription.id,
        Subscription.follower_id,
        Subscription.followed_user_id,
    ]
    column_searchable_list = [
        Subscription.id,
        Subscription.follower_id,
        Subscription.followed_user_id,
    ]
    column_sortable_list = [
        Subscription.created_at,
        Subscription.id,
        Subscription.follower_id,
        Subscription.followed_user_id,
    ]
    form_excluded_columns = [
        Subscription.created_at,
    ]
    category = "accounts"