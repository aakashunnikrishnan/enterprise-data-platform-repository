import logging
import os
import time
from collections.abc import Iterator

from .generators import RetailEventGenerator
from .kafka_config import KafkaConfig
from .kafka_producer import RetailKafkaProducer
from .models import BaseEvent

logger = logging.getLogger(__name__)


def generate_events(
    generator: RetailEventGenerator,
    events_per_second: int = 10,
) -> Iterator[BaseEvent]:
    """Generate retail events at the requested rate."""

    if events_per_second <= 0:
        raise ValueError("events_per_second must be greater than zero")

    interval = 1 / events_per_second

    while True:
        yield generator.generate_order()
        time.sleep(interval)


def main() -> None:
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )

    events_per_second = int(os.getenv("EVENTS_PER_SECOND", "5"))

    generator = RetailEventGenerator()
    kafka_producer = RetailKafkaProducer(KafkaConfig())

    logger.info(
        "Starting retail event producer at %s events/sec",
        events_per_second,
    )

    try:
        for event in generate_events(
            generator,
            events_per_second,
        ):
            kafka_producer.publish(event)

            logger.debug(
                "Published event: id=%s type=%s",
                event.event_id,
                event.event_type,
            )

    except KeyboardInterrupt:
        logger.info("Shutdown requested")

    finally:
        logger.info("Flushing outstanding Kafka messages")

        remaining = kafka_producer.flush()

        if remaining:
            logger.warning(
                "%s Kafka messages were not delivered",
                remaining,
            )

        logger.info("Producer shutdown complete")


if __name__ == "__main__":
    main()
