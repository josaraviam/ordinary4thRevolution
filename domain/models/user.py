from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user fields // shared across schemas"""
    username: str = Field(..., min_length=3, max_length=50)


class UserCreate(UserBase):
    """For registration // pwd required"""
    password: str = Field(..., min_length=6)


class UserLogin(UserBase):
    """For login request"""
    password: str


class UserInDB(UserBase):
    """Full user as stored in MongoDB"""
    id: Optional[str] = Field(None, alias="_id")
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

    class Config:
        populate_by_name = True  # allows _id -> id


class UserResponse(UserBase):
    """Safe user response // no pwd"""
    id: str
    created_at: datetime
    is_active: bool


class TokenResponse(BaseModel):
    """JWT token response"""
    token: str
    token_type: str = "bearer"
    expires_in: int  # seconds
