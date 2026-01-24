from pymongo.collection import Collection
from pymongo import AsyncMongoClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from typing import AsyncGenerator
from backend.core.config import settings

M_USER = settings.MONGO_USER
M_PASS = settings.MONGO_PASS
M_HOST = settings.MONGO_HOST
M_NAME = settings.MONGO_NAME

P_USER = settings.POSTGRES_USER
P_PASS = settings.POSTGRES_PASS
P_HOST = settings.POSTGRES_HOST
P_NAME = settings.POSTGRES_BASE

P_URL = f"postgresql+asyncpg://{P_USER}:{P_PASS}@{P_HOST}/{P_NAME}"
M_URL = f"mongodb://{M_USER}:{M_PASS}@{M_HOST}:27017"

_session = None
_AsyncSessionLocal = None

_engine = create_async_engine(
    P_URL,
    pool_size=20,
    max_overflow=10,
)

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    global _AsyncSessionLocal
    if _AsyncSessionLocal is None:
        _AsyncSessionLocal = async_sessionmaker(
            _engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
    async with _AsyncSessionLocal() as session:
        yield session

async def get_messages_collection() -> Collection:
    global _session
    if _session is None:
        _session = AsyncMongoClient(M_URL)
        _collection = _session[M_NAME]["messages"]
        
        await _collection.create_index([("chat_id", 1)], name="idx_chat_id")
        await _collection.create_index([("created_at", -1)], name="idx_created_at")

    return _session[M_NAME]["messages"]