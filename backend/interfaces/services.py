from typing import Protocol
from backend import models

class IDataRepository(Protocol):

    async def get_user_data(self, user_id: int) -> models.UserResponse: ...

    async def get_users_by_ids(self, ids) -> models.UsersResponse: ...


class IChatRepository(Protocol):

    async def get_user_chats(self, user_id: int) -> dict: ...

    async def add_chat(self, members_ids: int, permissions: dict) -> str: ...


class IAuthRepository(Protocol):

    async def register_new(self, username: str, email: str, password: str) -> int: ...

    async def check_user(self, username: str) -> models.usersBase: ...

    async def auth_user(self, username: str, password: str) -> int: ...


class IMessagesRepository(Protocol):

    async def add_messages(self, messages: models.SendMessagesRequestModel) -> None: ...

    async def get_messages_by_chat(self, chat_id: str, limit: int, offset: int) -> models.MessagesResponse: ...