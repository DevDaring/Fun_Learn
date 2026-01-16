"""
Utility Helper Functions
"""

import random
import string
from datetime import datetime
from typing import Any
import hashlib


def generate_unique_id(prefix: str = "", length: int = 3) -> str:
    """
    Generate a unique ID with optional prefix

    Args:
        prefix: Prefix for the ID (e.g., 'USR', 'SES')
        length: Number of digits in the numeric part

    Returns:
        Unique ID string (e.g., 'USR001', 'SES042')
    """
    # Get timestamp-based component
    timestamp = int(datetime.now().timestamp() * 1000)

    # Generate random number
    random_num = random.randint(0, 10 ** length - 1)

    # Format with leading zeros
    id_number = f"{random_num:0{length}d}"

    return f"{prefix}{id_number}_{timestamp % 10000}"


def generate_session_id() -> str:
    """Generate a unique session ID"""
    return generate_unique_id("SES", 3)


def generate_user_id() -> str:
    """Generate a unique user ID"""
    return generate_unique_id("USR", 3)


def calculate_xp_for_level(level: int) -> int:
    """
    Calculate XP required for a given level

    Args:
        level: User level

    Returns:
        XP points required
    """
    return (level - 1) * 500


def calculate_level_from_xp(xp: int) -> int:
    """
    Calculate user level from XP points

    Args:
        xp: Total XP points

    Returns:
        User level
    """
    return max(1, (xp // 500) + 1)


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to remove unsafe characters

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    # Remove unsafe characters
    valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
    sanitized = ''.join(c for c in filename if c in valid_chars)

    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip('. ')

    # Limit length
    if len(sanitized) > 255:
        name, ext = sanitized.rsplit('.', 1) if '.' in sanitized else (sanitized, '')
        sanitized = name[:250] + ('.' + ext if ext else '')

    return sanitized or 'unnamed'


def hash_string(text: str) -> str:
    """
    Generate SHA256 hash of a string

    Args:
        text: String to hash

    Returns:
        Hex digest of hash
    """
    return hashlib.sha256(text.encode()).hexdigest()


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to maximum length

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add when truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)].rstrip() + suffix


def format_duration(seconds: int) -> str:
    """
    Format duration in seconds to human-readable string

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration (e.g., "5m 30s", "1h 15m")
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours}h {minutes}m"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"


def calculate_accuracy_rate(correct: int, total: int) -> float:
    """
    Calculate accuracy rate as percentage

    Args:
        correct: Number of correct answers
        total: Total number of questions

    Returns:
        Accuracy rate (0-100)
    """
    if total == 0:
        return 0.0

    return round((correct / total) * 100, 2)


def parse_keywords(keywords_str: str) -> list[str]:
    """
    Parse comma-separated keywords string into list

    Args:
        keywords_str: Comma-separated keywords

    Returns:
        List of keywords
    """
    if not keywords_str:
        return []

    return [k.strip() for k in keywords_str.split(',') if k.strip()]


def format_keywords(keywords_list: list[str]) -> str:
    """
    Format keywords list into comma-separated string

    Args:
        keywords_list: List of keywords

    Returns:
        Comma-separated string
    """
    return ', '.join(keywords_list)


def validate_difficulty_level(level: int) -> bool:
    """
    Validate difficulty level is within acceptable range

    Args:
        level: Difficulty level

    Returns:
        True if valid, False otherwise
    """
    return 1 <= level <= 10


def validate_duration(minutes: int) -> bool:
    """
    Validate duration is within acceptable range

    Args:
        minutes: Duration in minutes

    Returns:
        True if valid, False otherwise
    """
    return 5 <= minutes <= 120


def calculate_points_for_difficulty(difficulty: int, is_correct: bool) -> int:
    """
    Calculate points earned based on difficulty and correctness

    Args:
        difficulty: Question difficulty (1-10)
        is_correct: Whether answer was correct

    Returns:
        Points earned
    """
    base_points = difficulty * 10

    if is_correct:
        return base_points
    else:
        # Partial credit for attempting
        return max(2, difficulty)


def merge_dicts(dict1: dict[str, Any], dict2: dict[str, Any]) -> dict[str, Any]:
    """
    Merge two dictionaries, with dict2 values taking precedence

    Args:
        dict1: First dictionary
        dict2: Second dictionary (overrides dict1)

    Returns:
        Merged dictionary
    """
    result = dict1.copy()
    result.update(dict2)
    return result


def safe_int(value: Any, default: int = 0) -> int:
    """
    Safely convert value to integer

    Args:
        value: Value to convert
        default: Default value if conversion fails

    Returns:
        Integer value
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_float(value: Any, default: float = 0.0) -> float:
    """
    Safely convert value to float

    Args:
        value: Value to convert
        default: Default value if conversion fails

    Returns:
        Float value
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def is_valid_email(email: str) -> bool:
    """
    Basic email validation

    Args:
        email: Email address to validate

    Returns:
        True if valid format, False otherwise
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
