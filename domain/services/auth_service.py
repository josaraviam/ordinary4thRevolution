from datetime import datetime
from typing import Optional

from domain.models.user import UserCreate, UserResponse, TokenResponse
from domain.exceptions.custom_exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from infrastructure.database.repositories.user_repository import user_repo
from infrastructure.security.password_hasher import hash_password, verify_password
from infrastructure.security.jwt_handler import create_access_token, get_token_expiry_seconds
from config.logging_config import get_logger

logger = get_logger("services.auth")


class AuthService:
    """
    Auth service layer
    Handles registration and login business logic
    """

    async def register(self, user_data: UserCreate) -> UserResponse:
        """
        Register new user
        Raises: UserAlreadyExistsError if username taken
        """
        # Check if username exists
        if await user_repo.username_exists(user_data.username):
            raise UserAlreadyExistsError(f"Username '{user_data.username}' already taken")

        # Create user doc
        user_doc = {
            "username": user_data.username,
            "hashed_password": hash_password(user_data.password),
            "created_at": datetime.utcnow(),
            "is_active": True
        }

        # Insert and get id
        user_id = await user_repo.create(user_doc)

        return UserResponse(
            id=user_id,
            username=user_data.username,
            created_at=user_doc["created_at"],
            is_active=True
        )

    async def login(self, username: str, password: str) -> TokenResponse:
        """
        Authenticate user and return JWT
        Raises: InvalidCredentialsError if auth fails
        """
        # Find user
        user = await user_repo.find_by_username(username)
        if user is None:
            raise InvalidCredentialsError()

        # Verify password
        if not verify_password(password, user["hashed_password"]):
            raise InvalidCredentialsError()

        # Check active
        if not user.get("is_active", True):
            raise InvalidCredentialsError("User account is disabled")

        # Create token
        token = create_access_token(subject=str(user["_id"]))

        return TokenResponse(
            token=token,
            token_type="bearer",
            expires_in=get_token_expiry_seconds()
        )

    async def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """Get user by ID for token validation"""
        user = await user_repo.find_by_id(user_id)
        if user is None:
            raise UserNotFoundError()
        return user


# Singleton instance
auth_service = AuthService()
