import os
from dataclasses import dataclass


@dataclass(frozen=True)
class KafkaConfig:
    bootstrap_servers: str = os.getenv(
        "KAFKA_BOOTSTRAP_SERVERS",
        "localhost:9092",
    )

    client_id: str = os.getenv(
        "KAFKA_CLIENT_ID",
        "retail-event-producer",
    )

    acks: str = os.getenv(
        "KAFKA_ACKS",
        "all",
    )

    retries: int = int(
        os.getenv(
            "KAFKA_RETRIES",
            "10",
        )
    )

    batch_size: int = int(
        os.getenv(
            "KAFKA_BATCH_SIZE",
            "65536",
        )
    )

    linger_ms: int = int(
        os.getenv(
            "KAFKA_LINGER_MS",
            "10",
        )
    )

    compression_type: str = os.getenv(
        "KAFKA_COMPRESSION_TYPE",
        "lz4",
    )

    enable_idempotence: bool = (
        os.getenv(
            "KAFKA_ENABLE_IDEMPOTENCE",
            "true",
        ).lower()
        == "true"
    )

    topic_orders: str = os.getenv(
        "KAFKA_TOPIC_ORDERS",
        "orders",
    )

    topic_payments: str = os.getenv(
        "KAFKA_TOPIC_PAYMENTS",
        "payments",
    )

    topic_inventory: str = os.getenv(
        "KAFKA_TOPIC_INVENTORY",
        "inventory",
    )

    topic_customer_activity: str = os.getenv(
        "KAFKA_TOPIC_CUSTOMER_ACTIVITY",
        "customer_activity",
    )

    def topics(self) -> tuple[str, ...]:
        return (
            self.topic_orders,
            self.topic_payments,
            self.topic_inventory,
            self.topic_customer_activity,
        )
