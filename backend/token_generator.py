from asyncio import get_running_loop
from functools import wraps, partial
from cryptography.fernet import Fernet
from os import getenv
from json import loads, dumps, JSONDecodeError
from errors import InvalidRefreshToken, InvalidAccessToken
from concurrent.futures import ProcessPoolExecutor
from datetime import now, timestamp

cipher = Fernet(getenv("JWT_SECRET", "supersecret"))

def move_to_process(func):
    _executor = ProcessPoolExecutor()
    @wraps(func)
    async def wrapper(*args, **kwargs):
        nonlocal _executor
        loop = get_running_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(_executor, pfunc)
    return wrapper

@move_to_process
def generate_tokens(userid: int) -> dict:
    raw_access_token = {
        "userid": userid,
        "expires_at": int(timestamp(now())) + 900 # 15 минут
    }
    access_token = cipher.encrypt(dumps(raw_access_token).encode())

    raw_refresh_token = {
        "userid": userid,
        "expires_at": int(timestamp(now())) + 604800 # 7 дней
    }
    refresh_token = cipher.encrypt(dumps(raw_refresh_token).encode())

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

@move_to_process
def refresh_tokens(refresh_token: str) -> dict | None:
    try:
        decrypted_token: dict = loads(cipher.decrypt(refresh_token))
    except JSONDecodeError:
        raise InvalidRefreshToken()
    
    raw_access_token = {
        "userid": decrypted_token.get("userid"),
        "expires_at": int(timestamp(now())) + 900 # 15 минут
    }
    access_token = cipher.encrypt(dumps(raw_access_token).encode())

    raw_refresh_token = {
        "userid": decrypted_token.get("userid"),
        "expires_at": int(timestamp(now())) + 604800 # 7 дней
    }
    refresh_token = cipher.encrypt(dumps(raw_refresh_token).encode())

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

@move_to_process
def validate_token(token: str) -> int | None:
    try:
        decrypted_token: dict = loads(cipher.decrypt(token))
    except JSONDecodeError:
        raise InvalidAccessToken()
    
    if decrypted_token.get("expires_at") < int(timestamp(now())):
        return None
    
    return decrypted_token.get("userid")