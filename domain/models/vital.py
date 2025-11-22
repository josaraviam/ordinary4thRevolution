# domain/models/vital.py
# Vital signs data + alerts

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class VitalDataInput(BaseModel):
    """Incoming vitals from Node-RED // matches their payload"""
    deviceId: str = Field(..., description="Patient/device ID like P-102")
    heartRate: int = Field(..., ge=0, le=300)
    oxygenLevel: int = Field(..., ge=0, le=100)
    bodyTemperature: float = Field(..., ge=30.0, le=45.0)
    steps: int = Field(..., ge=0)
    timestamp: datetime


class VitalInDB(BaseModel):
    """Vital reading stored in MongoDB"""
    id: Optional[str] = Field(None, alias="_id")
    patient_id: str  # normalized from deviceId
    heart_rate: int
    oxygen_level: int
    body_temperature: float
    steps: int
    timestamp: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True


class VitalResponse(BaseModel):
    """Single vital reading response"""
    id: Optional[str] = None
    patient_id: str
    heart_rate: int
    oxygen_level: int
    body_temperature: float
    steps: int
    timestamp: datetime


class VitalListResponse(BaseModel):
    """List of vital readings"""
    items: list[VitalResponse]
    total: int


# --- Alerts ---

class AlertBase(BaseModel):
    """Alert when thresholds exceeded"""
    patient_id: str
    metric: str  # heart_rate, oxygen_level, body_temperature
    type: str  # HIGH or LOW
    value: float
    threshold: float


class AlertInDB(AlertBase):
    """Alert in MongoDB"""
    id: Optional[str] = Field(None, alias="_id")
    alert_id: str  # friendly ID like ALT-001
    status: str = "ACTIVE"  # ACTIVE, ACKNOWLEDGED, RESOLVED
    created_at: datetime = Field(default_factory=datetime.utcnow)
    acknowledged_at: Optional[datetime] = None

    class Config:
        populate_by_name = True


class AlertResponse(AlertBase):
    """Alert API response"""
    id: Optional[str] = None
    alert_id: str
    status: str
    created_at: datetime
    acknowledged_at: Optional[datetime] = None


class AlertListResponse(BaseModel):
    """List of alerts"""
    items: list[AlertResponse]
    total: int


# --- Thresholds ---

class ThresholdSettings(BaseModel):
    """Configurable alert thresholds"""
    heart_rate_high: int = 120
    heart_rate_low: int = 50
    oxygen_level_low: int = 92
    body_temperature_high: float = 38.0
    body_temperature_low: float = 35.5
