from datetime import UTC, datetime

from microservices.inventory.models import (
    InventoryItem,
    InventoryReservationResponse,
    InventoryResponse,
)
from microservices.inventory.repository import InventoryRepository


class InventoryNotFoundError(Exception):
    pass


class InsufficientInventoryError(Exception):
    pass


class InvalidInventoryOperationError(Exception):
    pass


class InventoryService:
    def __init__(self, repository: InventoryRepository) -> None:
        self.repository = repository

    def get_inventory(
        self,
        product_id: str,
        warehouse_id: str,
    ) -> InventoryResponse:
        item = self.repository.get(
            product_id,
            warehouse_id,
        )

        if item is None:
            raise InventoryNotFoundError(
                f"Inventory not found for product={product_id}, warehouse={warehouse_id}"
            )

        return self._to_response(item)

    def update_inventory(
        self,
        product_id: str,
        warehouse_id: str,
        quantity_change: int,
    ) -> InventoryResponse:
        item = self.repository.get(
            product_id,
            warehouse_id,
        )

        if item is None:
            item = InventoryItem(
                product_id=product_id,
                warehouse_id=warehouse_id,
                quantity_available=0,
            )

        new_quantity = item.quantity_available + quantity_change

        if new_quantity < 0:
            raise InvalidInventoryOperationError("Inventory quantity cannot become negative")

        updated_item = item.model_copy(
            update={
                "quantity_available": new_quantity,
                "updated_at": datetime.now(UTC),
            }
        )

        self.repository.upsert(updated_item)

        return self._to_response(updated_item)

    def reserve_inventory(
        self,
        product_id: str,
        warehouse_id: str,
        quantity: int,
    ) -> InventoryReservationResponse:
        item = self.repository.get(
            product_id,
            warehouse_id,
        )

        if item is None:
            raise InventoryNotFoundError(
                f"Inventory not found for product={product_id}, warehouse={warehouse_id}"
            )

        if quantity > item.quantity_available:
            raise InsufficientInventoryError(
                f"Requested={quantity}, available={item.quantity_available}"
            )

        updated_item = item.model_copy(
            update={
                "quantity_available": (item.quantity_available - quantity),
                "quantity_reserved": (item.quantity_reserved + quantity),
                "updated_at": datetime.now(UTC),
            }
        )

        self.repository.upsert(updated_item)

        return InventoryReservationResponse(
            product_id=product_id,
            warehouse_id=warehouse_id,
            quantity_reserved=updated_item.quantity_reserved,
            quantity_available=updated_item.quantity_available,
        )

    def release_inventory(
        self,
        product_id: str,
        warehouse_id: str,
        quantity: int,
    ) -> InventoryReservationResponse:
        item = self.repository.get(
            product_id,
            warehouse_id,
        )

        if item is None:
            raise InventoryNotFoundError(
                f"Inventory not found for product={product_id}, warehouse={warehouse_id}"
            )

        if quantity > item.quantity_reserved:
            raise InvalidInventoryOperationError("Cannot release more inventory than reserved")

        updated_item = item.model_copy(
            update={
                "quantity_available": (item.quantity_available + quantity),
                "quantity_reserved": (item.quantity_reserved - quantity),
                "updated_at": datetime.now(UTC),
            }
        )

        self.repository.upsert(updated_item)

        return InventoryReservationResponse(
            product_id=product_id,
            warehouse_id=warehouse_id,
            quantity_reserved=updated_item.quantity_reserved,
            quantity_available=updated_item.quantity_available,
        )

    @staticmethod
    def _to_response(item: InventoryItem) -> InventoryResponse:
        return InventoryResponse(
            product_id=item.product_id,
            warehouse_id=item.warehouse_id,
            quantity_available=item.quantity_available,
            quantity_reserved=item.quantity_reserved,
            status=item.status,
            updated_at=item.updated_at,
        )
