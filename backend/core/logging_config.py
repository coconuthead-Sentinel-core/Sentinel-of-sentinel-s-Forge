"""
Structured JSON logging configuration for production monitoring.

Provides machine-readable log output compatible with:
- ELK Stack (Elasticsearch, Logstash, Kibana)
- AWS CloudWatch
- Azure Monitor / Log Analytics
- Datadog, New Relic, Splunk
- Any JSON log aggregator

Usage:
    from backend.core.logging_config import setup_logging
    setup_logging()  # Call once at app startup
"""
import logging
import json
import sys
import time
import traceback
from datetime import datetime, timezone
from typing import Any, Optional

from .config import settings


class JSONFormatter(logging.Formatter):
    """Format log records as single-line JSON for log aggregators."""

    def __init__(self, service_name: str = "sentinel-forge"):
        super().__init__()
        self.service_name = service_name

    def format(self, record: logging.LogRecord) -> str:
        log_entry: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "service": self.service_name,
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT,
        }

        # Add source location
        if record.pathname:
            log_entry["source"] = {
                "file": record.pathname,
                "line": record.lineno,
                "function": record.funcName,
            }

        # Add exception info if present
        if record.exc_info and record.exc_info[0] is not None:
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "stacktrace": traceback.format_exception(*record.exc_info),
            }

        # Add any extra fields attached to the record
        for key in ("request_id", "user_id", "endpoint", "method", "status_code", "duration_ms", "client_ip"):
            if hasattr(record, key):
                log_entry[key] = getattr(record, key)

        return json.dumps(log_entry, default=str)


class RequestContextFilter(logging.Filter):
    """Attach request context to log records (for use with middleware)."""

    def __init__(self):
        super().__init__()
        self._context: dict[str, Any] = {}

    def set_context(self, **kwargs: Any) -> None:
        self._context = kwargs

    def clear_context(self) -> None:
        self._context = {}

    def filter(self, record: logging.LogRecord) -> bool:
        for key, value in self._context.items():
            setattr(record, key, value)
        return True


# Singleton filter instance for request context
request_context = RequestContextFilter()


def setup_logging() -> None:
    """Configure logging for the application.

    - Production: JSON formatter for machine parsing
    - Development: Standard human-readable formatter
    """
    root = logging.getLogger()

    # Clear existing handlers
    root.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)

    if settings.is_production:
        handler.setFormatter(JSONFormatter())
    else:
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )

    handler.addFilter(request_context)
    root.addHandler(handler)
    root.setLevel(getattr(logging, settings.LOG_LEVEL, logging.INFO))

    # Quiet noisy libraries
    logging.getLogger("azure").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
