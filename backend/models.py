from pydantic import BaseModel

class AuthRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str
    email: str

class ChatCreateModel(BaseModel):
    members: list[int]

class GetUsersDataModel(BaseModel):
    users_ids: list[int]