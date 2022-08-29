# from pydantic import BaseModel
from tkinter import CASCADE
from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship
from . database import Base
# for creating ORM Models from Base class

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('NOW()'))
    user_id = Column(Integer, ForeignKey(
        'users.id', ondelete=CASCADE), nullable=False)
    user_info = relationship('User')


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('NOW()'))


class Vote(Base):
    __tablename__ = "votes"
    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
