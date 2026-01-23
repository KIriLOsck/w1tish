from pydantic import BaseModel


# основные модели

class UserModel(BaseModel):
    id: int
    nickname: str
    avatar_url: str

class ChatModel(BaseModel):
    id: str
    members: list[UserModel]

class MessageModel(BaseModel):
    chat_id: str
    content: str
    sender: str


# модели запросов

class AuthRequestModel(BaseModel):
    username: str
    password: str

class RegisterRequestModel(AuthRequestModel):
    email: str

class CreateChatRequestModel(BaseModel):
    members_ids: list[int]

class GetMessagesRequestModel(BaseModel):
    chat_id: int
    limit: int = 50
    offset: int = 0

class SendMessagesRequestModel(BaseModel):
    messages: list[MessageModel]


# модели ответов

class AccessTokenResponse(BaseModel):
    access_token: str

class TokensResponse(AccessTokenResponse):
    refresh_token: str

class MessagesResponse(SendMessagesRequestModel):
    pass

class UserResponse(UserModel):
    chats: dict

class UsersResponse(BaseModel):
    users: list[UserModel]

