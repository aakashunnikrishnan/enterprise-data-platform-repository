from fastapi import APIRouter, HTTPException, status

from microservices.inventory.models import (
    InventoryReservationRequest,
    InventoryReservationResponse,
    InventoryResponse,
    InventoryUpdateRequest,
)
from microservices.inventory.service import (
    InsufficientInventoryError,
    InvalidInventoryOperationError,
    InventoryNotFoundError,
    InventoryService,
)


def create_router(service: InventoryService) -> APIRouter:
    router = APIRouter(
        prefix="/api/v1/inventory",
        tags=["inventory"],
    )

    @router.get(
        "/{product_id}/{warehouse_id}",
        response_model=InventoryResponse,
    )
    def get_inventory(
        product_id: str,
        warehouse_id: str,
    ) -> InventoryResponse:
        try:
            return service.get_inventory(
                product_id,
                warehouse_id,
            )
        except InventoryNotFoundError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc

    @router.post(
        "/{product_id}/{warehouse_id}/update",
        response_model=InventoryResponse,
    )
    def update_inventory(
        product_id: str,
        warehouse_id: str,
        request: InventoryUpdateRequest,
    ) -> InventoryResponse:
        try:
            return service.update_inventory(
                product_id,
                warehouse_id,
                request.quantity_change,
            )

        except InvalidInventoryOperationError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            ) from exc

    @router.post(
        "/{product_id}/{warehouse_id}/reserve",
        response_model=InventoryReservationResponse,
    )
    def reserve_inventory(
        product_id: str,
        warehouse_id: str,
        request: InventoryReservationRequest,
    ) -> InventoryReservationResponse:
        try:
            return service.reserve_inventory(
                product_id,
                warehouse_id,
                request.quantity,
            )

        except InventoryNotFoundError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc

        except InsufficientInventoryError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(exc),
            ) from exc

    @router.post(
        "/{product_id}/{warehouse_id}/release",
        response_model=InventoryReservationResponse,
    )
    def release_inventory(
        product_id: str,
        warehouse_id: str,
        request: InventoryReservationRequest,
    ) -> InventoryReservationResponse:
        try:
            return service.release_inventory(
                product_id,
                warehouse_id,
                request.quantity,
            )

        except InventoryNotFoundError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc

        except InvalidInventoryOperationError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            ) from exc

    return router
