from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from hashlib import sha256
from random import choice as rand_choice

from backend.errors import UserExistError, UserNotFoundError, WrongPasswordError
from backend.databases.data_base.models import usersBase
from backend.config import settings

class AuthRepository:

    def __init__(self, db: AsyncSession): self.db = db

    async def register_new(
        self, 
        username: str,
        email: str,
        password: str
    ) -> int:
        try:
            new_user = usersBase(
                username=username,
                nickname=username,              # при регистрации ставим по умолчанию
                email=email,
                password_hash=sha256(password.encode()).hexdigest(), # TODO реализовать алгоритм шифрования на Bcrypt
                avatar_url=rand_choice(settings.BASE_AVATARS_URL)
            )

            self.db.add(new_user)
            await self.db.commit()
            await self.db.refresh(new_user)
            return new_user.id
        
        except IntegrityError:
            await self.db.rollback()
            raise UserExistError()


    async def check_user(self, username: str) -> usersBase:
        query = await self.db.execute(
            select(usersBase).where(
                usersBase.username == username
            )
        )
        user = query.scalar_one_or_none()
        if user is None: raise UserNotFoundError()
        return user

    async def auth_user(self, username: str, password: str) -> int:
        user = await self.check_user(username)
        if user.password_hash == sha256(password.encode()).hexdigest(): # TODO алгоритм шифрования
            return user.id
        raise WrongPasswordError()