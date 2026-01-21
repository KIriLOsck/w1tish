from asyncio import get_running_loop
import jwt
from os import getenv
from backend.errors import InvalidTokenError, ExpiredTokenError
from concurrent.futures import ProcessPoolExecutor
from backend.models import TokensResponse
import datetime



secret = getenv("JWT_SECRET")
algorithm = "HS256"
_executor = ProcessPoolExecutor()


async def create_tokens(userid: int) -> TokensResponse:
    loop = get_running_loop()
    tokens = await loop.run_in_executor(
        _executor,
        generate_tokens,
        userid
    )
    return tokens


async def refresh_tokens(refresh_token: str) -> TokensResponse:
    loop = get_running_loop()
    decrypted_token = await loop.run_in_executor(
        _executor,
        decrypt_token,
        refresh_token
    )
    
    tokens = await loop.run_in_executor(
        _executor,
        generate_tokens,
        decrypted_token["id"]
    )
    return tokens


async def get_userid_by_token(token: str) -> int:
    loop = get_running_loop()
    decrypted_token = await loop.run_in_executor(
        _executor,
        decrypt_token,
        token
    )
    
    return decrypted_token["id"]


def generate_tokens(id: int, access_time: int = 900, refresh_time: int = 604800) -> TokensResponse:
    access_payload = {
        "id": id,
        "t": "a",
        "exp": datetime.timedelta(seconds=access_time) + datetime.datetime.now(datetime.timezone.utc)
    }

    refresh_payload = {
        "id": id,
        "t": "r",
        "exp": datetime.timedelta(seconds=refresh_time) + datetime.datetime.now(datetime.timezone.utc)
    }
    
    access_token = jwt.encode(access_payload, secret, algorithm)
    refresh_token = jwt.encode(refresh_payload, secret, algorithm)

    return TokensResponse(access_token=access_token, refresh_token=refresh_token)

def decrypt_token(token: str) -> dict:
    try:
        data = jwt.decode(token, secret, algorithms=[algorithm])
        return data
    except jwt.ExpiredSignatureError:
        raise ExpiredTokenError()
    except jwt.InvalidTokenError:
        raise InvalidTokenError()
