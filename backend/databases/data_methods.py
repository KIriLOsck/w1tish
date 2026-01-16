from databases.models import usersDataBase
from sqlalchemy import select
from errors import UserNotFoundError
from sqlalchemy.exc import IntegrityError
from errors import UserExistError

async def get_user_data(user_id: int, session) -> usersDataBase:
    query = await session.execute(
        select(usersDataBase).where(
            usersDataBase.id == user_id
        )
    )
    user_data = query.scalar_one_or_none()
    if user_data is None:
        raise UserNotFoundError()
    return user_data

async def add_user_data(user_id: int, username: str, session) -> None:
    try:
        new_user_data = usersDataBase(
            id=user_id,
            username=username,
            avatar_url="https://sneg.top/uploads/posts/2023-06/1688086311_sneg-top-p-ava-obichnaya-seraya-instagram-5.jpg",
            chats=""
        )
        session.add(new_user_data)
        await session.commit()
        await session.refresh(new_user_data)
    except IntegrityError:
        await session.rollback()
        raise UserExistError()