from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from random import randint
from datetime import datetime

app = FastAPI()

class AuthRequest(BaseModel):
    username: str
    password: str

class DataResponse(BaseModel):
    token: str

class refreshTokens(BaseModel):
    refresh_token: str

@app.post("/auth")
async def authenticate(auth_request: AuthRequest):
    if auth_request.username == "testuser" and auth_request.password == "Testpass123":
        return {"access_token": f"access_token_{round(datetime.now().timestamp())}", "refresh_token": f"refresh_token_{randint(1000, 9999)}"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.post("/user/data")
async def get_user_data(token: DataResponse):
    if token.token.startswith("access_token_"):
        if int(token.token[-10:]) + 60 > round(datetime.now().timestamp()):
            return {"username": "PubertatUser3001", "avatar_url": "https://i.pinimg.com/originals/1b/76/e5/1b76e560086418af972c33ae6369b163.jpg"}
        else:
            raise HTTPException(status_code=401, detail="Token expired")
    else:
        raise HTTPException(status_code=422, detail="Invalid token format")

@app.post("/update_token")
async def update_token(token: refreshTokens):
    if token.refresh_token.startswith("refresh_token_"):
        return {"access_token": f"access_token_{round(datetime.now().timestamp())}", "refresh_token": f"refresh_token_{randint(1000, 9999)}"}
    else:
        raise HTTPException(status_code=422, detail="Invalid refresh token format")