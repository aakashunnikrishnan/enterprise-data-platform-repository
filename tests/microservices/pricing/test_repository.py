from decimal import Decimal

from microservices.pricing.models import ProductPrice
from microservices.pricing.repository import PricingRepository


def test_upsert_and_get():
    repository = PricingRepository()

    price = ProductPrice(
        product_id="PROD-001",
        base_price=Decimal("1000.00"),
        discount_percentage=Decimal("10"),
    )

    repository.upsert(price)

    result = repository.get("PROD-001")

    assert result is not None
    assert result.product_id == "PROD-001"
    assert result.base_price == Decimal("1000.00")


def test_get_missing_product():
    repository = PricingRepository()

    assert repository.get("UNKNOWN") is None


def test_delete_product():
    repository = PricingRepository()

    price = ProductPrice(
        product_id="PROD-001",
        base_price=Decimal("1000.00"),
    )

    repository.upsert(price)

    assert repository.delete("PROD-001") is True
    assert repository.get("PROD-001") is None


def test_delete_missing_product():
    repository = PricingRepository()

    assert repository.delete("UNKNOWN") is False
