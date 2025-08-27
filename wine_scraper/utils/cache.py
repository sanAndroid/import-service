"""Caching utilities."""

import json
import time
from pathlib import Path
from typing import Any, Optional

import diskcache

from settings import settings


class Cache:
    """Simple disk-based cache with TTL support."""

    def __init__(self, name: str):
        """Initialize cache with given name."""
        cache_dir = Path(settings.cache_dir)
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.cache = diskcache.Cache(str(cache_dir / name))

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if it exists and is not expired."""
        try:
            value = self.cache.get(key)
            if value is None:
                return None
            
            # Check if it's a tuple with TTL
            if isinstance(value, tuple) and len(value) == 2:
                data, expiry = value
                if time.time() < expiry:
                    return data
                else:
                    # Remove expired entry
                    self.cache.delete(key)
                    return None
            
            return value
            
        except Exception:
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache with optional TTL."""
        ttl = ttl or settings.cache_ttl
        
        if ttl:
            expiry = time.time() + ttl
            value_to_store = (value, expiry)
        else:
            value_to_store = value
        
        try:
            self.cache.set(key, value_to_store)
        except Exception:
            pass

    def delete(self, key: str) -> None:
        """Delete a key from cache."""
        try:
            self.cache.delete(key)
        except Exception:
            pass

    def clear(self) -> None:
        """Clear all entries from cache."""
        try:
            self.cache.clear()
        except Exception:
            pass

    def close(self) -> None:
        """Close the cache."""
        self.cache.close()