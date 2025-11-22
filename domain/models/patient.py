# domain/models/patient.py
# Patient model + schemas

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PatientBase(BaseModel):
    """Base patient fields"""
    patient_id: str = Field(..., description="External ID like P-101")
    patient_name: str = Field(..., min_length=1, max_length=100)


class PatientCreate(PatientBase):
    """For creating new patient"""
    pass


class PatientInDB(PatientBase):
    """Full patient doc in MongoDB"""
    id: Optional[str] = Field(None, alias="_id")
    status: str = "OK"  # OK, ALERT, CRITICAL
    last_heart_rate: Optional[int] = None
    last_oxygen_level: Optional[int] = None
    last_body_temperature: Optional[float] = None
    last_steps: Optional[int] = None
    last_update: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True


class PatientResponse(PatientBase):
    """Patient in API responses"""
    id: Optional[str] = None
    status: str
    last_heart_rate: Optional[int] = None
    last_oxygen_level: Optional[int] = None
    last_body_temperature: Optional[float] = None
    last_steps: Optional[int] = None
    last_update: Optional[datetime] = None


class PatientListResponse(BaseModel):
    """Paginated patient list"""
    items: list[PatientResponse]
    total: int
    page: int = 1
    page_size: int = 20
