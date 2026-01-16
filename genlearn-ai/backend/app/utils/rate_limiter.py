"""
Rate Limiter for API endpoints
Uses in-memory storage for simplicity (suitable for single-instance deployments)
"""

import time
import logging
from typing import Tuple, Optional
from collections import defaultdict
import threading
from fastapi import HTTPException, status, Request
from app.config import settings

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Simple in-memory rate limiter with sliding window.

    For production with multiple instances, use Redis-based rate limiting.
    """

    def __init__(self):
        # {client_id: [(timestamp, count), ...]}
        self._requests: dict[str, list] = defaultdict(list)
        self._lock = threading.Lock()

    def _clean_old_requests(self, client_id: str, window_seconds: int) -> None:
        """Remove requests outside the current window"""
        current_time = time.time()
        cutoff = current_time - window_seconds

        with self._lock:
            self._requests[client_id] = [
                ts for ts in self._requests[client_id]
                if ts > cutoff
            ]

    def is_allowed(
        self,
        client_id: str,
        max_requests: int,
        window_seconds: int
    ) -> Tuple[bool, int, int]:
        """
        Check if request is allowed under rate limit.

        Args:
            client_id: Unique identifier for the client (IP, user_id, etc.)
            max_requests: Maximum requests allowed in the window
            window_seconds: Time window in seconds

        Returns:
            Tuple of (is_allowed, remaining_requests, reset_seconds)
        """
        current_time = time.time()
        self._clean_old_requests(client_id, window_seconds)

        with self._lock:
            request_count = len(self._requests[client_id])

            if request_count >= max_requests:
                # Calculate reset time
                oldest_request = min(self._requests[client_id]) if self._requests[client_id] else current_time
                reset_seconds = int(oldest_request + window_seconds - current_time)
                return False, 0, max(0, reset_seconds)

            # Add new request
            self._requests[client_id].append(current_time)
            remaining = max_requests - request_count - 1

            return True, remaining, window_seconds

    def reset(self, client_id: str) -> None:
        """Reset rate limit for a client"""
        with self._lock:
            if client_id in self._requests:
                del self._requests[client_id]


# Global rate limiter instances
_general_limiter = RateLimiter()
_login_limiter = RateLimiter()


def get_client_id(request: Request) -> str:
    """Get unique client identifier from request"""
    # Use X-Forwarded-For if behind proxy, otherwise client host
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


async def check_rate_limit(
    request: Request,
    max_requests: Optional[int] = None,
    window_seconds: Optional[int] = None
) -> None:
    """
    Check general rate limit for a request.

    Args:
        request: FastAPI request object
        max_requests: Override default max requests
        window_seconds: Override default window

    Raises:
        HTTPException: If rate limit exceeded
    """
    client_id = get_client_id(request)
    max_req = max_requests or settings.RATE_LIMIT_REQUESTS
    window = window_seconds or settings.RATE_LIMIT_WINDOW_SECONDS

    allowed, remaining, reset_seconds = _general_limiter.is_allowed(
        client_id, max_req, window
    )

    if not allowed:
        logger.warning(f"Rate limit exceeded for client: {client_id}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Try again in {reset_seconds} seconds.",
            headers={
                "X-RateLimit-Limit": str(max_req),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(reset_seconds),
                "Retry-After": str(reset_seconds)
            }
        )


async def check_login_rate_limit(request: Request) -> None:
    """
    Check rate limit specifically for login attempts.

    Uses stricter limits to prevent brute force attacks.
    """
    client_id = get_client_id(request)
    max_requests = settings.LOGIN_RATE_LIMIT_REQUESTS
    window_seconds = settings.LOGIN_RATE_LIMIT_WINDOW_SECONDS

    allowed, remaining, reset_seconds = _login_limiter.is_allowed(
        client_id, max_requests, window_seconds
    )

    if not allowed:
        logger.warning(f"Login rate limit exceeded for client: {client_id}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many login attempts. Try again in {reset_seconds} seconds.",
            headers={
                "Retry-After": str(reset_seconds)
            }
        )


def reset_login_rate_limit(request: Request) -> None:
    """Reset login rate limit after successful login"""
    client_id = get_client_id(request)
    _login_limiter.reset(client_id)
