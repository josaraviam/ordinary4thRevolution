# config/settings.py
# App settings via pydantic-settings // loads from .env

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App info
    app_name: str = "Smart Health Monitoring API"
    app_version: str = "1.0.0"
    debug: bool = False

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # MongoDB
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db: str = "health_monitoring"

    # JWT Config
    jwt_secret: str = "super-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    # CORS
    cors_origins: str = "*"  # comma-separated if multiple

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance // call this everywhere"""
    return Settings()
