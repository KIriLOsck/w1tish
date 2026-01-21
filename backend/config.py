from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    REFRESH_TOKEN_MAX_AGE: int = 604800
    COOKIE_SECURE: bool = False
    COOKIE_SAMESITE: str = "lax"

    JWT_SECRET: str = "iWjwGUtt-DUeNb_QU8Oypc4jUZJX_FQflzpDzQTF9vA="

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()