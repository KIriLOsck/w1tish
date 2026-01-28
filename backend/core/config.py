from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import datetime

class Settings(BaseSettings):
    REFRESH_TOKEN_MAX_AGE: int = 604800
    ACCESS_TOKEN_MAX_AGE: int = 900
    PASSWORD_ROUNGS: int = 12
    PASSWORD_PEPER: str = "spice_peper"

    COOKIE_SECURE: bool = False
    COOKIE_SAMESITE: str = "lax"

    POSTGRES_USER: str = "admin"
    POSTGRES_PASS: str = "admin"
    POSTGRES_HOST: str = "database"
    POSTGRES_BASE: str = "users_db"

    MONGO_USER: str = "admin"
    MONGO_PASS: str = "admin"
    MONGO_HOST: str = "messagebase:27017"
    MONGO_NAME: str = "messages_db"
    MONGO_DISCONECT_TIMEOUT: int = 5

    LOGS_FILE: str = f"{datetime.now().strftime("%d-%m-%Y_%H:%M")}.log"

    JWT_SECRET: str = "iWjwGUtt-DUeNb_QU8Oypc4jUZJX_FQflzpDzQTF9vA="
    JWT_ALGORITHM: str = "HS256"

    BASE_AVATARS_URL: list[str] = [
        "https://cs15.pikabu.ru/post_img/2025/02/06/9/1738852265114233915.jpg",
        "https://cojo.ru/wp-content/uploads/2022/12/avatarka-1-3.webp",
        "https://img.freepik.com/free-photo/rendering-bee-anime-character_23-2150963632.jpg"
    ]

    WORKERS_COUNT: int = 8

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()