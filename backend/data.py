from fastapi import APIRouter, Depends, status, Security, Query
from fastapi.security.api_key import APIKeyHeader

from backend.utils.services import DataService
from typing import Annotated
from backend.utils.token_generator import get_userid_by_token
from backend import models

api_key_header = APIKeyHeader(name="Access-Token", auto_error=True)
async def get_userid_from_header(token: str = Security(api_key_header)):
    return await get_userid_by_token(token)

UserID = Annotated[int, Depends(get_userid_from_header)]
UsersIDs = Annotated[list[int] | None, Query()]

data_router = APIRouter(prefix="/api/data", tags=["Data methods"])

@data_router.get("/user", response_model=models.UsersResponse)
async def get_user_data_by_id(
    data_service: DataService,
    id: UsersIDs
): return await data_service.get_users_data(id)


@data_router.get("/", response_model=models.UserResponse)
async def get_self_data(data_service: DataService, user_id: UserID):
    return await data_service.get_user_data(user_id)


@data_router.post(
    "/messages",
    status_code=status.HTTP_201_CREATED,
    response_description="Messages added successfully"
)
async def add_new_messages(
    request: models.SendMessagesRequestModel,
    data_service: DataService,
    user_id: UserID
): await data_service.add_messages(user_id, request)

@data_router.get("/messages", response_model=models.MessagesResponse)
async def get_messages(
    chat_id: str,
    data_service: DataService,
    user_id: UserID,
    offset: int = 0,
    limit: int = 50,
):
    messages = await data_service.get_messages(user_id, chat_id, offset, limit)
    return messages

@data_router.post("/chats", status_code=status.HTTP_201_CREATED)
async def create_new_chat(
    request: models.CreateChatRequestModel,
    data_service: DataService,
    user_id: UserID
):  
    chat_id = await data_service.add_chat(user_id, request)
    return {"chat_id": chat_id}


# TODO добавить доставку сообщений в реальном времени через WebSocket