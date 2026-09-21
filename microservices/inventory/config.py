import os
from dataclasses import dataclass


@dataclass(frozen=True)
class InventoryConfig:
    service_name: str = os.getenv(
        "SERVICE_NAME",
        "inventory-service",
    )

    environment: str = os.getenv(
        "ENVIRONMENT",
        "dev",
    )

    log_level: str = os.getenv(
        "LOG_LEVEL",
        "INFO",
    )

    low_stock_threshold: int = int(
        os.getenv(
            "LOW_STOCK_THRESHOLD",
            "10",
        )
    )
