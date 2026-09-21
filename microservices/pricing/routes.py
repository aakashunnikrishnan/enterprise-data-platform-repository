from fastapi import APIRouter, HTTPException, status

from microservices.pricing.models import (
    PriceResponse,
    PriceUpdateRequest,
)
from microservices.pricing.service import (
    PriceNotFoundError,
    PricingService,
)


def create_router(service: PricingService) -> APIRouter:
    router = APIRouter(
        prefix="/api/v1/pricing",
        tags=["pricing"],
    )

    @router.get(
        "/{product_id}",
        response_model=PriceResponse,
    )
    def get_price(
        product_id: str,
    ) -> PriceResponse:
        try:
            return service.get_price(product_id)

        except PriceNotFoundError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc

    @router.put(
        "/{product_id}",
        response_model=PriceResponse,
    )
    def update_price(
        product_id: str,
        request: PriceUpdateRequest,
    ) -> PriceResponse:
        return service.create_or_update_price(
            product_id=product_id,
            base_price=request.base_price,
            discount_percentage=request.discount_percentage,
            currency=request.currency,
        )

    @router.delete(
        "/{product_id}",
        response_model=PriceResponse,
    )
    def deactivate_price(
        product_id: str,
    ) -> PriceResponse:
        try:
            return service.deactivate_price(product_id)

        except PriceNotFoundError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc

    return router
