from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from infrastructure.security.jwt_handler import decode_token
from infrastructure.database.repositories.user_repository import user_repo


# Bearer token extractor - this is what grabs the token from the request
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Dependency to get current user from JWT token
    This is the main security gatekeeper - use it on protected routes
    Usage: current_user: dict = Depends(get_current_user)
    """
    # Extract the actual token from the Bearer format
    token = credentials.credentials

    # Decode and verify the JWT token (the magic happens here)
    payload = decode_token(token)
    if payload is None:
        # Token is either invalid or expired - no access for you!
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}  # tells client to use Bearer auth
        )

    # Extract user ID from the token payload
    user_id: str = payload.get("sub")  # 'sub' is the standard JWT field for user ID
    if user_id is None:
        # Token exists but doesn't have user info - something's fishy
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Double-check that the user actually exists in our database
    # (in case someone deleted a user but their token is still valid)
    user = await user_repo.find_by_id(user_id)
    if user is None:
        # User doesn't exist anymore - token is orphaned
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # All checks passed - return the user data
    return user


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)  # don't throw error if no token
    )
) -> Optional[dict]:
    """
    Optional authentication - returns None if no token provided
    Perfect for routes that work with or without authentication
    Like public endpoints that show extra info if you're logged in
    """
    if credentials is None:
        # No token provided - that's fine for optional auth
        return None

    try:
        # Try to get the user normally
        return await get_current_user(credentials)
    except HTTPException:
        return None
