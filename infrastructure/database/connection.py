# infrastructure/database/connection.py
# MongoDB async connection via motor

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional

from config.settings import get_settings


class MongoDB:
    """Singleton-ish MongoDB connection manager"""
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None


db_instance = MongoDB()


async def connect_db():
    """Init connection // call on app startup"""
    settings = get_settings()
    db_instance.client = AsyncIOMotorClient(settings.mongo_uri)
    db_instance.db = db_instance.client[settings.mongo_db]

    # Quick ping to verify connection
    await db_instance.client.admin.command("ping")
    print(f"[DB] Connected to MongoDB: {settings.mongo_db}")


async def close_db():
    """Close connection // call on app shutdown"""
    if db_instance.client:
        db_instance.client.close()
        print("[DB] MongoDB connection closed")


def get_db() -> AsyncIOMotorDatabase:
    """Get db instance // use in deps"""
    if db_instance.db is None:
        raise RuntimeError("DB not initialized - call connect_db first")
    return db_instance.db
