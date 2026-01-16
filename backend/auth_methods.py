from databases.models import usersBase
from sqlalchemy.exc import IntegrityError
from hashlib import sha256
from errors import UserExistError

async def register_new(username: str, email: str, password: str, session) -> None:
    try:
        new_user = usersBase(
            username=username,
            email=email,
            password_hash=sha256(password.encode().hexdigest())
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
    
    except IntegrityError:
        await session.rollback()
        raise UserExistError()