import pytest
from time import sleep
from backend.utils.token_generator import generate_tokens, get_userid_by_token, refresh_tokens
from backend.errors import InvalidTokenError, ExpiredTokenError


@pytest.mark.asyncio
async def test_validate_token():
    user_id = 52
    tokens = generate_tokens(user_id, 1, 1)         # access time & refresh time in seconds

    assert await get_userid_by_token(tokens.access_token) == user_id
    assert await get_userid_by_token(tokens.refresh_token) == user_id

    sleep(1.2)

    with pytest.raises(ExpiredTokenError) as err:
        await get_userid_by_token(tokens.access_token)
    assert err.type == ExpiredTokenError
    
    with pytest.raises(ExpiredTokenError) as err:
        await get_userid_by_token(tokens.refresh_token)
    assert err.type == ExpiredTokenError
    
    with pytest.raises(InvalidTokenError) as err:
        await get_userid_by_token("Invalid token")
    assert err.type == InvalidTokenError

@pytest.mark.asyncio
async def test_refresh_tokens():
    user_id = 52
    tokens = generate_tokens(user_id)

    with pytest.raises(InvalidTokenError) as err:
        await refresh_tokens("Invalid token")
    assert err.type == InvalidTokenError

    new_tokens = await refresh_tokens(tokens.refresh_token)
    assert await get_userid_by_token(new_tokens.access_token) == user_id
    