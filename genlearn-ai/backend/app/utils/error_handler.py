"""
Error Handler Utilities
Provides safe error handling that doesn't leak sensitive information
"""

import logging
from typing import Any, Optional
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)


def handle_error(
    error: Exception,
    operation: str,
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    public_message: Optional[str] = None,
    log_context: Optional[dict[str, Any]] = None
) -> HTTPException:
    """
    Handle exceptions safely without leaking sensitive information.

    Args:
        error: The caught exception
        operation: Description of operation that failed (e.g., "fetching user profile")
        status_code: HTTP status code to return
        public_message: Optional custom message for user (if None, uses generic message)
        log_context: Optional context dict for logging

    Returns:
        HTTPException with safe error message
    """
    # Log the full error with context
    log_msg = f"Error during {operation}: {type(error).__name__}: {str(error)}"
    if log_context:
        log_msg += f" | Context: {log_context}"

    logger.error(log_msg, exc_info=True)

    # Return generic message to user (don't leak internals)
    if public_message:
        detail = public_message
    else:
        # Generic message based on status code
        if status_code == 404:
            detail = "Resource not found"
        elif status_code == 403:
            detail = "Access denied"
        elif status_code == 400:
            detail = "Invalid request"
        else:
            detail = f"An error occurred while {operation}. Please try again."

    return HTTPException(
        status_code=status_code,
        detail=detail
    )


def safe_error_response(
    operation: str,
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    public_message: Optional[str] = None
):
    """
    Decorator to wrap route handlers with safe error handling.

    Usage:
        @router.get("/profile")
        @safe_error_response("fetching user profile", status.HTTP_404_NOT_FOUND)
        async def get_profile(user_id: str):
            ...
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except HTTPException:
                # Re-raise HTTPExceptions as-is (already safe)
                raise
            except Exception as e:
                raise handle_error(e, operation, status_code, public_message)
        return wrapper
    return decorator


class ErrorMessages:
    """Standardized user-facing error messages"""

    # Generic
    INTERNAL_ERROR = "An internal error occurred. Please try again later."
    INVALID_REQUEST = "Invalid request. Please check your input."

    # Authentication
    INVALID_CREDENTIALS = "Invalid username or password"
    UNAUTHORIZED = "Authentication required"
    FORBIDDEN = "You don't have permission to access this resource"

    # Resources
    NOT_FOUND = "Resource not found"
    ALREADY_EXISTS = "Resource already exists"

    # Session
    SESSION_NOT_FOUND = "Session not found or expired"
    SESSION_ERROR = "An error occurred with your session. Please try again."

    # Content
    CONTENT_GENERATION_ERROR = "Failed to generate content. Please try again."
    UPLOAD_ERROR = "Failed to upload file. Please check the file and try again."

    # Quiz
    QUESTION_ERROR = "Failed to load questions. Please try again."
    ANSWER_ERROR = "Failed to submit answer. Please try again."

    # Video
    VIDEO_ERROR = "Failed to generate video. Please try again."
    VIDEO_NOT_READY = "Video is not ready yet. Please try again later."

    # Team/Tournament
    TEAM_ERROR = "An error occurred with team operations. Please try again."
    TOURNAMENT_ERROR = "An error occurred with tournament operations. Please try again."
