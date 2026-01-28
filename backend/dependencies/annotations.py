from typing import Annotated
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from pymongo.collection import Collection
from typing import AsyncGenerator

async def get_async_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    async with request.app.state.pg_session() as session:
        yield session

def get_messages_collection(request: Request) -> Collection:
    return request.app.state.mg_collection

Database = Annotated[AsyncSession, Depends(get_async_db)]
MessageBase = Annotated[Collection, Depends(get_messages_collection)]
