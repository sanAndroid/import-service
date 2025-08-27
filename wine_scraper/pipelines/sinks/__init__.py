"""Data sinks package."""

from .files import CSVSink, JSONSink, ParquetSink

__all__ = ["CSVSink", "JSONSink", "ParquetSink"]