from fastapi import APIRouter, HTTPException, Depends, Response, status, Cookie
from backend.databases.data_base.engine import get_async_db
from backend.databases.data_base.auth_methods import register_new, auth_user
from backend.utils.token_generator import create_tokens, refresh_tokens
from typing import Annotated

from backend.models import (
    AuthRequest,
    RegisterRequest
)

from backend.errors import (
    UserExistError,
    UserNotFoundError,
    WrongPasswordError,
    InvalidTokenError,
    ExpiredTokenError
)

print("creating router...")
auth_router = APIRouter(prefix="/api")

@auth_router.post("/auth")
async def authentificate(auth_request: AuthRequest, response: Response, db = Depends(get_async_db)):
    try:
        user = await auth_user(auth_request.username, auth_request.password, db)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    except WrongPasswordError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong password or login"
        )
    if user:
        tokens = await create_tokens(user.id)
        response.set_cookie(
            key="refresh_token",
            value=tokens.get("refresh_token"),
            httponly=True,
            path="/api/refresh",
            max_age=604800 # 7 дней
        )
        return {"access_token": tokens.get("access_token")}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Iternal server error"
        )
    

@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(register_request: RegisterRequest, response: Response, db = Depends(get_async_db)):
    try:
        user_id = await register_new(
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
    
    if user_id:
        tokens = await create_tokens(user_id)
        response.set_cookie(
            key="refresh_token",
            value=tokens.get("refresh_token"),
            httponly=True,
            path="/api/refresh",
            max_age=604800 # 7 дней
        )
        return {"access_token": tokens.get("access_token")}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
        

@auth_router.post("/update_token")
async def update_token(response: Response, refresh_token: Annotated[str | None, Cookie()]):
    try:
        tokens = await refresh_tokens(refresh_token)
        response.set_cookie(
            key="refresh_token",
            value=tokens.get("refresh_token"),
            httponly=True,
            path="/api/refresh",
            max_age=604800 # 7 дней
        )
        return {"access_token": tokens.get("access_token")}
    
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Invalid refresh token"
        )
    except ExpiredTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired"
        )