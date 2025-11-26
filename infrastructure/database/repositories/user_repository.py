from typing import Optional
from bson import ObjectId

from infrastructure.database.connection import get_db
from config.constants import Collections
from domain.models.user import UserInDB


class UserRepository:
    """User collection ops"""

    def __init__(self):
        self.collection_name = Collections.USERS

    @property
    def collection(self):
        return get_db()[self.collection_name]

    async def create(self, user_data: dict) -> str:
        """Insert user // returns inserted id"""
        result = await self.collection.insert_one(user_data)
        return str(result.inserted_id)

    async def find_by_username(self, username: str) -> Optional[dict]:
        """Find user by username // for login"""
        return await self.collection.find_one({"username": username})

    async def find_by_id(self, user_id: str) -> Optional[dict]:
        """Find user by ObjectId"""
        try:
            return await self.collection.find_one({"_id": ObjectId(user_id)})
        except Exception:
            return None

    async def username_exists(self, username: str) -> bool:
        """Check if username taken"""
        user = await self.collection.find_one({"username": username})
        return user is not None


# Singleton instance
user_repo = UserRepository()
