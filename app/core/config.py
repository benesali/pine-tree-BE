from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Require a sufficiently long secret for HMAC
    JWT_SECRET: str = Field(..., min_length=32)
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60
    DATABASE_URL: str


settings = Settings()
