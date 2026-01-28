from fastapi import FastAPI
from pymongo import AsyncMongoClient, timeout
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
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
M_URL = f"mongodb://{M_USER}:{M_PASS}@{M_HOST}"

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Creating db sessions & index...")

    engine = create_async_engine(P_URL, pool_size=20, max_overflow=10)
    mongo_session = AsyncMongoClient(M_URL)

    app.state.pg_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    app.state.mg_collection = mongo_session[M_NAME]["messages"]
    
    await app.state.mg_collection.create_index([("chat_id", 1)], name="idx_chat_id")
    await app.state.mg_collection.create_index([("created_at", -1)], name="idx_created_at")

    logger.info("Created index.")

    yield
    logger.info("Teardown db sessions...")
    await engine.dispose()
    with timeout(settings.MONGO_DISCONECT_TIMEOUT):
        await mongo_session.close()