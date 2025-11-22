# domain/exceptions/custom_exceptions.py
# Custom exceptions for business logic layer

class BaseAppException(Exception):
    """Base exception for all app errors"""
    def __init__(self, message: str, code: str = "APP_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


# --- Auth Exceptions ---

class AuthException(BaseAppException):
    """Base auth exception"""
    pass


class InvalidCredentialsError(AuthException):
    """Wrong username or password"""
    def __init__(self, message: str = "Invalid username or password"):
        super().__init__(message, "INVALID_CREDENTIALS")


class UserNotFoundError(AuthException):
    """User doesn't exist"""
    def __init__(self, message: str = "User not found"):
        super().__init__(message, "USER_NOT_FOUND")


class UserAlreadyExistsError(AuthException):
    """Username already taken"""
    def __init__(self, message: str = "Username already exists"):
        super().__init__(message, "USER_EXISTS")


class TokenExpiredError(AuthException):
    """JWT token expired"""
    def __init__(self, message: str = "Token has expired"):
        super().__init__(message, "TOKEN_EXPIRED")


class InvalidTokenError(AuthException):
    """Invalid JWT token"""
    def __init__(self, message: str = "Invalid token"):
        super().__init__(message, "INVALID_TOKEN")


# --- Patient Exceptions ---

class PatientException(BaseAppException):
    """Base patient exception"""
    pass


class PatientNotFoundError(PatientException):
    """Patient doesn't exist"""
    def __init__(self, patient_id: str):
        super().__init__(f"Patient {patient_id} not found", "PATIENT_NOT_FOUND")
        self.patient_id = patient_id


# --- Alert Exceptions ---

class AlertException(BaseAppException):
    """Base alert exception"""
    pass


class AlertNotFoundError(AlertException):
    """Alert doesn't exist"""
    def __init__(self, alert_id: str):
        super().__init__(f"Alert {alert_id} not found", "ALERT_NOT_FOUND")
        self.alert_id = alert_id


class AlertAlreadyAcknowledgedError(AlertException):
    """Alert already ack'd"""
    def __init__(self, alert_id: str):
        super().__init__(f"Alert {alert_id} already acknowledged", "ALERT_ALREADY_ACK")
        self.alert_id = alert_id


# --- Validation Exceptions ---

class ValidationException(BaseAppException):
    """Data validation error"""
    def __init__(self, message: str, field: str = None):
        super().__init__(message, "VALIDATION_ERROR")
        self.field = field
