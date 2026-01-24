from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import backend.errors as err

import logging
logger = logging.getLogger(__name__)

async def user_exist_handler(
    request: Request,
    exc: err.UserExistError
): return JSONResponse(
    status_code=status.HTTP_409_CONFLICT,
    content = {
        "detail": "User already exists"
    }
)


async def user_not_found_handler(
    request: Request,
    exc: err.UserNotFoundError
): return JSONResponse(
    status_code=status.HTTP_404_NOT_FOUND,
    content = {
        "detail": "User not exists"
    }
)

async def chat_not_found_handler(
    request: Request,
    exc: err.NoWritePermissionError
): return JSONResponse(
    status_code=status.HTTP_404_NOT_FOUND,
    content = {
        "detail": "Chat not exists"
    }
)


async def wrong_password_handler(
    request: Request,
    exc: err.WrongPasswordError
): return JSONResponse(
    status_code=status.HTTP_401_UNAUTHORIZED,
    content = {
        "delail": "Wrong password or login"
    }
)


async def invalid_token_handler(
    request: Request,
    exc: err.InvalidTokenError
): return JSONResponse(
    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    content = {
        "detail": "Invalid token"
    }
)


async def invalid_messages_handler(
    request: Request, 
    exc: err.InvalidMessagesError
): return JSONResponse(
    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    content = {
        "detail": "Invalid messages format"
    }
)


async def expired_token_handlers(
    request: Request,
    exc: err.ExpiredTokenError
): return JSONResponse(
    status_code=status.HTTP_401_UNAUTHORIZED,
    content = {
        "detail": "Token expired"
    }
)


async def no_write_permission_handlers(
    request: Request,
    exc: err.NoWritePermissionError
): ...


async def no_read_permission_handlers(
    request: Request,
    exc: err.NoReadPermissionError
): ...


HANDLERS = {
    err.UserExistError:         user_exist_handler,
    err.UserNotFoundError:      user_not_found_handler,
    err.ChatNotFoundError:      chat_not_found_handler,
    err.WrongPasswordError:     wrong_password_handler,
    err.InvalidTokenError:      invalid_token_handler,
    err.InvalidMessagesError:   invalid_messages_handler,
    err.ExpiredTokenError:      expired_token_handlers,
    err.NoWritePermissionError: no_write_permission_handlers,
    err.NoReadPermissionError:  no_read_permission_handlers
}

def setup_exception_handlers(app: FastAPI):
    for exc_class, handler in HANDLERS.items():
        app.add_exception_handler(exc_class, handler)

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Type: {type(exc).__name__}", exc_info=exc)
        return JSONResponse(
            status_code=500,
            content={"detail": f"Type: {type(exc).__name__}, Message: {str(exc)}"}
        )
