# domain/models/__init__.py
# Model exports

from domain.models.user import (
    UserBase,
    UserCreate,
    UserLogin,
    UserInDB,
    UserResponse,
    TokenResponse,
)
from domain.models.patient import (
    PatientBase,
    PatientCreate,
    PatientInDB,
    PatientResponse,
    PatientListResponse,
)
from domain.models.vital import (
    VitalDataInput,
    VitalInDB,
    VitalResponse,
    VitalListResponse,
    AlertBase,
    AlertInDB,
    AlertResponse,
    AlertListResponse,
    ThresholdSettings,
)

__all__ = [
    # User
    "UserBase",
    "UserCreate",
    "UserLogin",
    "UserInDB",
    "UserResponse",
    "TokenResponse",
    # Patient
    "PatientBase",
    "PatientCreate",
    "PatientInDB",
    "PatientResponse",
    "PatientListResponse",
    # Vital
    "VitalDataInput",
    "VitalInDB",
    "VitalResponse",
    "VitalListResponse",
    "AlertBase",
    "AlertInDB",
    "AlertResponse",
    "AlertListResponse",
    "ThresholdSettings",
]
