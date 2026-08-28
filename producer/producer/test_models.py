import pytest
from pydantic import ValidationError

from producer.models import OrderEvent


def test_order_rejects_negative_quantity() -> None:
    with pytest.raises(ValidationError):
        OrderEvent(
            event_id="event-1",
            event_time="2026-08-28T10:00:00Z",
            source="test",
            order_id="ORD-1",
            customer_id="CUS-1",
            product_id="PROD-1",
            quantity=-1,
            unit_price=100,
            city="Bangalore",
        )


def test_order_rejects_zero_price() -> None:
    with pytest.raises(ValidationError):
        OrderEvent(
            event_id="event-1",
            event_time="2026-08-28T10:00:00Z",
            source="test",
            order_id="ORD-1",
            customer_id="CUS-1",
            product_id="PROD-1",
            quantity=1,
            unit_price=0,
            city="Bangalore",
        )


def test_order_rejects_excessive_quantity() -> None:
    with pytest.raises(ValidationError):
        OrderEvent(
            event_id="event-1",
            event_time="2026-08-28T10:00:00Z",
            source="test",
            order_id="ORD-1",
            customer_id="CUS-1",
            product_id="PROD-1",
            quantity=21,
            unit_price=100,
            city="Bangalore",
        )
