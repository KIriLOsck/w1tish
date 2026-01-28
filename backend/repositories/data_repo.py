from backend import models
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, cast, String, update
from backend.errors import UserNotFoundError, ChatNotFoundError
from contextlib import asynccontextmanager
from datetime import datetime
from typing import AsyncGenerator

from logging import getLogger
logger = getLogger(__name__)

class ChatRepository:
    def __init__(self, db: AsyncSession): self.db = db
    
    async def get_user_chats(self, user_id: int) -> list[int]:
        query = await self.db.execute(
            select(
                models.chatsBase.id
            ).where(
                models.chatsBase.permissions.has_key(cast(str(user_id), String))
            )
        )
        chats = query.scalars().all()
        if not chats:
            raise ChatNotFoundError()
        return chats

    async def add_chat(self, permissions: dict) -> str:
        new_chat = models.chatsBase(
            permissions = permissions
        )
        self.db.add(new_chat)
        await self.db.commit()
        await self.db.refresh(new_chat)

        return str(new_chat.id)
    
    @asynccontextmanager
    async def set_chat(self, message: models.MessageModel) -> AsyncGenerator[None, None]:
        try:
            await self.db.execute(
                update(
                    models.chatsBase
                ).where(
                    models.chatsBase.id == int(message.chat_id)
                ).values(
                    last_message_author = int(message.sender),
                    last_message_text = message.content,
                    last_message_time = datetime.fromisoformat(message.created_at)
                )
            )
            yield
            await self.db.commit()
        
        except:
            await self.db.rollback()
            raise
    

class DataRepository:
    def __init__(self, session: AsyncSession):
        self.db = session
    
    async def get_user_data(self, user_id: int) -> models.UserResponse:
        query = await self.db.execute(
            select(
                models.usersBase.id.label("user_id"),
                models.usersBase.username,
                models.usersBase.nickname,
                models.usersBase.avatar_url,
                models.chatsBase.id.label("chat_id"),
                models.chatsBase.last_message_author,
                models.chatsBase.last_message_text,
                models.chatsBase.last_message_time,
                models.chatsBase.permissions
            ).outerjoin(
                models.chatsBase,
                models.chatsBase.permissions.has_key(cast(str(user_id), String))
            ).where(
                models.usersBase.id == user_id
            )
        )
        user_data = query.all()

        if not user_data:
            raise UserNotFoundError()

        chats = {
            row.chat_id: {
                "last_message": row.last_message_text,
                "last_message_time": row.last_message_time,
                "last_message_author": row.last_message_author,
                "permissions": row.permissions
            }
            for row in user_data if row.chat_id is not None
        }

        response = models.UserResponse(
            id=user_data[0].user_id,
            username=user_data[0].username,
            nickname=user_data[0].nickname,
            avatar_url=user_data[0].avatar_url,
            chats=chats
        )

        return response
    
    async def get_users_by_ids(self, ids) -> models.UsersResponse:
        query = await self.db.execute(
            select(
                models.usersBase.nickname,
                models.usersBase.avatar_url,
                models.usersBase.id,
                models.usersBase.username
            ).where(
                models.usersBase.id.in_(ids)
            )
        )
        
        users_data = query.mappings().all()
        if len(users_data) != len(set(ids)):
            logger.warning(f"Failed to get users data! Getted {len(users_data)}/{len(ids)}")
            raise UserNotFoundError()
        
        return models.UsersResponse.model_validate({"users":users_data})