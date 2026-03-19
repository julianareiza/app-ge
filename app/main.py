import os

from fastapi import FastAPI

from app.config import settings
from app.logging_config import setup_logging
from app.routes import health, items

setup_logging()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

# OTel instrumentation — must happen BEFORE app starts serving
if os.getenv("OTEL_ENABLED", "true").lower() == "true":
    from app.middleware.otel import setup_otel_providers, create_metrics_middleware
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

    setup_otel_providers()
    app.add_middleware(create_metrics_middleware())
    FastAPIInstrumentor.instrument_app(app)

app.include_router(health.router)
app.include_router(items.router)
