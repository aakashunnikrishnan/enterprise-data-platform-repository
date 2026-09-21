import os
from dataclasses import dataclass


@dataclass(frozen=True)
class PricingConfig:
    service_name: str = os.getenv(
        "SERVICE_NAME",
        "pricing-service",
    )

    environment: str = os.getenv(
        "ENVIRONMENT",
        "dev",
    )

    log_level: str = os.getenv(
        "LOG_LEVEL",
        "INFO",
    )

    default_currency: str = os.getenv(
        "DEFAULT_CURRENCY",
        "INR",
    )
