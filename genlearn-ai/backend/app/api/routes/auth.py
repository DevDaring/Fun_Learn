"""
Authentication Routes - Login and user authentication
"""

import logging
from fastapi import APIRouter, HTTPException, status, Depends, Request
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from datetime import datetime

from app.api.dependencies import create_access_token, get_current_user, verify_api_key
from app.database.csv_handler import CSVHandler
from app.models.user import User
from app.utils.rate_limiter import check_login_rate_limit, reset_login_rate_limit
from app.utils.validators import validate_username, sanitize_string

logger = logging.getLogger(__name__)
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LoginRequest(BaseModel):
    """Login request model"""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=100)


class LoginResponse(BaseModel):
    """Login response model"""
    access_token: str
    token_type: str = "bearer"
    user: User


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """Generate password hash"""
    return pwd_context.hash(password)


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(
    credentials: LoginRequest,
    request: Request,
    api_key_valid: bool = Depends(verify_api_key)
):
    """
    Login endpoint - authenticate user and return JWT token

    Args:
        credentials: Username and password
        request: FastAPI request object
        api_key_valid: API key validation result

    Returns:
        Access token and user data

    Raises:
        HTTPException: If credentials are invalid or rate limit exceeded
    """
    # Check rate limit first
    await check_login_rate_limit(request)

    csv_handler = CSVHandler()

    try:
        # Sanitize username
        username = sanitize_string(credentials.username, max_length=50)

        # Find user by username
        users = csv_handler.read_all("users")
        user = None

        for u in users:
            if u.get("username") == username:
                user = u
                break

        if not user:
            logger.warning(f"Login attempt for non-existent user: {username[:20]}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verify password
        if not verify_password(credentials.password, user.get("password_hash", "")):
            logger.warning(f"Failed login attempt for user: {username[:20]}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Reset rate limit on successful login
        reset_login_rate_limit(request)

        # Update last login
        user["last_login"] = datetime.now().isoformat()
        csv_handler.update("users", user["user_id"], user, "user_id")

        # Create access token
        access_token = create_access_token(
            data={"sub": user["user_id"], "role": user.get("role", "user")}
        )

        # Remove password hash from response
        user_data = {k: v for k, v in user.items() if k != "password_hash"}

        logger.info(f"Successful login for user: {user['user_id']}")

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_data
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during login. Please try again."
        )


@router.get("/me", response_model=User, status_code=status.HTTP_200_OK)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current authenticated user information

    Args:
        current_user: Authenticated user from dependency

    Returns:
        User data without password hash
    """
    try:
        # Remove password hash from response
        user_data = {k: v for k, v in current_user.items() if k != "password_hash"}
        return user_data

    except Exception as e:
        logger.error(f"Error fetching user data: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching user data"
        )
