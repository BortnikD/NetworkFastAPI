from sqlalchemy import String, BIGINT, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

from .base import Base


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('users.id'), index=True)
    post_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('posts.id'), index=True)
    text_content: Mapped[str] = mapped_column(String(1024), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False, index=True)
    
    user = relationship("User", back_populates="comments", cascade="all, delete")
    post = relationship("Post", back_populates="comments", cascade="all, delete") 

    repr_cols = ("id", "user_id", "post_id", "text_content")  # Укажите поля, которые должны выводиться в __repr__
    repr_cols_num = 4  # Количество полей для вывода