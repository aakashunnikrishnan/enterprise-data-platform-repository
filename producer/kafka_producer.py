import json
import logging
from collections.abc import Callable

from confluent_kafka import Producer

from .kafka_config import KafkaConfig
from .models import (
    BaseEvent,
    CustomerActivityEvent,
    InventoryEvent,
    OrderEvent,
    PaymentEvent,
)

logger = logging.getLogger(__name__)


class RetailKafkaProducer:
    """Kafka producer for retail domain events."""

    def __init__(
        self,
        config: KafkaConfig | None = None,
        kafka_client: Producer | None = None,
    ) -> None:
        self.config = config or KafkaConfig()

        if kafka_client is not None:
            self._producer = kafka_client
            return

        self._producer = Producer(
            {
                "bootstrap.servers": self.config.bootstrap_servers,
                "client.id": self.config.client_id,
                "acks": self.config.acks,
                "retries": self.config.retries,
                "batch.size": self.config.batch_size,
                "linger.ms": self.config.linger_ms,
                "compression.type": self.config.compression_type,
                "enable.idempotence": self.config.enable_idempotence,
            }
        )

    def _delivery_callback(self, error, message) -> None:
        """Handle Kafka delivery result."""

        if error is not None:
            logger.error(
                "Kafka delivery failed: topic=%s partition=%s error=%s",
                message.topic(),
                message.partition(),
                error,
            )
            return

        logger.debug(
            "Kafka delivery succeeded: topic=%s partition=%s offset=%s",
            message.topic(),
            message.partition(),
            message.offset(),
        )

    @staticmethod
    def _serialize(event: BaseEvent) -> bytes:
        """Serialize event to UTF-8 encoded JSON."""

        return json.dumps(
            event.model_dump(mode="json"),
            separators=(",", ":"),
        ).encode("utf-8")

    @staticmethod
    def _topic_for_event(
        event: BaseEvent,
        config: KafkaConfig,
    ) -> str:
        """Map event type to Kafka topic."""

        if isinstance(event, OrderEvent):
            return config.topic_orders

        if isinstance(event, PaymentEvent):
            return config.topic_payments

        if isinstance(event, InventoryEvent):
            return config.topic_inventory

        if isinstance(event, CustomerActivityEvent):
            return config.topic_customer_activity

        raise ValueError(f"Unsupported event type: {type(event).__name__}")

    @staticmethod
    def _key_for_event(event: BaseEvent) -> str:
        """Return a stable Kafka partition key."""

        if isinstance(event, OrderEvent):
            return event.order_id

        if isinstance(event, PaymentEvent):
            return event.order_id

        if isinstance(event, InventoryEvent):
            return event.product_id

        if isinstance(event, CustomerActivityEvent):
            return event.customer_id

        raise ValueError(f"Unsupported event type: {type(event).__name__}")

    def publish(
        self,
        event: BaseEvent,
        on_delivery: Callable | None = None,
    ) -> None:
        """Publish a domain event to Kafka."""

        topic = self._topic_for_event(
            event,
            self.config,
        )

        key = self._key_for_event(event)

        payload = self._serialize(event)

        callback = on_delivery if on_delivery is not None else self._delivery_callback

        self._producer.produce(
            topic=topic,
            key=key.encode("utf-8"),
            value=payload,
            callback=callback,
        )

        # Process delivery callbacks without blocking.
        self._producer.poll(0)

    def flush(self, timeout: float = 10.0) -> int:
        """Wait for outstanding messages to be delivered."""

        return self._producer.flush(timeout)
