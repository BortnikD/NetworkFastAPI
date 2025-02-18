from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BIGINT, ForeignKey, TIMESTAMP, func, UniqueConstraint

from base import Base


class Like(Base):
    __tablename__ = 'likes'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('users.id'), index=True)
    post_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('posts.id'), index=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates='likes')
    post = relationship("Post", back_populates='likes')

    __table_args__ = (UniqueConstraint("user_id", "post_id", name='unique_like'),)