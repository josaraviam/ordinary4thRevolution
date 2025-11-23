# config/settings.py
# Global app config (all driven by .env)

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App info
    app_name: str            # From APP_NAME
    app_version: str         # From APP_VERSION
    debug: bool = False      # DEBUG=true/false

    # Server
    host: str                # HOST
    port: int                # PORT

    # MongoDB
    mongo_uri: str           # MONGO_URI
    mongo_db: str            # MONGO_DB

    # JWT auth
    jwt_secret: str          # JWT_SECRET
    jwt_algorithm: str       # JWT_ALGORITHM
    jwt_expire_minutes: int  # JWT_EXPIRE_MINUTES

    # CORS
    cors_origins: str        # CORS_ORIGINS (comma-separated)

    class Config:
        env_file = ".env"            # Load vars from .env
        env_file_encoding = "utf-8"  # Encoding


@lru_cache()
def get_settings() -> Settings:
    # Singleton-like cached settings
    return Settings()
