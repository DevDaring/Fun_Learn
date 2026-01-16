"""
Retry utilities for external API calls
"""

import asyncio
import logging
from typing import TypeVar, Callable, Any, Optional, Type, Tuple
from functools import wraps
import httpx
from app.config import settings

logger = logging.getLogger(__name__)

T = TypeVar('T')

# Exceptions that should trigger a retry
RETRYABLE_EXCEPTIONS: Tuple[Type[Exception], ...] = (
    httpx.TimeoutException,
    httpx.NetworkError,
    httpx.ConnectError,
    httpx.ReadTimeout,
    httpx.WriteTimeout,
    httpx.ConnectTimeout,
    ConnectionError,
    TimeoutError,
)

# HTTP status codes that should trigger a retry
RETRYABLE_STATUS_CODES = {408, 429, 500, 502, 503, 504}


async def retry_async(
    func: Callable[..., T],
    *args,
    max_attempts: Optional[int] = None,
    delay_seconds: Optional[float] = None,
    backoff_multiplier: float = 2.0,
    max_delay: float = 30.0,
    retryable_exceptions: Optional[Tuple[Type[Exception], ...]] = None,
    **kwargs
) -> T:
    """
    Retry an async function with exponential backoff.

    Args:
        func: Async function to call
        *args: Positional arguments for func
        max_attempts: Maximum retry attempts
        delay_seconds: Initial delay between retries
        backoff_multiplier: Multiplier for delay on each retry
        max_delay: Maximum delay between retries
        retryable_exceptions: Tuple of exceptions to retry on
        **kwargs: Keyword arguments for func

    Returns:
        Result of the function

    Raises:
        Last exception if all retries fail
    """
    max_attempts = max_attempts or settings.API_RETRY_ATTEMPTS
    delay_seconds = delay_seconds or settings.API_RETRY_DELAY_SECONDS
    retryable_exceptions = retryable_exceptions or RETRYABLE_EXCEPTIONS

    last_exception = None
    current_delay = delay_seconds

    for attempt in range(1, max_attempts + 1):
        try:
            return await func(*args, **kwargs)

        except retryable_exceptions as e:
            last_exception = e
            if attempt < max_attempts:
                logger.warning(
                    f"Attempt {attempt}/{max_attempts} failed: {type(e).__name__}: {e}. "
                    f"Retrying in {current_delay:.1f}s..."
                )
                await asyncio.sleep(current_delay)
                current_delay = min(current_delay * backoff_multiplier, max_delay)
            else:
                logger.error(
                    f"All {max_attempts} attempts failed. Last error: {type(e).__name__}: {e}"
                )

        except httpx.HTTPStatusError as e:
            if e.response.status_code in RETRYABLE_STATUS_CODES:
                last_exception = e
                if attempt < max_attempts:
                    logger.warning(
                        f"Attempt {attempt}/{max_attempts} got status {e.response.status_code}. "
                        f"Retrying in {current_delay:.1f}s..."
                    )
                    await asyncio.sleep(current_delay)
                    current_delay = min(current_delay * backoff_multiplier, max_delay)
                else:
                    logger.error(f"All {max_attempts} attempts failed with status {e.response.status_code}")
            else:
                # Non-retryable status code
                raise

    raise last_exception


def with_retry(
    max_attempts: Optional[int] = None,
    delay_seconds: Optional[float] = None,
    backoff_multiplier: float = 2.0,
    retryable_exceptions: Optional[Tuple[Type[Exception], ...]] = None
):
    """
    Decorator for adding retry logic to async functions.

    Usage:
        @with_retry(max_attempts=3, delay_seconds=1.0)
        async def call_external_api():
            ...
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            return await retry_async(
                func,
                *args,
                max_attempts=max_attempts,
                delay_seconds=delay_seconds,
                backoff_multiplier=backoff_multiplier,
                retryable_exceptions=retryable_exceptions,
                **kwargs
            )
        return wrapper
    return decorator


class RetryableHTTPClient:
    """
    HTTP client wrapper with built-in retry logic.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: float = 60.0,
        max_attempts: Optional[int] = None,
        delay_seconds: Optional[float] = None
    ):
        self.base_url = base_url
        self.timeout = timeout
        self.max_attempts = max_attempts or settings.API_RETRY_ATTEMPTS
        self.delay_seconds = delay_seconds or settings.API_RETRY_DELAY_SECONDS

    async def request(
        self,
        method: str,
        url: str,
        **kwargs
    ) -> httpx.Response:
        """Make HTTP request with retry logic"""
        async def _make_request():
            async with httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout
            ) as client:
                response = await client.request(method, url, **kwargs)
                response.raise_for_status()
                return response

        return await retry_async(
            _make_request,
            max_attempts=self.max_attempts,
            delay_seconds=self.delay_seconds
        )

    async def get(self, url: str, **kwargs) -> httpx.Response:
        return await self.request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs) -> httpx.Response:
        return await self.request("POST", url, **kwargs)

    async def put(self, url: str, **kwargs) -> httpx.Response:
        return await self.request("PUT", url, **kwargs)

    async def delete(self, url: str, **kwargs) -> httpx.Response:
        return await self.request("DELETE", url, **kwargs)
