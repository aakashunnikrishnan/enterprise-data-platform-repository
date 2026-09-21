import pytest

from schemas.event_schema import OrderEventSchema
from schemas.validator import EventValidationError, validate_event


def valid_order() -> dict:
    return {
        "event_id": "evt-001",
        "event_type": "ORDER_CREATED",
        "event_time": "2026-09-20T10:00:00Z",
        "source": "retail-event-generator",
        "version": 1,
        "environment": "test",
        "schema_version": "1.0",
        "order_id": "ORD-001",
        "customer_id": "CUS-001",
        "product_id": "PROD-001",
        "quantity": 2,
        "unit_price": 999.99,
        "currency": "INR",
        "city": "Bangalore",
    }


def test_validate_event_returns_correct_schema():
    result = validate_event(valid_order())

    assert isinstance(result, OrderEventSchema)
    assert result.order_id == "ORD-001"


def test_validate_event_rejects_invalid_event():
    event = valid_order()
    event["quantity"] = 0

    with pytest.raises(EventValidationError):
        validate_event(event)


def test_validate_event_rejects_unknown_event_type():
    event = valid_order()
    event["event_type"] = "UNKNOWN_EVENT"

    with pytest.raises(EventValidationError):
        validate_event(event)
