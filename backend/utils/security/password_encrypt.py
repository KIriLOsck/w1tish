import bcrypt
import asyncio
from concurrent.futures import ThreadPoolExecutor
from backend.core.config import settings

class PasswordEncrypter:
    def __init__(self):
        self._executor = ThreadPoolExecutor(max_workers=settings.WORKERS_COUNT)

    def _encrypt_password_sync(self, password: str) -> str:
        password += settings.PASSWORD_PEPER
        return bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt(rounds=settings.PASSWORD_ROUNGS)
        ).decode('utf-8')

    def _validate_password_sync(self, password: str, hashed: str) -> bool:
        password += settings.PASSWORD_PEPER
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    async def encrypt_password(self, password: str) -> str:
        event_loop = asyncio.get_event_loop()
        hashed = await event_loop.run_in_executor(
            self._executor,
            self._encrypt_password_sync,
            password
        )
        return hashed

    async def validate_password(self, password: str, hashed: str) -> bool:
        event_loop = asyncio.get_event_loop()
        return await event_loop.run_in_executor(
            self._executor,
            self._validate_password_sync,
            password,
            hashed
        )