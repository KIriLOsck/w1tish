from fastapi import FastAPI
from pymongo.collection import Collection
from pymongo import AsyncMongoClient, timeout
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from typing import AsyncGenerator
from backend.core.config import settings
from contextlib import asynccontextmanager

from logging import getLogger
logger = getLogger(__name__)

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

logger.debug("Creating postgres session...")

engine = create_async_engine(P_URL, pool_size=20, max_overflow=10)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
mongo_session: AsyncMongoClient = None

logger.debug("Created postgres session.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    global mongo_session

    logger.info("Creating mongo session & index...")

    mongo_session = AsyncMongoClient(M_URL, )
    collection = get_messages_collection()
        
    await collection.create_index([("chat_id", 1)], name="idx_chat_id")
    await collection.create_index([("created_at", -1)], name="idx_created_at")

    logger.info("Created index.")

    yield
    logger.info("Teardown db sessions...")
    await engine.dispose()
    with timeout(settings.MONGO_DISCONECT_TIMEOUT):
        await mongo_session.close()

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        logger.debug("Return new postgres session")
        yield session

def get_messages_collection() -> Collection:
    logger.debug("Return new mongo collection")
    return mongo_session[M_NAME]["messages"]