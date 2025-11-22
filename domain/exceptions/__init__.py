# domain/exceptions/__init__.py
# Export all custom exceptions

from domain.exceptions.custom_exceptions import (
    BaseAppException,
    AuthException,
    InvalidCredentialsError,
    UserNotFoundError,
    UserAlreadyExistsError,
    TokenExpiredError,
    InvalidTokenError,
    PatientException,
    PatientNotFoundError,
    AlertException,
    AlertNotFoundError,
    AlertAlreadyAcknowledgedError,
    ValidationException,
)

__all__ = [
    "BaseAppException",
    "AuthException",
    "InvalidCredentialsError",
    "UserNotFoundError",
    "UserAlreadyExistsError",
    "TokenExpiredError",
    "InvalidTokenError",
    "PatientException",
    "PatientNotFoundError",
    "AlertException",
    "AlertNotFoundError",
    "AlertAlreadyAcknowledgedError",
    "ValidationException",
]
