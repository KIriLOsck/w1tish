from pydantic import BaseModel

class AuthRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str
    email: str

class ResponseData(BaseModel):
    token: str