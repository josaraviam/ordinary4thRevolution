# domain/services/__init__.py
# Export all services

from domain.services.auth_service import auth_service, AuthService
from domain.services.patient_service import patient_service, PatientService
from domain.services.vital_service import (
    vital_service, VitalService,
    alert_service, AlertService,
    report_service, ReportService,
)

__all__ = [
    "auth_service",
    "AuthService",
    "patient_service",
    "PatientService",
    "vital_service",
    "VitalService",
    "alert_service",
    "AlertService",
    "report_service",
    "ReportService",
]
