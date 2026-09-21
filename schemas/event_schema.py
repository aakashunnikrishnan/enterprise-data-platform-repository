from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class EventType(StrEnum):
    ORDER_CREATED = "ORDER_CREATED"
    PAYMENT_COMPLETED = "PAYMENT_COMPLETED"
    INVENTORY_UPDATED = "INVENTORY_UPDATED"
    CUSTOMER_ACTIVITY = "CUSTOMER_ACTIVITY"


class EventEnvelope(BaseModel):
    """
    Common metadata shared by every retail event.
    """

    model_config = ConfigDict(extra="forbid")

    event_id: str = Field(min_length=1)
    event_type: EventType
    event_time: datetime
    source: str = Field(min_length=1)
    version: int = Field(default=1, ge=1)
    environment: Literal["dev", "test", "staging", "prod"] = "dev"
    schema_version: str = Field(default="1.0", min_length=1)


class OrderEventSchema(EventEnvelope):
    event_type: Literal[EventType.ORDER_CREATED] = EventType.ORDER_CREATED

    order_id: str = Field(min_length=1)
    customer_id: str = Field(min_length=1)
    product_id: str = Field(min_length=1)

    quantity: int = Field(ge=1, le=20)
    unit_price: float = Field(gt=0)
    currency: str = Field(default="INR", min_length=3, max_length=3)
    city: str = Field(min_length=1)


class PaymentEventSchema(EventEnvelope):
    event_type: Literal[EventType.PAYMENT_COMPLETED] = EventType.PAYMENT_COMPLETED

    payment_id: str = Field(min_length=1)
    order_id: str = Field(min_length=1)
    customer_id: str = Field(min_length=1)

    amount: float = Field(gt=0)
    currency: str = Field(default="INR", min_length=3, max_length=3)
    payment_method: str = Field(min_length=1)


class InventoryEventSchema(EventEnvelope):
    event_type: Literal[EventType.INVENTORY_UPDATED] = EventType.INVENTORY_UPDATED

    inventory_event_id: str = Field(min_length=1)
    product_id: str = Field(min_length=1)
    warehouse_id: str = Field(min_length=1)

    quantity_change: int
    quantity_available: int = Field(ge=0)


class CustomerActivityEventSchema(EventEnvelope):
    event_type: Literal[EventType.CUSTOMER_ACTIVITY] = EventType.CUSTOMER_ACTIVITY

    activity_id: str = Field(min_length=1)
    customer_id: str = Field(min_length=1)

    activity_type: str = Field(min_length=1)
    product_id: str | None = None
    city: str = Field(min_length=1)
