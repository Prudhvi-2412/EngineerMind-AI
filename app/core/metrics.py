import time
from fastapi import Request, Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

# Prometheus Metrics Definitions
HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP Requests Received",
    ["method", "endpoint", "status_code"]
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "http_request_duration_seconds",
    "HTTP Request Latency in Seconds",
    ["method", "endpoint"]
)

AGENT_EXECUTION_DURATION_SECONDS = Histogram(
    "agent_execution_duration_seconds",
    "LangGraph AI Agent Execution Duration in Seconds",
    ["agent_name"]
)

EVENTS_INGESTED_TOTAL = Counter(
    "events_ingested_total",
    "Total Events Ingested by Event Collector",
    ["source"]
)

NEO4J_ACTIVE_CONNECTIONS = Gauge(
    "neo4j_active_connections",
    "Active Neo4j Driver Connections"
)


async def prometheus_metrics_middleware(request: Request, call_next):
    """
    Middleware to intercept HTTP requests and update Prometheus metrics.
    """
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    endpoint = request.url.path
    method = request.method
    status_code = str(response.status_code)

    HTTP_REQUESTS_TOTAL.labels(method=method, endpoint=endpoint, status_code=status_code).inc()
    HTTP_REQUEST_DURATION_SECONDS.labels(method=method, endpoint=endpoint).observe(duration)

    return response


def get_prometheus_metrics_response() -> Response:
    """
    Returns Prometheus metrics formatted endpoint response for /metrics scraping.
    """
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
