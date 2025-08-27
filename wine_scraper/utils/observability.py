"""Observability utilities for logging and metrics."""

import logging
import sys
from typing import Any, Dict

import structlog
from rich.console import Console
from rich.logging import RichHandler

from settings import settings


def setup_logging() -> None:
    """Setup structured logging with rich output."""
    
    # Remove default handlers
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=Console(), rich_tracebacks=True)]
    )
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> Any:
    """Get a structured logger instance."""
    return structlog.get_logger(name)


class MetricsCollector:
    """Simple metrics collector for scraper performance."""
    
    def __init__(self):
        self.metrics: Dict[str, Any] = {
            "requests_made": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "errors": 0,
            "wines_found": 0,
        }
    
    def increment(self, key: str, value: int = 1) -> None:
        """Increment a metric counter."""
        if key in self.metrics:
            self.metrics[key] += value
    
    def set_value(self, key: str, value: Any) -> None:
        """Set a metric value."""
        self.metrics[key] = value
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all collected metrics."""
        return self.metrics.copy()


# Global metrics instance
metrics = MetricsCollector()


# Initialize logging
setup_logging()