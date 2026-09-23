import os
from dataclasses import dataclass


@dataclass(frozen=True)
class FraudConfig:
    high_value_threshold: int = int(
        os.getenv(
            "HIGH_VALUE_THRESHOLD",
            "100000",
        )
    )

    velocity_threshold: int = int(
        os.getenv(
            "VELOCITY_THRESHOLD",
            "10",
        )
    )

    velocity_amount_threshold: int = int(
        os.getenv(
            "VELOCITY_AMOUNT_THRESHOLD",
            "500000",
        )
    )

    suspicious_payment_methods: tuple[str, ...] = (
        "PREPAID_CARD",
        "ANONYMOUS_WALLET",
    )

    medium_risk_threshold: int = int(
        os.getenv(
            "MEDIUM_RISK_THRESHOLD",
            "30",
        )
    )

    high_risk_threshold: int = int(
        os.getenv(
            "HIGH_RISK_THRESHOLD",
            "70",
        )
    )
