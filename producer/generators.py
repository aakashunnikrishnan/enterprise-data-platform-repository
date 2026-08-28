import random
import uuid
from datetime import UTC, datetime
from decimal import Decimal

from .config import GeneratorConfig
from .models import (
    CustomerActivityEvent,
    InventoryEvent,
    OrderEvent,
    PaymentEvent,
)


class RetailEventGenerator:
    """Generate realistic synthetic retail events."""

    def __init__(self, config: GeneratorConfig | None = None) -> None:
        self.config = config or GeneratorConfig()

    @staticmethod
    def _event_id() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def _now() -> datetime:
        return datetime.now(UTC)

    def generate_order(self) -> OrderEvent:
        quantity = random.randint(1, 5)
        unit_price = Decimal(str(random.randint(100, 10_000)))

        return OrderEvent(
            event_id=self._event_id(),
            event_time=self._now(),
            source="web-store",
            order_id=f"ORD-{uuid.uuid4().hex[:12].upper()}",
            customer_id=f"CUS-{random.randint(1, self.config.customer_count):06d}",
            product_id=f"PROD-{random.randint(1, self.config.product_count):05d}",
            quantity=quantity,
            unit_price=unit_price,
            city=random.choice(self.config.cities),
        )

    def generate_payment(self, order: OrderEvent) -> PaymentEvent:
        amount = order.unit_price * order.quantity

        return PaymentEvent(
            event_id=self._event_id(),
            event_time=self._now(),
            source="payment-service",
            payment_id=f"PAY-{uuid.uuid4().hex[:12].upper()}",
            order_id=order.order_id,
            customer_id=order.customer_id,
            amount=amount,
            payment_method=random.choice(self.config.payment_methods),
        )

    def generate_inventory(self, order: OrderEvent) -> InventoryEvent:
        quantity_change = -order.quantity

        return InventoryEvent(
            event_id=self._event_id(),
            event_time=self._now(),
            source="inventory-system",
            inventory_event_id=f"INV-{uuid.uuid4().hex[:12].upper()}",
            product_id=order.product_id,
            warehouse_id=random.choice(self.config.warehouse_ids),
            quantity_change=quantity_change,
            quantity_available=random.randint(0, 1_000),
        )

    def generate_customer_activity(self) -> CustomerActivityEvent:
        activity_type = random.choice(self.config.activity_types)

        return CustomerActivityEvent(
            event_id=self._event_id(),
            event_time=self._now(),
            source="customer-web-app",
            activity_id=f"ACT-{uuid.uuid4().hex[:12].upper()}",
            customer_id=f"CUS-{random.randint(1, self.config.customer_count):06d}",
            activity_type=activity_type,
            product_id=(
                f"PROD-{random.randint(1, self.config.product_count):05d}"
                if activity_type != "SEARCH"
                else None
            ),
            city=random.choice(self.config.cities),
        )
