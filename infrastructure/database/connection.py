from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
import logging

from config.settings import get_settings

# simple logger 
logger = logging.getLogger("health_monitoring.database")


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
    logger.info("Attempting to connect to MongoDB", extra={
        "database": settings.mongo_db,
        "event": "db_connect_start"
    })
    
    try:
        db_instance.client = AsyncIOMotorClient(settings.mongo_uri)
        db_instance.db = db_instance.client[settings.mongo_db]

        # Quick health check - if this fails, we know something's wrong
        await db_instance.client.admin.command("ping")
        
        logger.info("Successfully connected to MongoDB", extra={
            "database": settings.mongo_db,
            "event": "db_connect_success"
        })
    except Exception as e:
        logger.error("Failed to connect to MongoDB", extra={
            "database": settings.mongo_db,
            "error": str(e),
            "event": "db_connect_failed"
        }, exc_info=True)
        raise


async def close_db():
    """Close MongoDB connection
    """
    if db_instance.client:
        logger.info("Closing MongoDB connection", extra={"event": "db_disconnect_start"})
        db_instance.client.close()
        logger.info("MongoDB connection closed successfully", extra={"event": "db_disconnect_success"})
    else:
        logger.warning("No MongoDB connection to close", extra={"event": "db_disconnect_no_connection"})


def get_db() -> AsyncIOMotorDatabase:
    """
    This is what repositories and services call to get the database.
    Crashes if DB isn't initialized
    """
    if db_instance.db is None:
        raise RuntimeError("DB not initialized - did you forget to call connect_db?")
    return db_instance.db
