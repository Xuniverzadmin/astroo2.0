from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DEFAULT_TZ: str = "Asia/Kolkata"
    REDIS_URL: str | None = None

    model_config = {"env_file": ".env", "extra": "ignore"}

settings = Settings()
