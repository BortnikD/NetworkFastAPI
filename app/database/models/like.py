from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, TIMESTAMP, func, UniqueConstraint

from base import Base


class Like(Base):
    __tablename__ = 'likes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), index=True)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('posts.id'), index=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates='likes')
    post = relationship("Post", back_populates='likes')

    __table_args__ = (UniqueConstraint("user_id", "post_id", name='unique_like'),)