from threading import Lock

from microservices.pricing.models import ProductPrice


class PricingRepository:
    """
    Thread-safe in-memory pricing repository.

    The storage implementation can later be replaced with
    PostgreSQL, Cosmos DB, Redis, or another persistent store.
    """

    def __init__(self) -> None:
        self._prices: dict[str, ProductPrice] = {}
        self._lock = Lock()

    def get(self, product_id: str) -> ProductPrice | None:
        with self._lock:
            price = self._prices.get(product_id)

            if price is None:
                return None

            return price.model_copy(deep=True)

    def upsert(self, price: ProductPrice) -> ProductPrice:
        with self._lock:
            self._prices[price.product_id] = price.model_copy(deep=True)

            return self._prices[price.product_id].model_copy(deep=True)

    def delete(self, product_id: str) -> bool:
        with self._lock:
            if product_id not in self._prices:
                return False

            del self._prices[product_id]
            return True

    def clear(self) -> None:
        with self._lock:
            self._prices.clear()
