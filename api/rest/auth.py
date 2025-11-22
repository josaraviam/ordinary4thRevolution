# api/rest/auth.py
# Auth endpoints // login & register

from fastapi import APIRouter, HTTPException, status

from domain.models.user import UserCreate, UserLogin, TokenResponse, UserResponse
from domain.services.auth_service import auth_service
from domain.exceptions.custom_exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
)


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """
    POST /api/auth/register
    Create new user account
    """
    try:
        return await auth_service.register(user_data)
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """
    POST /api/auth/login
    Authenticate and get JWT token
    """
    try:
        return await auth_service.login(credentials.username, credentials.password)
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message
        )
