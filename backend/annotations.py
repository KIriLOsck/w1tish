from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.databases.messages_base.engine import get_messages_collection
from pymongo.collection import Collection

from backend.databases.data_base.engine import get_async_db

Database = Annotated[AsyncSession, Depends(get_async_db)]
MessageBase = Annotated[Collection, Depends(get_messages_collection)]
