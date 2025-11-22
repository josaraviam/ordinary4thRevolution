# infrastructure/database/repositories/vital_repository.py
# Vital readings + alerts CRUD

from typing import Optional, List
from bson import ObjectId
from datetime import datetime, timedelta
import uuid

from infrastructure.database.connection import get_db
from config.constants import Collections, AlertStatus


class VitalRepository:
    """Vital readings collection ops"""

    def __init__(self):
        self.collection_name = Collections.VITALS

    @property
    def collection(self):
        return get_db()[self.collection_name]

    async def create(self, vital_data: dict) -> str:
        """Insert vital reading"""
        result = await self.collection.insert_one(vital_data)
        return str(result.inserted_id)

    async def find_by_patient(
        self,
        patient_id: str,
        limit: int = 10,
        skip: int = 0
    ) -> List[dict]:
        """Get readings for a patient // newest first"""
        cursor = self.collection.find(
            {"patient_id": patient_id}
        ).sort("timestamp", -1).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    async def count_by_patient(self, patient_id: str) -> int:
        """Count readings for patient"""
        return await self.collection.count_documents({"patient_id": patient_id})

    async def get_avg_heart_rate(self, minutes: int = 5) -> Optional[float]:
        """Avg HR in last N minutes // for KPIs"""
        since = datetime.utcnow() - timedelta(minutes=minutes)
        pipeline = [
            {"$match": {"timestamp": {"$gte": since}}},
            {"$group": {"_id": None, "avg_hr": {"$avg": "$heart_rate"}}}
        ]
        result = await self.collection.aggregate(pipeline).to_list(1)
        if result:
            return round(result[0]["avg_hr"], 1)
        return None

    async def get_min_oxygen(self, minutes: int = 5) -> Optional[int]:
        """Min SpO2 in last N minutes"""
        since = datetime.utcnow() - timedelta(minutes=minutes)
        pipeline = [
            {"$match": {"timestamp": {"$gte": since}}},
            {"$group": {"_id": None, "min_o2": {"$min": "$oxygen_level"}}}
        ]
        result = await self.collection.aggregate(pipeline).to_list(1)
        if result:
            return result[0]["min_o2"]
        return None

    async def get_readings_in_window(
        self,
        minutes: int = 5,
        patient_id: Optional[str] = None
    ) -> List[dict]:
        """Get all readings in time window // for reports"""
        since = datetime.utcnow() - timedelta(minutes=minutes)
        query = {"timestamp": {"$gte": since}}
        if patient_id:
            query["patient_id"] = patient_id
        cursor = self.collection.find(query).sort("timestamp", -1)
        return await cursor.to_list(length=1000)  # cap at 1k


class AlertRepository:
    """Alerts collection ops"""

    def __init__(self):
        self.collection_name = Collections.ALERTS

    @property
    def collection(self):
        return get_db()[self.collection_name]

    async def create(self, alert_data: dict) -> str:
        """Insert new alert"""
        # Generate friendly alert_id
        alert_data["alert_id"] = f"ALT-{uuid.uuid4().hex[:8].upper()}"
        alert_data["created_at"] = datetime.utcnow()
        alert_data["status"] = AlertStatus.ACTIVE
        result = await self.collection.insert_one(alert_data)
        return str(result.inserted_id)

    async def find_active(self, skip: int = 0, limit: int = 50) -> List[dict]:
        """Get active alerts"""
        cursor = self.collection.find(
            {"status": AlertStatus.ACTIVE}
        ).sort("created_at", -1).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    async def count_active(self) -> int:
        """Count active alerts"""
        return await self.collection.count_documents({"status": AlertStatus.ACTIVE})

    async def find_by_status(
        self,
        status: str,
        skip: int = 0,
        limit: int = 50
    ) -> List[dict]:
        """Find alerts by status"""
        cursor = self.collection.find(
            {"status": status}
        ).sort("created_at", -1).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    async def acknowledge(self, alert_id: str) -> bool:
        """Mark alert as acknowledged // by alert_id"""
        result = await self.collection.update_one(
            {"alert_id": alert_id, "status": AlertStatus.ACTIVE},
            {
                "$set": {
                    "status": AlertStatus.ACKNOWLEDGED,
                    "acknowledged_at": datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0

    async def find_by_alert_id(self, alert_id: str) -> Optional[dict]:
        """Find alert by friendly alert_id"""
        return await self.collection.find_one({"alert_id": alert_id})

    async def count_in_window(self, minutes: int = 5) -> int:
        """Count alerts created in time window"""
        since = datetime.utcnow() - timedelta(minutes=minutes)
        return await self.collection.count_documents({"created_at": {"$gte": since}})


class SettingsRepository:
    """Settings/thresholds collection ops"""

    def __init__(self):
        self.collection_name = Collections.SETTINGS

    @property
    def collection(self):
        return get_db()[self.collection_name]

    async def get_thresholds(self) -> Optional[dict]:
        """Get current threshold settings"""
        return await self.collection.find_one({"type": "thresholds"})

    async def upsert_thresholds(self, thresholds: dict) -> bool:
        """Update or create thresholds"""
        result = await self.collection.update_one(
            {"type": "thresholds"},
            {"$set": {**thresholds, "updated_at": datetime.utcnow()}},
            upsert=True
        )
        return result.acknowledged


# Singletons
vital_repo = VitalRepository()
alert_repo = AlertRepository()
settings_repo = SettingsRepository()
