from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security.api_key import APIKeyHeader

from backend.databases.messages_base.engine import get_messages_collection
from backend.databases.data_base.data_methods import get_user_data, add_chat, get_users_data_by_ids
from backend.databases.messages_base.methods import add_messages, get_messages_by_chat
from backend.databases.data_base.engine import get_async_db

from backend.utils.token_generator import get_userid_by_token
from backend.models import ChatCreateModel, GetUsersDataModel, AddMessagesModel
from backend.errors import (
    InvalidMessagesError,
    InvalidTokenError,
    ExpiredTokenError,
    NoReadPermissionError,
    NoWritePermissionError,
    UserNotFoundError
)

api_key_header = APIKeyHeader(name="Access-Token", auto_error=False)
async def get_userid_from_header(token: str = Security(api_key_header)):
    try:
        return await get_userid_by_token(token)
    
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Invalid token"
        )
    except ExpiredTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )

data_router = APIRouter(prefix="/data")

@data_router.post("/user/")
async def get_user_data_by_id(
    users: GetUsersDataModel,
    db = Depends(get_async_db)
):
    try:
        return await get_users_data_by_ids(users.users_ids, db)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
@data_router.get("/")
async def get_self_data(user_id = Depends(get_userid_from_header), db = Depends(get_async_db)):
    return await get_user_data(user_id, db)


@data_router.post("/messages/add", status_code=status.HTTP_201_CREATED)
async def add_new_messages(
    messages: AddMessagesModel,
    user_id = Depends(get_userid_from_header),
    session = Depends(get_async_db),
    collection = Depends(get_messages_collection)
):
    try:
        await add_messages(user_id, messages.messages, session, collection)
    except InvalidMessagesError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Invalid messages format"
        )
    except NoWritePermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Error chat: {e.error_message.get("chat_id")}"
        )
    return {"detail": "Messages added successfully"}

@data_router.get("/messages/{chat_id}")
async def get_messages(
    chat_id: str,
    limit: int = 50,
    offset: int = 0,
    user_id = Depends(get_userid_from_header),
    session = Depends(get_async_db),
    collection = Depends(get_messages_collection)
):
    try:
        messages = await get_messages_by_chat(user_id, chat_id, collection, session, limit, offset)
    except NoReadPermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User has no permission to read this"
        )
    return {"messages": messages}

@data_router.post("/chats/add", status_code=status.HTTP_201_CREATED)
async def create_new_chat(
    chat: ChatCreateModel,
    user_id = Depends(get_userid_from_header),
    session = Depends(get_async_db)
):  
    if len(chat.members) > 7 or len(chat.members) < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid members count. Allowed 1 - 7"
        )
    try:
        chat_id = await add_chat(user_id, chat.members, session)
        return {"chat_id": chat_id}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# TODO добавить доставку сообщений в реальном времени через WebSocket