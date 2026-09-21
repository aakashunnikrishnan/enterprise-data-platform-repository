from decimal import Decimal

import pytest
from pydantic import ValidationError

from microservices.pricing.models import ProductPrice
from microservices.pricing.repository import PricingRepository
from microservices.pricing.service import (
    PriceNotFoundError,
    PricingService,
)


@pytest.fixture
def repository():
    return PricingRepository()


@pytest.fixture
def service(repository):
    return PricingService(repository)


def test_create_price(service):
    result = service.create_or_update_price(
        product_id="PROD-001",
        base_price=Decimal("1000.00"),
        discount_percentage=Decimal("10"),
        currency="INR",
    )

    assert result.product_id == "PROD-001"
    assert result.base_price == Decimal("1000.00")
    assert result.discount_percentage == Decimal("10")
    assert result.final_price == Decimal("900.00")
    assert result.currency == "INR"


def test_get_price(service):
    service.create_or_update_price(
        product_id="PROD-001",
        base_price=Decimal("2000.00"),
        discount_percentage=Decimal("20"),
        currency="INR",
    )

    result = service.get_price("PROD-001")

    assert result.final_price == Decimal("1600.00")


def test_missing_price(service):
    with pytest.raises(PriceNotFoundError):
        service.get_price("UNKNOWN")


def test_update_price(service):
    service.create_or_update_price(
        product_id="PROD-001",
        base_price=Decimal("1000.00"),
        discount_percentage=Decimal("10"),
        currency="INR",
    )

    result = service.create_or_update_price(
        product_id="PROD-001",
        base_price=Decimal("1500.00"),
        discount_percentage=Decimal("20"),
        currency="INR",
    )

    assert result.base_price == Decimal("1500.00")
    assert result.final_price == Decimal("1200.00")


def test_deactivate_price(service):
    service.create_or_update_price(
        product_id="PROD-001",
        base_price=Decimal("1000.00"),
        discount_percentage=Decimal("0"),
        currency="INR",
    )

    result = service.deactivate_price("PROD-001")

    assert result.status == "INACTIVE"


def test_negative_price_rejected():
    with pytest.raises(ValidationError):
        ProductPrice(
            product_id="PROD-001",
            base_price=Decimal("-100"),
        )


def test_discount_above_100_rejected():
    with pytest.raises(ValidationError):
        ProductPrice(
            product_id="PROD-001",
            base_price=Decimal("1000"),
            discount_percentage=Decimal("101"),
        )


def test_final_price_calculation():
    price = ProductPrice(
        product_id="PROD-001",
        base_price=Decimal("999.99"),
        discount_percentage=Decimal("15"),
    )

    assert price.final_price == Decimal("849.99")
