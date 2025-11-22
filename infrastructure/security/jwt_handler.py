# infrastructure/security/jwt_handler.py
# JWT creation and verification

from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError

from config.settings import get_settings


def create_access_token(
    subject: str,
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create JWT token // subject is usually user_id"""
    settings = get_settings()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expire_minutes)

    payload = {
        "sub": subject,
        "exp": expire,
        "iat": datetime.utcnow()
    }

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm
    )


def decode_token(token: str) -> Optional[dict]:
    """Decode and verify JWT // returns payload or None"""
    settings = get_settings()

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )
        return payload
    except JWTError:
        return None


def get_token_expiry_seconds() -> int:
    """Get token expiry in seconds // for response"""
    settings = get_settings()
    return settings.jwt_expire_minutes * 60
