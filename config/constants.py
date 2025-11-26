# Alert thresholds (defaults)
DEFAULT_THRESHOLDS = {
    "heart_rate_high": 120,
    "heart_rate_low": 50,
    "oxygen_level_low": 92,
    "body_temperature_high": 38.0,
    "body_temperature_low": 35.5,
}

# Patient statuses
class PatientStatus:
    OK = "OK"
    ALERT = "ALERT"
    CRITICAL = "CRITICAL"

# Alert types
class AlertType:
    HIGH = "HIGH"
    LOW = "LOW"

# Alert statuses
class AlertStatus:
    ACTIVE = "ACTIVE"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    RESOLVED = "RESOLVED"

# Collection names for MongoDB
class Collections:
    USERS = "users"
    PATIENTS = "patients"
    VITALS = "vitals"
    ALERTS = "alerts"
    SETTINGS = "settings"
