# infrastructure/database/connection.py
# MongoDB connection handling - keeping it simple with Motor (async driver)
# database "gateway" - everything goes through here

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional

from config.settings import get_settings


class MongoDB:
    """Singleton-style MongoDB connection manager
    
    Keeps our database connection alive and shared across the app.
    Not a true singleton but close enough.
    """
    client: Optional[AsyncIOMotorClient] = None  # The MongoDB client
    db: Optional[AsyncIOMotorDatabase] = None    # Our specific database


# Global instance - everyone will use this
db_instance = MongoDB()


async def connect_db():
    """Initialize MongoDB connection 
    """
    settings = get_settings()
    db_instance.client = AsyncIOMotorClient(settings.mongo_uri)
    db_instance.db = db_instance.client[settings.mongo_db]

    # Quick health check - if this fails, we know something's wrong
    await db_instance.client.admin.command("ping")
    print(f"[DB] Connected to MongoDB: {settings.mongo_db} (we're good to go!)")


async def close_db():
    """Close MongoDB connection
    """
    if db_instance.client:
        db_instance.client.close()
        print("[DB] MongoDB connection closed (bye bye!)")


def get_db() -> AsyncIOMotorDatabase:
    """
    This is what repositories and services call to get the database.
    Crashes if DB isn't initialized
    """
    if db_instance.db is None:
        raise RuntimeError("DB not initialized - did you forget to call connect_db?")
    return db_instance.db
