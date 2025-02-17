from sqlalchemy import ForeignKey, Integer, TIMESTAMP, func, String, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

from .base import Base


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=True)
    text_content: Mapped[str] = mapped_column(String, default=None, nullable=True)
    is_repost: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user = relationship('User', back_populates='posts', cascade='all, delete')
    comments = relationship("Comment", back_populates="post", cascade='all, delete') 


