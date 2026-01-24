from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pymongo.collection import Collection

from backend.core import engine

Database = Annotated[AsyncSession, Depends(engine.get_async_db)]
MessageBase = Annotated[Collection, Depends(engine.get_messages_collection)]
