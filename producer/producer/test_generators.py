from decimal import Decimal

from producer.generators import RetailEventGenerator
from producer.models import EventType


def test_generate_order() -> None:
    generator = RetailEventGenerator()

    event = generator.generate_order()

    assert event.event_type == EventType.ORDER_CREATED
    assert event.order_id.startswith("ORD-")
    assert event.customer_id.startswith("CUS-")
    assert event.product_id.startswith("PROD-")
    assert event.quantity > 0
    assert event.unit_price > Decimal("0")


def test_generate_payment_from_order() -> None:
    generator = RetailEventGenerator()

    order = generator.generate_order()
    payment = generator.generate_payment(order)

    assert payment.event_type == EventType.PAYMENT_COMPLETED
    assert payment.order_id == order.order_id
    assert payment.customer_id == order.customer_id
    assert payment.amount == order.unit_price * order.quantity


def test_generate_inventory_from_order() -> None:
    generator = RetailEventGenerator()

    order = generator.generate_order()
    inventory = generator.generate_inventory(order)

    assert inventory.event_type == EventType.INVENTORY_UPDATED
    assert inventory.product_id == order.product_id
    assert inventory.quantity_change == -order.quantity


def test_generate_customer_activity() -> None:
    generator = RetailEventGenerator()

    event = generator.generate_customer_activity()

    assert event.event_type == EventType.CUSTOMER_ACTIVITY
    assert event.customer_id.startswith("CUS-")
    assert event.activity_type
