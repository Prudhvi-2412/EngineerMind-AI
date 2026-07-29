from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

EVENTS_COLLECTED_TOTAL = Counter(
    "engineeringos_events_collected_total",
    "Total raw telemetry events ingested by collector service",
    ["source", "event_action"]
)

EVENTS_PROCESSED_TOTAL = Counter(
    "engineeringos_events_processed_total",
    "Total telemetry events processed asynchronously by worker",
    ["source", "status"]
)

EVENT_PROCESSING_LATENCY = Histogram(
    "engineeringos_event_processing_latency_seconds",
    "Time taken to normalize and persist telemetry events in seconds",
    ["source"]
)


def get_prometheus_metrics_payload() -> bytes:
    """Generates latest Prometheus scraping exposition format"""
    return generate_latest()
