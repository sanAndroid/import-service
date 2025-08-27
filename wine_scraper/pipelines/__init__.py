"""Pipelines package for data processing and storage."""

from .models import Wine, WineRating, ScrapingResult
from .transforms import DataTransformer
from .sinks import CSVSink, JSONSink, ParquetSink

__all__ = [
    "Wine", "WineRating", "ScrapingResult",
    "DataTransformer",
    "CSVSink", "JSONSink", "ParquetSink",
]