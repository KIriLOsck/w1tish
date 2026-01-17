from databases.data_base.models import usersBase, usersDataBase
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from hashlib import sha256
from errors import UserExistError, UserNotFoundError, WrongPasswordError
from databases.data_base.data_methods import add_user_data

async def register_new(username: str, email: str, password: str, session) -> None:
    try:
        new_user = usersBase(
            username=username,
            email=email,
            password_hash=sha256(password.encode()).hexdigest()
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        await add_user_data(new_user.id, username, session)

        return new_user.id
    
    except IntegrityError:
        await session.rollback()
        raise UserExistError()


async def check_user(username: str, session) -> bool:
    query = await session.execute(
        select(usersBase).where(
            usersBase.username == username
        )
    )
    user = query.scalar_one_or_none()
    return user if user is not None else None

async def auth_user(username: str, password: str, session) -> bool:
    user = await check_user(username, session)
    if user is None:
        raise UserNotFoundError()
    if user.password_hash == sha256(password.encode()).hexdigest():
        return user
    raise WrongPasswordError()