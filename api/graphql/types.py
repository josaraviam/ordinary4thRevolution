import strawberry
from typing import Optional, List
from datetime import datetime


@strawberry.type
class PatientType:
    """Patient GraphQL type"""
    id: str
    name: str
    patient_id: str
    status: str
    heart_rate: Optional[int] = None
    oxygen_level: Optional[int] = None
    body_temperature: Optional[float] = None
    steps: Optional[int] = None
    last_update: Optional[datetime] = None


@strawberry.type
class VitalType:
    """Vital reading GraphQL type"""
    id: str
    patient_id: str
    heart_rate: int
    oxygen_level: int
    body_temperature: float
    steps: int
    timestamp: datetime


@strawberry.type
class AlertType:
    """Alert GraphQL type"""
    id: str
    alert_id: str
    patient_id: str
    metric: str
    type: str  # HIGH or LOW
    value: float
    threshold: float
    status: str
    created_at: datetime
    acknowledged_at: Optional[datetime] = None


@strawberry.type
class LiveVitalsType:
    """Live vitals for subscriptions"""
    id: str  # patient_id
    heart_rate: int
    oxygen_level: int
    body_temperature: float
    steps: int
    timestamp: datetime


@strawberry.type
class ThresholdType:
    """Threshold settings type"""
    heart_rate_high: int
    heart_rate_low: int
    oxygen_level_low: int
    body_temperature_high: float
    body_temperature_low: float


@strawberry.type
class KPIType:
    """Dashboard KPIs type"""
    patients_monitored: int
    active_alerts: int
    average_heart_rate: float
    window_minutes: int


@strawberry.type
class SummaryType:
    """Report summary type"""
    average_heart_rate: float
    minimum_oxygen_level: int
    alert_count: int
    window_minutes: int


# --- Input types ---

@strawberry.input
class ThresholdInput:
    """Input for updating thresholds"""
    heart_rate_high: int = 120
    heart_rate_low: int = 50
    oxygen_level_low: int = 92
    body_temperature_high: float = 38.0
    body_temperature_low: float = 35.5


@strawberry.input
class VitalDataInput:
    """Input for ingesting vital data"""
    device_id: str
    heart_rate: int
    oxygen_level: int
    body_temperature: float
    steps: int
    timestamp: datetime


# --- Response types ---

@strawberry.type
class IngestResponse:
    """Response after ingesting vital data"""
    status: str
    message: str
    patient_id: str
    patient_status: str


@strawberry.type
class AckResponse:
    """Response after acknowledging alert"""
    status: str
    message: str
    alert_id: str
