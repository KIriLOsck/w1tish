from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column


# основные модели

class Base(AsyncAttrs, DeclarativeBase): ...

class UserModel(BaseModel):
    id: int
    username: str
    nickname: str
    avatar_url: str

class ChatModel(BaseModel):
    id: str
    members: list[UserModel]

class MessageModel(BaseModel):
    chat_id: str
    content: str
    sender: str
    created_at: str


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
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    avatar_url: Mapped[str] = mapped_column(nullable=True)
    nickname: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)

class chatsBase(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    last_message_text: Mapped[str] = mapped_column(server_default=text("'_Чат создан_'"))
    last_message_time: Mapped[datetime] = mapped_column(server_default=text("now()"))
    last_message_author: Mapped[int] = mapped_column(server_default=text("0"))
    permissions: Mapped[dict] = mapped_column(JSONB, server_default=text("'{}'::jsonb"))

