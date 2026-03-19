import logging
import sys

from pythonjsonlogger.json import JsonFormatter


def setup_logging() -> None:
    formatter = JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s %(otelTraceID)s %(otelSpanID)s",
        rename_fields={
            "asctime": "timestamp",
            "levelname": "severity",
            "otelTraceID": "trace_id",
            "otelSpanID": "span_id",
        },
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)
