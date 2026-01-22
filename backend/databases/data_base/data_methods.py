from backend.databases.data_base.models import usersDataBase, chatsBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from backend.errors import UserNotFoundError, UserExistError
from sqlalchemy.exc import IntegrityError
from backend.models import UsersResponse, UserResponse, ChatModel

async def get_user_data(user_id: int, session: AsyncSession) -> UserResponse:
    query = await session.execute(
        select(usersDataBase).where(
            usersDataBase.id == user_id
        )
    )
    user_data = query.scalar_one_or_none()
    if user_data is None:
        raise UserNotFoundError()

    return UserResponse(
        id=user_data.id,
        nickname=user_data.nickname,
        avatar_url=user_data.avatar_url,
        chats=user_data.chats
    )

async def add_user_data(user_id: int, username: str, session: AsyncSession) -> None:
    try:
        new_user_data = usersDataBase(
            id=user_id,
            nickname=username,
            avatar_url = "https://sneg.top/uploads/posts/2023-06/1688086311_sneg-top-p-ava-obichnaya-seraya-instagram-5.jpg"
        )
        session.add(new_user_data)
        await session.commit()
        await session.refresh(new_user_data)
    except IntegrityError:
        await session.rollback()
        raise UserExistError()
    
async def get_user_chats(user_id: int, session: AsyncSession) -> dict:
    querty = select(usersDataBase.chats).where(usersDataBase.id == user_id)
    return await session.scalar(querty)

async def add_chat(user_id: int, members_ids: int, session: AsyncSession) -> int:
    permissions = {str(member): "user" for member in members_ids}
    permissions[str(user_id)] = "owner"

    new_chat = chatsBase(
        members = permissions
    )
    session.add(new_chat)
    await session.commit()
    await session.refresh(new_chat)

    stmt = (
        update(usersDataBase)
        .where(usersDataBase.id == user_id)
        .values(
            chats = usersDataBase.chats.concat(
                {
                    str(new_chat.id): {
                        "last_message": "_Чат создан_",
                        "ids": members_ids
                    }
                }
    )))
    
    await session.execute(stmt) 
    await session.commit()
    
    return new_chat.id

async def get_users_data_by_ids(ids, session: AsyncSession):
    query = await session.execute(
        select(usersDataBase.nickname, usersDataBase.avatar_url, usersDataBase.id).where(
            usersDataBase.id.in_(ids)
        )
    )
    
    users_data = query.mappings().all()
    if len(users_data) != len(set(ids)):
        raise UserNotFoundError()
        
    return UsersResponse.model_validate({"users":users_data})