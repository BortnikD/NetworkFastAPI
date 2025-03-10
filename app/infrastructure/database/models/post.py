from sqlalchemy import ForeignKey, BIGINT, TIMESTAMP, func, String, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

from .base import Base


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('users.id'), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False, index=True)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=True)
    text_content: Mapped[str] = mapped_column(String, nullable=True)
    is_repost: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user = relationship('User', back_populates='posts')
    likes = relationship('Like', back_populates='post', cascade='all, delete')
    comments = relationship("Comment", back_populates="post", cascade='all, delete')
    images = relationship('Image', back_populates='post', cascade='all, delete')


