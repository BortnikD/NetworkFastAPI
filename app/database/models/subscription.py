from sqlalchemy import BIGINT, TIMESTAMP, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from .base import Base


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    follower_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('users.id'), index=True, nullable=False)
    followed_user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('users.id'), index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    
    # following = relationship('Subscription', back_populates='follower', cascade="all, delete", foreign_keys='Subscription.follower_id')
    # followers = relationship('Subscription', back_populates='followed_user', cascade="all, delete", foreign_keys='Subscription.followed_user_id')

    __table_args__ = (UniqueConstraint("follower_id", "followed_user_id", name='unique_subscription'),)