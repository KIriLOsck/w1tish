from fastapi import Depends
from typing import Annotated
from backend import models

from backend.utils import token_generator
from backend.annotations import Database, MessageBase

from backend.databases.data_base import data_methods
from backend.databases.data_base import auth_methods
from backend.databases.messages_base import methods


class AuthServiceClass:
    def __init__(self, db: Database):
        self.db = db
    
    async def auth_user(self, request: models.AuthRequestModel) -> models.TokensResponse:
        user_id = await auth_methods.auth_user(
            request.username,
            request.password,
            self.db
        )
        tokens = await token_generator.create_tokens(user_id)
        return tokens
    
    async def register_user(self, request: models.RegisterRequestModel) -> models.TokensResponse:
        user_id = await auth_methods.register_new(
            request.username,
            request.email,
            request.password,
            self.db
        )
        tokens = await token_generator.create_tokens(user_id)
        return tokens
    
    async def update_auth_session(self, token: str) -> models.TokensResponse:
        tokens = await token_generator.refresh_tokens(token)
        return tokens
    
AuthService = Annotated[AuthServiceClass, Depends()]


class DataServiceClass:
    def __init__(self, db: Database, mb: MessageBase):
        self.db = db
        self.mb = mb

    async def add_messages(self, user_id: int, request: models.SendMessagesRequestModel) -> None:
        await methods.add_messages(
            user_id,
            request,
            self.db,
            self.mb
        )

    async def add_chat(self, user_id: int, request: models.CreateChatRequestModel) -> int:
        chat_id = await data_methods.add_chat(
            user_id,
            request.members_ids,
            self.db
        )
        return chat_id

    async def get_messages(self, user_id: int, chat_id: str, offset: int, limit: int) -> models.MessagesResponse:
        messages = await methods.get_messages_by_chat(
            user_id,
            chat_id,
            self.mb,
            self.db,
            limit,
            offset
        )
        return messages

    async def get_user_data(self, user_id: int) -> models.UserResponse:
        data = await data_methods.get_user_data(user_id, self.db)
        return data
    
    async def get_users_data(self, users_ids: list[int]) -> models.UsersResponse:
        data = await data_methods.get_users_data_by_ids(users_ids, self.db)
        return data

DataService = Annotated[DataServiceClass, Depends()]