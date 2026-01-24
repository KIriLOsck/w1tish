from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String


# основные модели

class Base(AsyncAttrs, DeclarativeBase): ...

class UserModel(BaseModel):
    id: int
    nickname: str
    avatar_url: str

class ChatModel(BaseModel):
    id: str
    members: list[UserModel]

class MessageModel(BaseModel):
    chat_id: str
    content: str
    sender: str


# модели запросов

class AuthRequestModel(BaseModel):
    username: str
    password: str

class RegisterRequestModel(AuthRequestModel):
    email: str

class CreateChatRequestModel(BaseModel):
    members_ids: list[int]

class GetMessagesRequestModel(BaseModel):
    chat_id: int
    limit: int = 50
    offset: int = 0

class SendMessagesRequestModel(BaseModel):
    messages: list[MessageModel]


# модели ответов

class AccessTokenResponse(BaseModel):
    access_token: str

class TokensResponse(AccessTokenResponse):
    refresh_token: str

class MessagesResponse(SendMessagesRequestModel): ...

class CreateChatResponse(BaseModel):
    chat_id: str

class UserResponse(UserModel):
    chats: dict

class UsersResponse(BaseModel):
    users: list[UserModel]


# базы данных

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

