from datetime import UTC, datetime
from decimal import Decimal

from microservices.pricing.models import (
    PriceResponse,
    PricingStatus,
    ProductPrice,
)
from microservices.pricing.repository import PricingRepository


class PriceNotFoundError(Exception):
    pass


class InvalidPricingOperationError(Exception):
    pass


class PricingService:
    def __init__(self, repository: PricingRepository) -> None:
        self.repository = repository

    def get_price(
        self,
        product_id: str,
    ) -> PriceResponse:
        price = self.repository.get(product_id)

        if price is None:
            raise PriceNotFoundError(f"Price not found for product={product_id}")

        return self._to_response(price)

    def create_or_update_price(
        self,
        product_id: str,
        base_price: Decimal,
        discount_percentage: Decimal,
        currency: str,
    ) -> PriceResponse:
        price = ProductPrice(
            product_id=product_id,
            base_price=base_price,
            discount_percentage=discount_percentage,
            currency=currency.upper(),
            status=PricingStatus.ACTIVE,
            updated_at=datetime.now(UTC),
        )

        self.repository.upsert(price)

        return self._to_response(price)

    def deactivate_price(
        self,
        product_id: str,
    ) -> PriceResponse:
        price = self.repository.get(product_id)

        if price is None:
            raise PriceNotFoundError(f"Price not found for product={product_id}")

        updated_price = price.model_copy(
            update={
                "status": PricingStatus.INACTIVE,
                "updated_at": datetime.now(UTC),
            }
        )

        self.repository.upsert(updated_price)

        return self._to_response(updated_price)

    @staticmethod
    def _to_response(
        price: ProductPrice,
    ) -> PriceResponse:
        return PriceResponse(
            product_id=price.product_id,
            currency=price.currency,
            base_price=price.base_price,
            discount_percentage=price.discount_percentage,
            final_price=price.final_price,
            status=price.status,
            updated_at=price.updated_at,
        )
