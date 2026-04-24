"""Structured JSON log formatter for hub request logs.

Pulls a fixed set of structured fields off the ``LogRecord`` (populated via
``logger.info("...", extra={...})`` inside the xray middleware) and emits a
single-line JSON document. TKT-071 wires this into Grafana Cloud via OTLP;
until then, the handler writes to stdout.
"""

import json
import logging
from typing import Any

# Structured fields the xray middleware attaches to request-log records.
_STRUCTURED_FIELDS = (
    "method",
    "path",
    "tenant_id",
    "user_email",
    "xray_session",
    "status",
    "duration_ms",
    "error",
)


class JsonFormatter(logging.Formatter):
    """Render a LogRecord as a single-line JSON object."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for key in _STRUCTURED_FIELDS:
            if hasattr(record, key):
                payload[key] = getattr(record, key)
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str)
