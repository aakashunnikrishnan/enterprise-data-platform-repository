from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class InventoryStatus(StrEnum):
    AVAILABLE = "AVAILABLE"
    LOW_STOCK = "LOW_STOCK"
    OUT_OF_STOCK = "OUT_OF_STOCK"


class InventoryItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    product_id: str = Field(min_length=1)
    warehouse_id: str = Field(min_length=1)

    quantity_available: int = Field(ge=0)
    quantity_reserved: int = Field(default=0, ge=0)

    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @property
    def status(self) -> InventoryStatus:
        if self.quantity_available == 0:
            return InventoryStatus.OUT_OF_STOCK

        if self.quantity_available <= 10:
            return InventoryStatus.LOW_STOCK

        return InventoryStatus.AVAILABLE


class InventoryUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    quantity_change: int


class InventoryResponse(BaseModel):
    product_id: str
    warehouse_id: str
    quantity_available: int
    quantity_reserved: int
    status: InventoryStatus
    updated_at: datetime


class InventoryReservationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    quantity: int = Field(gt=0)


class InventoryReservationResponse(BaseModel):
    product_id: str
    warehouse_id: str
    quantity_reserved: int
    quantity_available: int
