# api/rest/auth.py
# Authentication API routes - login/register stuff
# Keep it simple: register, login, get JWT token, profit!

from fastapi import APIRouter, HTTPException, status

from domain.models.user import UserCreate, UserLogin, TokenResponse, UserResponse
from domain.services.auth_service import auth_service
from domain.exceptions.custom_exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
)

# Router for all auth-related endpoints
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """
    POST /api/auth/register
    
    Create new user account - pretty straightforward stuff.
    Returns user info (without password obviously).
    """
    try:
        return await auth_service.register(user_data)
    except UserAlreadyExistsError as e:
        # Username already taken - happens all the time
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """
    POST /api/auth/login
    
    Login with username/password, get JWT token back.
    Token is what you use for protected endpoints.
    """
    try:
        return await auth_service.login(credentials.username, credentials.password)
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message
        )
