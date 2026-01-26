import jwt
from backend.errors import InvalidTokenError, ExpiredTokenError
from backend.models import TokensResponse
import datetime
from backend.core.config import settings

secret = settings.JWT_SECRET
algorithm = settings.JWT_ALGORITHM


def refresh_tokens(refresh_token: str) -> TokensResponse:
    decrypted_token = decrypt_token(refresh_token)
    if decrypted_token["t"] == "r":
        tokens = generate_tokens(decrypted_token["id"])
        return tokens
    raise InvalidTokenError


def get_id_by_jwt(token: str) -> int:
    decrypted_token = decrypt_token(token)
    return decrypted_token["id"]


def generate_tokens(
    id: int,
    access_time: int = settings.ACCESS_TOKEN_MAX_AGE,
    refresh_time: int = settings.REFRESH_TOKEN_MAX_AGE
) -> TokensResponse:
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
