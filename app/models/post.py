# from sqlalchemy import  ForeignKey, Mapped, mapped_column, Integer, TIMESTAMP, func, String, Boolean
# from sqlalchemy.orm import relationship
# from datetime import datetime

# from .base import Base


# class Post(Base):
#     __tablename__ = 'posts'

#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
#     created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now(), nullable=False)
#     updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, update=func.now(), nullable=True)
#     text_content: Mapped[str] = mapped_column(String, default=None, nullable=True)
#     is_repost: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

#     user = relationship('User', back_populates='posts', cascade='all, delete')


from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship

from .base import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=func.now(), nullable=True)
    text_content = Column(String, nullable=True)
    is_repost = Column(Boolean, default=False, nullable=False)

    user = relationship("User", back_populates="posts")