from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.databases.data_base.engine import get_async_db

Database = Annotated[AsyncSession, Depends(get_async_db)]
