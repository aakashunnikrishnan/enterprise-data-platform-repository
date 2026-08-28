from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, Field


class EventType(StrEnum):
    ORDER_CREATED = "ORDER_CREATED"
    PAYMENT_COMPLETED = "PAYMENT_COMPLETED"
    INVENTORY_UPDATED = "INVENTORY_UPDATED"
    CUSTOMER_ACTIVITY = "CUSTOMER_ACTIVITY"


class BaseEvent(BaseModel):
    event_id: str
    event_type: EventType
    event_time: datetime

    source: str
    version: int = 1

    environment: str = "dev"
    schema_version: str = "1.0"


class OrderEvent(BaseEvent):
    event_type: EventType = EventType.ORDER_CREATED

    order_id: str
    customer_id: str
    product_id: str

    quantity: int = Field(gt=0, le=20)
    unit_price: Decimal = Field(gt=0)

    currency: str = "INR"
    city: str


class PaymentEvent(BaseEvent):
    event_type: EventType = EventType.PAYMENT_COMPLETED

    payment_id: str
    order_id: str
    customer_id: str

    amount: Decimal = Field(gt=0)
    currency: str = "INR"
    payment_method: str


class InventoryEvent(BaseEvent):
    event_type: EventType = EventType.INVENTORY_UPDATED

    inventory_event_id: str
    product_id: str

    warehouse_id: str
    quantity_change: int
    quantity_available: int = Field(ge=0)


class CustomerActivityEvent(BaseEvent):
    event_type: EventType = EventType.CUSTOMER_ACTIVITY

    activity_id: str
    customer_id: str

    activity_type: str
    product_id: str | None = None
    city: str
