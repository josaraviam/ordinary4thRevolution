# domain/models/patient.py
# Patient data models - basically our patient schema definitions
# Using pydantic because it makes validation super easy

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PatientBase(BaseModel):
    """Base patient fields - the essentials every patient needs"""
    patient_id: str = Field(..., description="External ID like P-101 (easier than MongoDB ObjectId)")
    patient_name: str = Field(..., min_length=1, max_length=100)


class PatientCreate(PatientBase):
    """For creating new patients - just the basics for now"""
    pass  # Inherits everything from PatientBase


class PatientInDB(PatientBase):
    """Full patient document as stored in MongoDB
    
    This has all the fields including the health status and vitals.
    MongoDB likes to add _id, so we handle that with alias.
    """
    id: Optional[str] = Field(None, alias="_id")  # MongoDB ObjectId becomes 'id'
    status: str = "OK"  # OK, ALERT, CRITICAL (starts as OK obviously)
    last_heart_rate: Optional[int] = None         # Latest HR reading
    last_oxygen_level: Optional[int] = None       # Latest SpO2 
    last_body_temperature: Optional[float] = None # Latest temp
    last_steps: Optional[int] = None              # Step count (why not?)
    last_update: Optional[datetime] = None        # When we last got data
    created_at: datetime = Field(default_factory=datetime.utcnow)  # When patient was added

    class Config:
        populate_by_name = True  # Allows both 'id' and '_id'


class PatientResponse(PatientBase):
    """Patient data for API responses - what the frontend gets"""
    id: Optional[str] = None
    status: str
    last_heart_rate: Optional[int] = None
    last_oxygen_level: Optional[int] = None
    last_body_temperature: Optional[float] = None
    last_steps: Optional[int] = None
    last_update: Optional[datetime] = None


class PatientListResponse(BaseModel):
    """Paginated patient list - because nobody wants to load 1000 patients at once"""
    items: list[PatientResponse]  # The actual patients
    total: int                    # Total count in DB
    page: int = 1                # Current page
    page_size: int = 20          # Items per page
