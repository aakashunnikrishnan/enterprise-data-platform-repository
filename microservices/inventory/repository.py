from threading import Lock

from microservices.inventory.models import InventoryItem


class InventoryRepository:
    """
    Thread-safe in-memory inventory repository.

    This repository is intentionally isolated behind an interface-like
    class so that it can later be replaced with Redis, Cosmos DB,
    PostgreSQL, or another persistent store.
    """

    def __init__(self) -> None:
        self._items: dict[tuple[str, str], InventoryItem] = {}
        self._lock = Lock()

    def get(
        self,
        product_id: str,
        warehouse_id: str,
    ) -> InventoryItem | None:
        key = (product_id, warehouse_id)

        with self._lock:
            item = self._items.get(key)

            if item is None:
                return None

            return item.model_copy(deep=True)

    def upsert(self, item: InventoryItem) -> InventoryItem:
        key = (item.product_id, item.warehouse_id)

        with self._lock:
            self._items[key] = item.model_copy(deep=True)

            return self._items[key].model_copy(deep=True)

    def delete(
        self,
        product_id: str,
        warehouse_id: str,
    ) -> bool:
        key = (product_id, warehouse_id)

        with self._lock:
            if key not in self._items:
                return False

            del self._items[key]
            return True

    def clear(self) -> None:
        with self._lock:
            self._items.clear()
