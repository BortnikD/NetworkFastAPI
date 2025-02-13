from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, func
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    first_name = Column(String(64), nullable=True)
    last_name = Column(String(64), nullable=True)
    is_active = Column(Boolean, default=False, nullable=False)
    date_joined = Column(TIMESTAMP, default=func.now(), nullable=False)
    last_active_time = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
    
    # comments = relationship("Comment", back_populates="user", cascade="all, delete")
    # posts = relationship("Post", back_populates="user", cascade="all, delete")
    # likes = relationship("Like", back_populates="user", cascade="all, delete")
