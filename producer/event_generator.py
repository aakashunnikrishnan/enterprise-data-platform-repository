import json
import time
from collections.abc import Iterator

from .generators import RetailEventGenerator
from .models import BaseEvent


def generate_events(
    generator: RetailEventGenerator,
    events_per_second: int = 10,
) -> Iterator[BaseEvent]:
    """Generate retail events at the requested rate."""

    interval = 1 / events_per_second

    while True:
        event = generator.generate_order()

        yield event

        time.sleep(interval)


def main() -> None:
    generator = RetailEventGenerator()

    print("Starting synthetic retail event generator...")

    for event in generate_events(generator, events_per_second=5):
        print(json.dumps(event.model_dump(mode="json")))


if __name__ == "__main__":
    main()
