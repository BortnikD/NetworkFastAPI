from sqlalchemy import Column, BIGINT, ForeignKey, String, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from .base import Base


class Chat(Base):
    __tablename__ = 'chat'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    first_user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('user.id', ondelete="CASCADE"), index=True)
    second_user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('user.id', ondelete="CASCADE"), index=True)
    text: Mapped[str] = mapped_column(String(2048), nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), index=True)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), index=True)

    first_user: Mapped["User"] = relationship("User", foreign_keys=[first_user_id], back_populates="chats_as_first_user")
    second_user: Mapped["User"] = relationship("User", foreign_keys=[second_user_id], back_populates="chats_as_second_user")
