from pydantic import BaseModel

class AuthRequestModel(BaseModel):
    username: str
    password: str

class RegisterRequestModel(BaseModel):
    username: str
    password: str
    email: str

class ChatCreateModel(BaseModel):
    members: list[int]

class GetUsersDataModel(BaseModel):
    users_ids: list[int]

class MessageModel(BaseModel):
    chat_id: str
    content: str

class AddMessagesModel(BaseModel):
    messages: list[MessageModel]

class AccessTokenResponse(BaseModel):
    access_token: str

class TokensResponse(BaseModel):
    access_token: str
    refresh_token: str