# infrastructure/security/password_hasher.py
# Bcrypt password hashing

from passlib.context import CryptContext


# bcrypt context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """Hash a password // for registration"""
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check password against hash // for login"""
    return pwd_context.verify(plain_password, hashed_password)
