from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    REFRESH_TOKEN_MAX_AGE: int = 604800
    COOKIE_SECURE: bool = False
    COOKIE_SAMESITE: str = "lax"

    POSTRES_USER: str = "admin"
    POSTGRES_PASS: str = "admin"
    POSTGRESS_HOST: str = "database"
    POSTGRESS_BASE_NAME: str = "users_db"

    JWT_SECRET: str = "iWjwGUtt-DUeNb_QU8Oypc4jUZJX_FQflzpDzQTF9vA="
    JWT_ALGORITHM: str = "HS256"

    BASE_AVATARS_URL: list[str] = [
        "https://cs15.pikabu.ru/post_img/2025/02/06/9/1738852265114233915.jpg",
        "https://cojo.ru/wp-content/uploads/2022/12/avatarka-1-3.webp",
        "https://img.freepik.com/free-photo/rendering-bee-anime-character_23-2150963632.jpg"
    ]

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()