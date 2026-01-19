from fastapi import APIRouter, Depends, HTTPException, status

from backend.databases.messages_base.engine import get_messages_collection
from backend.databases.data_base.data_methods import get_user_data
from backend.databases.messages_base.methods import add_messages, get_messages_by_chat
from backend.databases.data_base.engine import get_async_db

from backend.utils.token_generator import get_userid_by_token
from backend.models import ResponseData
from backend.errors import InvalidMessagesError, InvalidTokenError, ExpiredTokenError


data_router = APIRouter(prefix="/data")

@data_router.post("/user")
async def get_user_data_by_token(token: ResponseData, db = Depends(get_async_db)):
    try:
        user_id = await get_userid_by_token(token.token)

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Invalid access token"
        )
    except ExpiredTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token expired"
        )
    else:
        return await get_user_data(user_id, db)


@data_router.post("/messages/add")  # TODO добавить аутентификацию
async def add_new_messages(messages: list[dict], collection = Depends(get_messages_collection)):
    try:
        await add_messages(messages, collection)
    except InvalidMessagesError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Invalid messages format"
        )
    return {"detail": "Messages added successfully"}

@data_router.get("/messages/{chat_id}") # TODO добавить аутентификацию
async def get_messages(
    chat_id: str,
    limit: int = 50,
    offset: int = 0,
    collection = Depends(get_messages_collection)
):
    messages = await get_messages_by_chat(chat_id, collection, limit, offset)
    return {"messages": messages}

# TODO добавить доставку сообщений в реальном времени через WebSocket