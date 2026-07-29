import logging
import sys
import json
from datetime import datetime
from typing import Any, Dict


class JSONFormatter(logging.Formatter):
    """
    Custom JSON Formatter for Grafana Loki Structured Logging.
    Formats log records into JSON objects containing timestamp, service_name, level, trace_id, and message.
    """

    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat() + "Z",
            "service": "engineering_os_backend",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "filename": record.filename,
            "lineno": record.lineno,
        }

        # Include OpenTelemetry trace and span IDs if present
        if hasattr(record, "trace_id"):
            log_data["trace_id"] = getattr(record, "trace_id")
        if hasattr(record, "span_id"):
            log_data["span_id"] = getattr(record, "span_id")

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


def setup_structured_logging():
    """
    Configures application-wide JSON structured logging.
    """
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.handlers = [handler]

    # Silence verbose noisy loggers
    logging.getLogger("uvicorn.access").handlers = [handler]
    logging.getLogger("neo4j").setLevel(logging.WARNING)


logger = logging.getLogger("engineering_os")
