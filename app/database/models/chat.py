from sqlalchemy import Column, BIGINT, ForeignKey, String, TIMESTAMP, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from .base import Base
from .user import User


class Chat(Base):
    __tablename__ = 'chat'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    first_user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('users.id', ondelete="CASCADE"), index=True)
    second_user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('users.id', ondelete="CASCADE"), index=True)

    # Указываем foreign_keys и устанавливаем связи
    first_user: Mapped["User"] = relationship("User", foreign_keys=[first_user_id],
                                              back_populates="chats_as_first_user")
    second_user: Mapped["User"] = relationship("User", foreign_keys=[second_user_id],
                                               back_populates="chats_as_second_user")

    messages: Mapped["ChatMessage"] = relationship("ChatMessage", back_populates="chat", cascade="all, delete")

    __table_args__ = (
        UniqueConstraint('first_user_id', 'second_user_id', name='unique_chat_users'),
    )


class  ChatMessage(Base):
    __tablename__ = 'chat_messages'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    chat_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('chat.id', ondelete="CASCADE"), index=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('users.id', ondelete="CASCADE"), index=True)
    text: Mapped[str] = mapped_column(String(2048))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), index=True)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), index=True)

    chat = relationship("Chat", back_populates="messages")
