from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship

from .base import Base
from .user import User


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(User.id), index=True)
    text_content = Column(String(1024), nullable=False)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    
    user = relationship("User", back_populates="comments", cascade="all, delete")

