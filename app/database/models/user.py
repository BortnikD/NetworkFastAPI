from sqlalchemy import BIGINT, String, Boolean, TIMESTAMP, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

from .base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    first_name: Mapped[str] = mapped_column(String(64), nullable=True)
    last_name: Mapped[str] = mapped_column(String(64), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    date_joined: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)
    last_active_time: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now(),
                                                       nullable=False)

    comments = relationship("Comment", back_populates="user", cascade="all, delete")
    posts = relationship("Post", back_populates="user", cascade="all, delete")
    likes = relationship("Like", back_populates="user", cascade="all, delete")
    images = relationship('Image', back_populates='user', cascade="all, delete")
    # following = relationship('Subscription', back_populates='follower', cascade="all, delete")
    # followers = relationship('Subscription', back_populates='followed_user', cascade="all, delete")
    chats_as_first_user = relationship("Chat", back_populates="first_user", cascade="all, delete",
                                       foreign_keys="[Chat.first_user_id]")
    chats_as_second_user = relationship("Chat", back_populates="second_user", cascade="all, delete",
                                        foreign_keys="[Chat.second_user_id]")

    repr_cols = ("id", "username", "email", "date_joined")
    repr_cols_num = 3  