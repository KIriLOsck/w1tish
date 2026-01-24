from fastapi import APIRouter, Depends, status, Security, Query
from fastapi.security import HTTPBearer

from backend.dependencies.dependencies import DataServiceDep
from typing import Annotated
from backend.utils.token_generator import get_id_by_jwt
from backend import models

http_bearer = HTTPBearer(auto_error=True)
def get_userid_from_bearer(token: str = Security(http_bearer)):
    return get_id_by_jwt(token.credentials)

CurrentUser = Annotated[int, Depends(get_userid_from_bearer)]
data_router = APIRouter(prefix="/api/data", tags=["Data methods"])

@data_router.get("/user", response_model=models.UsersResponse)
async def get_user_data_by_id(
    service: DataServiceDep,
    user_id: Annotated[list[int], Query(min_length=1)]
):
    return await service.get_users_data(user_id)


@data_router.get("/", response_model=models.UserResponse)
async def get_self_data(service: DataServiceDep, user_id: CurrentUser):
    return await service.get_user_data(user_id)


@data_router.post(
    "/messages",
    status_code=status.HTTP_201_CREATED
)
async def add_new_messages(
    request: models.SendMessagesRequestModel,
    service: DataServiceDep,
    user_id: CurrentUser
):
    await service.add_messages(user_id, request)

@data_router.get("/messages", response_model=models.MessagesResponse)
async def get_messages(
    service: DataServiceDep,
    user_id: CurrentUser,
    chat_id: str,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 50
):
    messages = await service.get_messages(user_id, chat_id, offset, limit)
    return messages

@data_router.post("/chats", status_code=status.HTTP_201_CREATED, response_model=models.CreateChatResponse)
async def create_new_chat(
    request: models.CreateChatRequestModel,
    service: DataServiceDep,
    user_id: CurrentUser
):  
    chat_id = await service.add_chat(user_id, request)
    return models.CreateChatResponse(chat_id=chat_id)


# TODO добавить доставку сообщений в реальном времени через WebSocket