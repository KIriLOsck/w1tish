import pytest
from time import sleep
from backend.utils.token_generator import generate_tokens, validate_token, refresh_tokens
from backend.errors import InvalidTokenError

@pytest.mark.asyncio
async def test_generate_token():
    tokens = generate_tokens(52)
    assert tokens.get("access_token") is not None
    assert tokens.get("refresh_token") is not None

@pytest.mark.asyncio
async def test_validate_token():
    user_id = 52
    tokens = generate_tokens(user_id, 1, 1)         # access time & refresh time in seconds
    assert await validate_token(tokens.get("access_token")) == user_id
    assert await validate_token(tokens.get("refresh_token")) == user_id

    sleep(1.1)

    assert await validate_token(tokens.get("access_token", "None")) is None
    assert await validate_token(tokens.get("refresh_token", "None")) is None
    
    with pytest.raises(InvalidTokenError) as err:
        await validate_token("Invalid token")

    assert err.type == InvalidTokenError

@pytest.mark.asyncio
async def test_refresh_tokens():
    user_id = 52
    tokens = generate_tokens(user_id)
    with pytest.raises(InvalidTokenError) as err:
        await refresh_tokens("Invalid token")

    assert err.type == InvalidTokenError

    new_tokens = await refresh_tokens(tokens.get("refresh_token"))
    assert await validate_token(new_tokens.get("access_token")) == user_id
    