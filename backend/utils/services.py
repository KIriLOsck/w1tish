from backend import models

from backend.utils import token_generator
from backend.dependencies.annotations import Database
from backend import errors as err

from backend.databases.data_base.data_methods import ChatRepository, DataRepository
from backend.databases.data_base.auth_methods import AuthRepository
from backend.databases.messages_base.chat_methods import MessagesRepository


class AuthService:
    def __init__(self, auth_repo: AuthRepository):
        self.auth_repo = auth_repo
    
    async def auth_user(self, request: models.AuthRequestModel) -> models.TokensResponse:
        user_id = await self.auth_repo.auth_user(
            request.username,
            request.password
        )
        tokens = await token_generator.create_tokens(user_id)
        return tokens
    
    async def register_user(self, request: models.RegisterRequestModel) -> models.TokensResponse:
        user_id = await self.auth_repo.register_new(
            request.username,
            request.email,
            request.password
        )
        tokens = await token_generator.create_tokens(user_id)
        return tokens
    
    async def update_auth_session(self, token: str) -> models.TokensResponse:
        tokens = await token_generator.refresh_tokens(token)
        return tokens


class DataService:
    def __init__(
        self,
        data_repo: DataRepository,
        chats_repo: ChatRepository,
        mess_repo: MessagesRepository
    ):
        self.user_data = data_repo
        self.user_chats = chats_repo
        self.user_messages = mess_repo

    async def add_messages(self, user_id: int, request: models.SendMessagesRequestModel) -> None:
        avarible_chats = await self.user_chats.get_user_chats(user_id)
        for message in request.messages:
            if message.chat_id not in avarible_chats:
                raise err.NoWritePermissionError(message)
            
        await self.user_messages.add_messages(request)

    async def add_chat(self, user_id: int, request: models.CreateChatRequestModel) -> str:
        permissions = {str(member): "user" for member in request.members_ids}
        permissions[str(user_id)] = "owner"

        chat_id = await self.user_chats.add_chat(
            request.members_ids,
            permissions
        )
        return chat_id

    async def get_messages(self, user_id: int, chat_id: str, offset: int, limit: int) -> models.MessagesResponse:
        avarible_chats = await self.user_chats.get_user_chats(user_id)
        if chat_id in avarible_chats:
            messages = await self.user_messages.get_messages_by_chat(
                chat_id,
                limit,
                offset
            )
            return messages
        raise err.NoReadPermissionError()

    async def get_user_data(self, user_id: int) -> models.UserResponse:
        data = await self.user_data.get_user_data(user_id)
        return data
    
    async def get_users_data(self, users_ids: list[int]) -> models.UsersResponse:
        data = await self.user_data.get_users_by_ids(users_ids)
        return data