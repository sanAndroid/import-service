"""HTTP client utilities."""

import httpx
from typing import Optional

from settings import settings


def create_http_client(
    timeout: Optional[int] = None,
    retries: Optional[int] = None,
) -> httpx.AsyncClient:
    """Create an HTTP client with common settings."""
    timeout = timeout or settings.http_timeout
    
    transport = httpx.AsyncHTTPTransport(
        retries=retries or settings.http_retries,
    )
    
    client = httpx.AsyncClient(
        timeout=httpx.Timeout(timeout),
        transport=transport,
        headers={"User-Agent": settings.user_agents[0]},
    )
    
    return client