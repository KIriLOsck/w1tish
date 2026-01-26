from backend import models
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from backend.errors import UserNotFoundError, ChatNotFoundError

from logging import getLogger
logger = getLogger(__name__)

class ChatRepository:
    def __init__(self, db: AsyncSession): self.db = db
    
    async def get_user_chats(self, user_id: int) -> dict:
        querty = select(
            models.usersBase.chats
        ).where(models.usersBase.id == user_id)

        chats = await self.db.scalar(querty)
        if not chats:
            raise ChatNotFoundError()
        return chats

    async def add_chat(self, members_ids: int, permissions: dict) -> str:
        new_chat = models.chatsBase(
            members = permissions
        )
        self.db.add(new_chat)
        await self.db.commit()
        await self.db.refresh(new_chat)

        stmt = (
            update(models.usersBase)
            .where(models.usersBase.id.in_(members_ids))
            .values(
                chats = models.usersBase.chats.concat(
                    {
                        str(new_chat.id): {
                            "last_message": "_Чат создан_",
                            "ids": members_ids
                        }
                    }
        )))
        
        await self.db.execute(stmt) 
        await self.db.commit()
        return str(new_chat.id)
    

class DataRepository:
    def __init__(self, session: AsyncSession):
        self.db = session
    
    async def get_user_data(self, user_id: int) -> models.UserResponse:
        query = await self.db.execute(
            select(
                models.usersBase.id,
                models.usersBase.avatar_url,
                models.usersBase.nickname,
                models.usersBase.chats
            ).where(
                models.usersBase.id == user_id
            )
        )
        user_data = query.one_or_none()
        if user_data is None:
            raise UserNotFoundError()

        return models.UserResponse(
            id=user_data.id,
            nickname=user_data.nickname,
            avatar_url=user_data.avatar_url,
            chats=user_data.chats
        )
    
    async def get_users_by_ids(self, ids) -> models.UsersResponse:
        query = await self.db.execute(
            select(
                models.usersBase.nickname,
                models.usersBase.avatar_url,
                models.usersBase.id
            ).where(
                models.usersBase.id.in_(ids)
            )
        )
        
        users_data = query.mappings().all()
        if len(users_data) != len(set(ids)):
            logger.warning(f"Failed to get users data! Getted {len(users_data)}/{len(ids)}")
            raise UserNotFoundError()
        
        return models.UsersResponse.model_validate({"users":users_data})