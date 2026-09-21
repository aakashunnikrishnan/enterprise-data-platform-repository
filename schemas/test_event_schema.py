from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from schemas.event_schema import (
    CustomerActivityEventSchema,
    InventoryEventSchema,
    OrderEventSchema,
    PaymentEventSchema,
)


def base_event() -> dict:
    return {
        "event_id": "evt-001",
        "event_time": datetime.now(UTC),
        "source": "test",
        "version": 1,
        "environment": "test",
        "schema_version": "1.0",
    }


def test_valid_order_event():
    event = {
        **base_event(),
        "event_type": "ORDER_CREATED",
        "order_id": "ORD-001",
        "customer_id": "CUS-001",
        "product_id": "PROD-001",
        "quantity": 2,
        "unit_price": 999.99,
        "currency": "INR",
        "city": "Bangalore",
    }

    result = OrderEventSchema.model_validate(event)

    assert result.order_id == "ORD-001"
    assert result.quantity == 2


def test_order_rejects_invalid_quantity():
    event = {
        **base_event(),
        "event_type": "ORDER_CREATED",
        "order_id": "ORD-001",
        "customer_id": "CUS-001",
        "product_id": "PROD-001",
        "quantity": 0,
        "unit_price": 999.99,
        "currency": "INR",
        "city": "Bangalore",
    }

    with pytest.raises(ValidationError):
        OrderEventSchema.model_validate(event)


def test_order_rejects_unknown_fields():
    event = {
        **base_event(),
        "event_type": "ORDER_CREATED",
        "order_id": "ORD-001",
        "customer_id": "CUS-001",
        "product_id": "PROD-001",
        "quantity": 2,
        "unit_price": 999.99,
        "currency": "INR",
        "city": "Bangalore",
        "unknown_field": "should_fail",
    }

    with pytest.raises(ValidationError):
        OrderEventSchema.model_validate(event)


def test_valid_payment_event():
    event = {
        **base_event(),
        "event_type": "PAYMENT_COMPLETED",
        "payment_id": "PAY-001",
        "order_id": "ORD-001",
        "customer_id": "CUS-001",
        "amount": 1999.99,
        "currency": "INR",
        "payment_method": "UPI",
    }

    result = PaymentEventSchema.model_validate(event)

    assert result.payment_id == "PAY-001"
    assert result.amount == 1999.99


def test_valid_inventory_event():
    event = {
        **base_event(),
        "event_type": "INVENTORY_UPDATED",
        "inventory_event_id": "INV-001",
        "product_id": "PROD-001",
        "warehouse_id": "WH-BLR-01",
        "quantity_change": -5,
        "quantity_available": 95,
    }

    result = InventoryEventSchema.model_validate(event)

    assert result.quantity_change == -5
    assert result.quantity_available == 95


def test_inventory_rejects_negative_available_quantity():
    event = {
        **base_event(),
        "event_type": "INVENTORY_UPDATED",
        "inventory_event_id": "INV-001",
        "product_id": "PROD-001",
        "warehouse_id": "WH-BLR-01",
        "quantity_change": -5,
        "quantity_available": -1,
    }

    with pytest.raises(ValidationError):
        InventoryEventSchema.model_validate(event)


def test_valid_customer_activity_event():
    event = {
        **base_event(),
        "event_type": "CUSTOMER_ACTIVITY",
        "activity_id": "ACT-001",
        "customer_id": "CUS-001",
        "activity_type": "PRODUCT_VIEW",
        "product_id": "PROD-001",
        "city": "Bangalore",
    }

    result = CustomerActivityEventSchema.model_validate(event)

    assert result.activity_type == "PRODUCT_VIEW"
