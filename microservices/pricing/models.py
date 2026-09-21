from datetime import UTC, datetime
from decimal import ROUND_HALF_UP, Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class PricingStatus(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class ProductPrice(BaseModel):
    model_config = ConfigDict(extra="forbid")

    product_id: str = Field(min_length=1)

    currency: str = Field(
        default="INR",
        min_length=3,
        max_length=3,
    )

    base_price: Decimal = Field(gt=0)

    discount_percentage: Decimal = Field(
        default=Decimal("0"),
        ge=0,
        le=100,
    )

    status: PricingStatus = PricingStatus.ACTIVE

    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @property
    def final_price(self) -> Decimal:
        discount = self.base_price * self.discount_percentage / Decimal("100")

        final_price = self.base_price - discount

        return final_price.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )


class PriceUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    base_price: Decimal = Field(gt=0)

    discount_percentage: Decimal = Field(
        default=Decimal("0"),
        ge=0,
        le=100,
    )

    currency: str = Field(
        default="INR",
        min_length=3,
        max_length=3,
    )


class PriceResponse(BaseModel):
    product_id: str
    currency: str
    base_price: Decimal
    discount_percentage: Decimal
    final_price: Decimal
    status: PricingStatus
    updated_at: datetime
