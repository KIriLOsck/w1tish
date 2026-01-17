from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (
    Column,
    Integer,
    String
)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class usersBase(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

class usersDataBase(Base):
    __tablename__ = "users_data"
    
    id = Column(Integer, nullable=False, primary_key=True, index=True)
    nickname = Column(String, nullable=False)
    avatar_url = Column(String, nullable=True)
    chats = Column(JSONB, nullable=True)


# -> pass & login (/auth) 200(новые токены) 422(виноват фронтэндер) 404(виноват пользователь) 500(виноват бэкэндер)
# -> access (/get_user_data) 200(данные пользователя) 401(токен устарел) 422(виноват фронтендер) 500(виноват бэкэндер)
# -> refresh (/update_token) 200(новые токены) 500(виноват бэкэндер)