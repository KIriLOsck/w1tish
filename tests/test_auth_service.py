from backend.utils.services import AuthServiceClass
from backend.models import RegisterRequestModel, AuthRequestModel, TokensResponse
from backend.errors import UserExistError, UserNotFoundError, InvalidTokenError, WrongPasswordError
import pytest

@pytest.fixture
def auth_service(session):
    service = AuthServiceClass(session)
    yield service

@pytest.mark.asyncio(loop_scope="session")
async def test_register_user(auth_service):
    request = RegisterRequestModel(username="Kirilosck", password="Kirilosck123", email="Kirilosck@w1tish.net")
    tokens = await auth_service.register_user(request)
    assert tokens.__class__ == TokensResponse

    with pytest.raises(UserExistError) as err:
        await auth_service.register_user(request)
    assert err.type == UserExistError

@pytest.mark.asyncio(loop_scope="session")
async def test_auth_user(auth_service):
    register_request = RegisterRequestModel(username="Kirilosck", password="Kirilosck123", email="Kirilosck@w1tish.net")
    await auth_service.register_user(register_request)

    auth_request = AuthRequestModel(username="Kirilosck", password="Kirilosck123")
    tokens = await auth_service.auth_user(auth_request)
    assert tokens.__class__ == TokensResponse

    auth_request.username = "Invalid nickname"
    with pytest.raises(UserNotFoundError) as err:
        await auth_service.auth_user(auth_request)
    assert err.type == UserNotFoundError

    auth_request.username = "Kirilosck"
    auth_request.password = "Invalid password"
    with pytest.raises(WrongPasswordError) as err:
        await auth_service.auth_user(auth_request)
    assert err.type == WrongPasswordError

@pytest.mark.asyncio(loop_scope="session")
async def test_update_token(auth_service):
    request = RegisterRequestModel(username="Kirilosck", password="Kirilosck123", email="Kirilosck@w1tish.net")
    tokens = await auth_service.register_user(request)

    tokens = await auth_service.update_auth_session(tokens.refresh_token)
    assert tokens.__class__ == TokensResponse

    with pytest.raises(InvalidTokenError) as err:
        await auth_service.update_auth_session("Invalid token")
    assert err.type == InvalidTokenError
