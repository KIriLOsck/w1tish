from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from typing import AsyncGenerator
from os import getenv
from backend.config import settings

USER = settings.POSTRES_USER
PASSWORD = settings.POSTGRES_PASS
HOST = settings.POSTGRESS_HOST
NAME = settings.POSTGRESS_BASE_NAME

DATABASE_URL = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}/{NAME}"

_engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
)

_AsyncSessionLocal = async_sessionmaker(
    _engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with _AsyncSessionLocal() as session:
        yield session