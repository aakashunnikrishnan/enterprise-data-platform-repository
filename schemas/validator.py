from typing import Any

from pydantic import ValidationError

from schemas.event_schema import (
    CustomerActivityEventSchema,
    EventEnvelope,
    InventoryEventSchema,
    OrderEventSchema,
    PaymentEventSchema,
)


class EventValidationError(ValueError):
    """Raised when an event does not conform to the expected schema."""


EVENT_SCHEMA_MAP = {
    "ORDER_CREATED": OrderEventSchema,
    "PAYMENT_COMPLETED": PaymentEventSchema,
    "INVENTORY_UPDATED": InventoryEventSchema,
    "CUSTOMER_ACTIVITY": CustomerActivityEventSchema,
}


def validate_event(event: dict[str, Any]) -> EventEnvelope:
    """Validate an incoming event against its event schema."""

    event_type = event.get("event_type")

    if event_type not in EVENT_SCHEMA_MAP:
        raise EventValidationError(f"Unsupported event type: {event_type}")

    schema_class = EVENT_SCHEMA_MAP[event_type]

    try:
        return schema_class.model_validate(event)
    except ValidationError as exc:
        raise EventValidationError(f"Event validation failed for {event_type}: {exc}") from exc
