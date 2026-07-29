import pytest
from app.core.logging import JSONFormatter
import logging


def test_json_log_formatter():
    formatter = JSONFormatter()
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test.py",
        lineno=10,
        msg="Test log message",
        args=(),
        exc_info=None
    )

    formatted_json = formatter.format(record)
    assert "timestamp" in formatted_json
    assert "engineering_os_backend" in formatted_json
    assert "Test log message" in formatted_json
