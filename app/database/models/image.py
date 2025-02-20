from sqlalchemy import BIGINT, ForeignKey, String, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from .base import Base


class Image(Base):
    __tablename__ = 'images'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('users.id'), index=True, nullable=False)
    post_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('posts.id'), index=True, nullable=False)
    src: Mapped[str] = mapped_column(String(512), index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    user = relationship('User', back_populates='images')
    post = relationship('Post', back_populates='images')