from decimal import Decimal

from producer.models import EventType


def test_generate_order(generator) -> None:
    event = generator.generate_order()

    assert event.event_type == EventType.ORDER_CREATED
    assert event.source == "web-store"

    assert event.order_id.startswith("ORD-")
    assert event.customer_id.startswith("CUS-")
    assert event.product_id.startswith("PROD-")

    assert 1 <= event.quantity <= 5
    assert event.unit_price > Decimal("0")

    assert event.city in generator.config.cities


def test_generate_payment_is_linked_to_order(generator) -> None:
    order = generator.generate_order()

    payment = generator.generate_payment(order)

    assert payment.event_type == EventType.PAYMENT_COMPLETED
    assert payment.order_id == order.order_id
    assert payment.customer_id == order.customer_id

    expected_amount = order.unit_price * order.quantity

    assert payment.amount == expected_amount
    assert payment.payment_method in generator.config.payment_methods


def test_generate_inventory_is_linked_to_order(generator) -> None:
    order = generator.generate_order()

    inventory = generator.generate_inventory(order)

    assert inventory.event_type == EventType.INVENTORY_UPDATED
    assert inventory.product_id == order.product_id

    assert inventory.quantity_change == -order.quantity
    assert inventory.quantity_available >= 0

    assert inventory.warehouse_id in generator.config.warehouse_ids


def test_generate_customer_activity(generator) -> None:
    event = generator.generate_customer_activity()

    assert event.event_type == EventType.CUSTOMER_ACTIVITY
    assert event.customer_id.startswith("CUS-")

    assert event.activity_type in generator.config.activity_types
    assert event.city in generator.config.cities


def test_event_ids_are_unique(generator) -> None:
    events = [generator.generate_order() for _ in range(1_000)]

    event_ids = [event.event_id for event in events]

    assert len(event_ids) == len(set(event_ids))
