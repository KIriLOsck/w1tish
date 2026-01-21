from fastapi import APIRouter, status, Cookie, Response
from typing import Annotated

from backend.config import settings
from backend.utils.services import AuthService
from backend.models import (
    AuthRequestModel,
    RegisterRequestModel,
    AccessTokenResponse
)

def _set_refresh_cookie(response: Response, refresh_token) -> None:
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite=settings.COOKIE_SAMESITE,
            path="/auth/refresh",
            max_age=settings.REFRESH_TOKEN_MAX_AGE
        )

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/", response_model=AccessTokenResponse)
async def authenticate(
    auth_request: AuthRequestModel,
    auth_service: AuthService,
    response: Response
):  
    tokens = await auth_service.auth_user(auth_request)
    _set_refresh_cookie(response, tokens.refresh_token)

    return {
          "access_token": tokens.access_token
    }
    

@auth_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=AccessTokenResponse)
async def register(
    register_request: RegisterRequestModel,
    auth_service: AuthService,
    response: Response
): 
    tokens = await auth_service.register_user(register_request)
    _set_refresh_cookie(response, tokens.refresh_token)

    return {
          "access_token": tokens.access_token
    }
        

@auth_router.post("/refresh", response_model=AccessTokenResponse)
async def update_token(
    auth_service: AuthService,
    response: Response,
    refresh_token: Annotated[str | None, Cookie()] = None
):  
    tokens = await auth_service.update_auth_session(refresh_token)
    _set_refresh_cookie(response, tokens.refresh_token)

    return {
          "access_token": tokens.access_token
    }