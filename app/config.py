from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "app-ge"
    app_version: str = "1.0.0"
    debug: bool = False
    otel_exporter_otlp_endpoint: str = "http://localhost:4317"
    otel_service_name: str = "app-ge"

    model_config = {"env_prefix": ""}


settings = Settings()
