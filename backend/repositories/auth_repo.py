from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from hashlib import sha256
from random import choice as rand_choice

from backend.errors import UserExistError, UserNotFoundError, WrongPasswordError
from backend import models
from backend.core.config import settings

from logging import getLogger
logger = getLogger(__name__)


class AuthRepository:

    def __init__(self, db: AsyncSession): self.db = db

    async def register_new(
        self, 
        username: str,
        email: str,
        password: str
    ) -> int:
        try:
            logger.info("Try register new user...")

            new_user = models.usersBase(
                username=username,
                nickname=username,                                   # при регистрации ставим ник по умолчанию username
                email=email,
                password_hash=sha256(password.encode()).hexdigest(), # TODO реализовать алгоритм шифрования на Bcrypt
                avatar_url=rand_choice(settings.BASE_AVATARS_URL)
            )

            self.db.add(new_user)
            await self.db.commit()
            await self.db.refresh(new_user)

            logger.info(f"User {username} succesfully registred")

            return new_user.id
        
        except IntegrityError:

            logger.warning(f"User {username} already exist!")
            await self.db.rollback()
            raise UserExistError()


    async def check_user(self, username: str) -> models.usersBase:
        logger.info("Check user in db...")
        query = await self.db.execute(
            select(models.usersBase).where(
                models.usersBase.username == username
            )
        )
        user = query.scalar_one_or_none()
        if user is None:
            logger.warning(f"User {username} not exist!")
            raise UserNotFoundError()
        
        logger.info(f"User {username} exist")
        return user


    async def auth_user(self, username: str, password: str) -> int:
        user = await self.check_user(username)
        logger.info("Checking password...")

        if user.password_hash == sha256(password.encode()).hexdigest():          # TODO алгоритм шифрования
            return user.id
        
        logger.warning("Incorrect password")
        raise WrongPasswordError()
    