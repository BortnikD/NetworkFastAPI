from sqlalchemy import String, Integer, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

from .base import Base
from .user import User


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), index=True)
    text_content: Mapped[str] = mapped_column(String(1024), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now(), nullable=False)
    
    user = relationship("User", back_populates="comments", cascade="all, delete")

