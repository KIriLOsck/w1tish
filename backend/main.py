from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from errors import UserExistError
from models import AuthRequest, RegisterRequest, ResponseData, RefreshTokens

from auth_methods import register_new
from databases.engine import engine, get_async_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # для тестирования разрешаем все источники
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/auth")
async def authenticate(auth_request: AuthRequest):
    if auth_request.username == "testuser" and auth_request.password == "Testpass123":
        now_time = round(datetime.now().timestamp())
        return {
            "access_token": f"access_token_{now_time}",
            "refresh_token": f"refresh_token_{now_time}"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
@app.post("/register")
async def register(
        register_request: RegisterRequest, 
        db = Depends(get_async_db)
    ):
    try:
        await register_new(
            register_request.username,
            register_request.email,
            register_request.password,
            db
        )
    except UserExistError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )

@app.post("/user/data")
async def get_user_data(token: ResponseData):
    if token.token.startswith("access_token_"):
        if int(token.token[-10:]) + 60 > datetime.now().timestamp():
            return {
                "username": "PubertatUser3001",
                "avatar_url": "https://i.pinimg.com/originals/1b/76/e5/1b76e560086418af972c33ae6369b163.jpg"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Invalid token format"
        )

@app.post("/update_token")
async def update_token(token: RefreshTokens):
    if token.refresh_token.startswith("refresh_token_"):
        now_time = round(datetime.now().timestamp())
        if int(token.refresh_token[-10:]) + 120 > now_time:
            return {"access_token": f"access_token_{now_time}",
                    "refresh_token": f"refresh_token_{now_time}"
                }
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Invalid refresh token"
        )
    
