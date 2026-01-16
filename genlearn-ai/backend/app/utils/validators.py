"""
Input Validators for API endpoints
Provides validation functions and Pydantic validators
"""

import re
import html
import logging
from typing import Optional, Any
from pydantic import validator, Field
from fastapi import HTTPException, status, UploadFile
from app.config import settings

logger = logging.getLogger(__name__)

# Regex patterns
USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_]{3,30}$')
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
SESSION_ID_PATTERN = re.compile(r'^SES[0-9]{3,}$')
USER_ID_PATTERN = re.compile(r'^USR[0-9]{3,}$')
QUESTION_ID_PATTERN = re.compile(r'^(MCQ|DSC)[0-9]{3,}$')

# Dangerous patterns for prompt injection
PROMPT_INJECTION_PATTERNS = [
    r'ignore\s+(previous|above|all)\s+instructions?',
    r'disregard\s+(previous|above|all)',
    r'forget\s+(previous|above|all)',
    r'new\s+instructions?:',
    r'system\s*:',
    r'assistant\s*:',
    r'<\s*script',
    r'javascript\s*:',
]


def validate_username(username: str) -> str:
    """Validate username format"""
    if not username or not USERNAME_PATTERN.match(username):
        raise ValueError(
            "Username must be 3-30 characters, alphanumeric and underscores only"
        )
    return username


def validate_email(email: str) -> str:
    """Validate email format"""
    if not email or not EMAIL_PATTERN.match(email):
        raise ValueError("Invalid email format")
    return email.lower()


def validate_password(password: str) -> str:
    """Validate password strength"""
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    if len(password) > 100:
        raise ValueError("Password must be less than 100 characters")
    return password


def validate_session_id(session_id: str) -> str:
    """Validate session ID format"""
    if not session_id or not SESSION_ID_PATTERN.match(session_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid session ID format"
        )
    return session_id


def validate_user_id(user_id: str) -> str:
    """Validate user ID format"""
    if not user_id or not USER_ID_PATTERN.match(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    return user_id


def validate_question_id(question_id: str) -> str:
    """Validate question ID format"""
    if not question_id or not QUESTION_ID_PATTERN.match(question_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid question ID format"
        )
    return question_id


def validate_difficulty_level(level: int) -> int:
    """Validate difficulty level (1-10)"""
    if not isinstance(level, int) or level < 1 or level > 10:
        raise ValueError("Difficulty level must be between 1 and 10")
    return level


def validate_duration_minutes(duration: int) -> int:
    """Validate session duration"""
    valid_durations = [5, 10, 15, 30, 45, 60]
    if duration not in valid_durations:
        raise ValueError(f"Duration must be one of: {valid_durations}")
    return duration


def validate_pagination(
    limit: int,
    offset: int,
    max_limit: Optional[int] = None
) -> tuple:
    """
    Validate and sanitize pagination parameters.

    Args:
        limit: Requested page size
        offset: Requested offset
        max_limit: Maximum allowed limit

    Returns:
        Tuple of (sanitized_limit, sanitized_offset)
    """
    max_limit = max_limit or settings.MAX_PAGE_SIZE

    if limit < 1:
        limit = settings.DEFAULT_PAGE_SIZE
    elif limit > max_limit:
        limit = max_limit

    if offset < 0:
        offset = 0

    return limit, offset


def sanitize_string(text: str, max_length: int = 1000) -> str:
    """
    Sanitize string input for safe storage and display.

    Args:
        text: Input text
        max_length: Maximum allowed length

    Returns:
        Sanitized string
    """
    if not text:
        return ""

    # Truncate to max length
    text = text[:max_length]

    # HTML escape to prevent XSS
    text = html.escape(text)

    # Remove null bytes
    text = text.replace('\x00', '')

    return text.strip()


def sanitize_topic(topic: str) -> str:
    """
    Sanitize topic input for AI prompts.

    Removes potential prompt injection attempts while preserving
    legitimate educational topics.

    Args:
        topic: User-provided topic

    Returns:
        Sanitized topic
    """
    if not topic:
        raise ValueError("Topic cannot be empty")

    # Trim and limit length
    topic = topic.strip()[:200]

    # Check for prompt injection patterns
    topic_lower = topic.lower()
    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, topic_lower, re.IGNORECASE):
            logger.warning(f"Potential prompt injection detected: {topic[:50]}...")
            raise ValueError("Invalid characters in topic")

    # Remove control characters
    topic = ''.join(char for char in topic if ord(char) >= 32 or char in '\n\t')

    # HTML escape
    topic = html.escape(topic)

    if len(topic) < 2:
        raise ValueError("Topic must be at least 2 characters")

    return topic


def sanitize_answer(answer: str, max_length: int = 5000) -> str:
    """
    Sanitize user answer input.

    Args:
        answer: User-provided answer
        max_length: Maximum allowed length

    Returns:
        Sanitized answer
    """
    if not answer:
        return ""

    # Trim and limit length
    answer = answer.strip()[:max_length]

    # Remove control characters except newlines and tabs
    answer = ''.join(char for char in answer if ord(char) >= 32 or char in '\n\t')

    return answer


async def validate_upload_file(
    file: UploadFile,
    allowed_types: Optional[list[str]] = None,
    max_size_mb: Optional[int] = None
) -> UploadFile:
    """
    Validate uploaded file.

    Args:
        file: Uploaded file
        allowed_types: List of allowed MIME types
        max_size_mb: Maximum file size in MB

    Returns:
        Validated file

    Raises:
        HTTPException: If validation fails
    """
    allowed_types = allowed_types or settings.ALLOWED_IMAGE_TYPES
    max_size_mb = max_size_mb or settings.MAX_UPLOAD_SIZE_MB
    max_size_bytes = max_size_mb * 1024 * 1024

    # Check content type
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {allowed_types}"
        )

    # Check file size by reading content
    content = await file.read()
    await file.seek(0)  # Reset file position

    if len(content) > max_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size: {max_size_mb}MB"
        )

    if len(content) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is empty"
        )

    # Validate filename
    if file.filename:
        # Remove path components (prevent path traversal)
        filename = file.filename.replace('\\', '/').split('/')[-1]
        # Remove null bytes
        filename = filename.replace('\x00', '')
        # Limit length
        filename = filename[:255]
        file.filename = filename

    return file


def validate_mcq_answer(answer: str) -> str:
    """Validate MCQ answer option"""
    answer = answer.upper().strip()
    if answer not in ['A', 'B', 'C', 'D']:
        raise ValueError("Answer must be A, B, C, or D")
    return answer


def validate_visual_style(style: str) -> str:
    """Validate visual style option"""
    style = style.lower().strip()
    if style not in ['cartoon', 'realistic']:
        raise ValueError("Visual style must be 'cartoon' or 'realistic'")
    return style


def validate_play_mode(mode: str) -> str:
    """Validate play mode option"""
    mode = mode.lower().strip()
    if mode not in ['solo', 'team', 'tournament']:
        raise ValueError("Play mode must be 'solo', 'team', or 'tournament'")
    return mode
