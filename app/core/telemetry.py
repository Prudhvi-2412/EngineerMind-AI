from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource
from app.core.config import settings


def setup_opentelemetry(app=None):
    """
    Configures OpenTelemetry Tracing SDK with Resource attributes and SpanProcessors.
    """
    resource = Resource.create(attributes={"service.name": "engineering-os-backend", "environment": settings.ENVIRONMENT})
    provider = TracerProvider(resource=resource)
    
    # Process spans in background batch
    processor = BatchSpanProcessor(ConsoleSpanExporter())
    provider.add_span_processor(processor)

    trace.set_tracer_provider(provider)
    return trace.get_tracer("engineering_os_tracer")


tracer = trace.get_tracer("engineering_os_tracer")
