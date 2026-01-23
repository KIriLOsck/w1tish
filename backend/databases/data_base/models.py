from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (
    Column,
    Integer,
    String
)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class usersBase(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    avatar_url = Column(String, nullable=True)
    nickname = Column(String, nullable=False)
    chats = Column(JSONB, nullable=True)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

class chatsBase(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    members = Column(JSONB, nullable=True)