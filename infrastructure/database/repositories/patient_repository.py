# infrastructure/database/repositories/patient_repository.py
# Patient CRUD ops

from typing import Optional, List
from bson import ObjectId
from datetime import datetime

from infrastructure.database.connection import get_db
from config.constants import Collections


class PatientRepository:
    """Patient collection ops"""

    def __init__(self):
        self.collection_name = Collections.PATIENTS

    @property
    def collection(self):
        return get_db()[self.collection_name]

    async def find_all(self, skip: int = 0, limit: int = 20) -> List[dict]:
        """Get all patients // paginated"""
        cursor = self.collection.find().skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    async def count_all(self) -> int:
        """Total patient count"""
        return await self.collection.count_documents({})

    async def find_by_patient_id(self, patient_id: str) -> Optional[dict]:
        """Find by external patient_id (P-101)"""
        return await self.collection.find_one({"patient_id": patient_id})

    async def find_by_id(self, doc_id: str) -> Optional[dict]:
        """Find by MongoDB ObjectId"""
        try:
            return await self.collection.find_one({"_id": ObjectId(doc_id)})
        except Exception:
            return None

    async def create(self, patient_data: dict) -> str:
        """Insert new patient // returns id"""
        result = await self.collection.insert_one(patient_data)
        return str(result.inserted_id)

    async def upsert_by_patient_id(self, patient_id: str, data: dict) -> str:
        """Update or create by patient_id // used when new data comes in"""
        data["last_update"] = datetime.utcnow()
        result = await self.collection.update_one(
            {"patient_id": patient_id},
            {"$set": data, "$setOnInsert": {"created_at": datetime.utcnow()}},
            upsert=True
        )
        if result.upserted_id:
            return str(result.upserted_id)
        # If updated, fetch the doc to return id
        doc = await self.find_by_patient_id(patient_id)
        return str(doc["_id"]) if doc else ""

    async def update_latest_vitals(
        self,
        patient_id: str,
        heart_rate: int,
        oxygen_level: int,
        body_temp: float,
        steps: int,
        status: str
    ):
        """Update patient's latest vitals + status"""
        await self.collection.update_one(
            {"patient_id": patient_id},
            {
                "$set": {
                    "last_heart_rate": heart_rate,
                    "last_oxygen_level": oxygen_level,
                    "last_body_temperature": body_temp,
                    "last_steps": steps,
                    "status": status,
                    "last_update": datetime.utcnow()
                }
            }
        )

    async def count_active(self) -> int:
        """Count patients with recent updates (monitored)"""
        return await self.collection.count_documents({"last_update": {"$ne": None}})


# Singleton
patient_repo = PatientRepository()
