from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware

from errors import UserExistError, UserNotFoundError, WrongPasswordError, InvalidTokenError
from models import AuthRequest, RegisterRequest, ResponseData, RefreshTokens

from databases.data_base.auth_methods import register_new, auth_user
from databases.data_base.data_methods import get_user_data
from databases.data_base.engine import engine, get_async_db
from token_generator import create_tokens, refresh_tokens, validate_token, cipher



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # для тестирования разрешаем все источники
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/auth")
async def authentificate(auth_request: AuthRequest, db = Depends(get_async_db)):
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
        return await create_tokens(user.id)
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Iternal server error"
        )
    

@app.post("/register")
async def register(register_request: RegisterRequest, db = Depends(get_async_db)):
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
        return await create_tokens(user_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@app.post("/user/data")
async def get_user_data_by_token(token: ResponseData, db = Depends(get_async_db)):
    try:
        is_token_valid = await validate_token(token.token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Invalid access token"
        )
    if is_token_valid is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token expired"
        )
    else:
        return await get_user_data(is_token_valid, db)
        


@app.post("/update_token")
async def update_token(token: RefreshTokens):
    try:
        is_token_valid = await refresh_tokens(token.token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Invalid refresh token"
        )
    if is_token_valid is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired"
        )
    else:
        return await refresh_tokens(token.token)