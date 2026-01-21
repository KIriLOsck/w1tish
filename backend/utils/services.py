from fastapi import Depends
from typing import Annotated

from backend.utils import token_generator
from backend.annotations import Database

from backend.models import RegisterRequestModel, AuthRequestModel, TokensResponse
from backend.databases.data_base import auth_methods

class AuthServiceClass:
    def __init__(self, db: Database):
        self.db = db
    
    async def auth_user(self, request: AuthRequestModel) -> TokensResponse:
        user_id = await auth_methods.auth_user(
            request.username,
            request.password,
            self.db
        )
        tokens = await token_generator.create_tokens(user_id)
        return tokens
    
    async def register_user(self, request: RegisterRequestModel) -> TokensResponse:
        user_id = await auth_methods.register_new(
            request.username,
            request.email,
            request.password,
            self.db
        )
        tokens = await token_generator.create_tokens(user_id)
        return tokens
    
    async def update_auth_session(self, token: str) -> TokensResponse:
        tokens = await token_generator.refresh_tokens(token)
        return tokens
    
AuthService = Annotated[AuthServiceClass, Depends()]