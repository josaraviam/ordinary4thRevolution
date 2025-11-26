
# Back to basics XD – defaults added again to avoid Pydantic blowing up on startup.

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Centralized application settings.
    - Works with local .env during development.
    - Automatically overrides values when using Azure App Settings.
    - Defaults included so the API never crashes if a variable is missing (XD).
    """
    app_name: str = "Smart Health Monitoring API"    # Overridden by APP_NAME
    app_version: str = "1.0.0"                       # Overridden by APP_VERSION
    debug: bool = False                              # DEBUG=true overrides this

    host: str = "0.0.0.0"   # HOST
    port: int = 8000        # PORT

    mongo_uri: str = "mongodb://localhost:27017"     # MONGO_URI
    mongo_db: str = "health_monitoring"              # MONGO_DB

    # These defaults only prevent startup crashes — Azure MUST override jwt_secret.
    jwt_secret: str = "sfcbdb0de9c3063651fb59d2fde96f98c58ace98236753df6969c04d9c771857566926de122c65865cc743fa3f51a202db69a670b10b9b918d54d0d128eb689a7"   # hOPE THis Helps
    jwt_algorithm: str = "HS256"                                # JWT_ALGORITHM
    jwt_expire_minutes: int = 60                                # JWT_EXPIRE_MINUTES

    # Default wildcard is intentional — avoids breaking WebSockets & Node-RED on deploy.
    cors_origins: str = "*"                                     # CORS_ORIGINS

    class Config:
        """
        Pydantic Settings configuration:
        - Automatically loads environment variables from `.env` (local only).
        - Azure App Settings override automatically due to BaseSettings behavior.
        """
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.
    Always use this instead of creating Settings() directly.
    """
    return Settings()
