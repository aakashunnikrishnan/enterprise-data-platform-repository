import pytest

from microservices.inventory.repository import InventoryRepository
from microservices.inventory.service import (
    InsufficientInventoryError,
    InvalidInventoryOperationError,
    InventoryNotFoundError,
    InventoryService,
)


@pytest.fixture
def repository():
    return InventoryRepository()


@pytest.fixture
def service(repository):
    return InventoryService(repository)


def test_update_inventory(service):
    result = service.update_inventory(
        "PROD-001",
        "WH-BLR-01",
        100,
    )

    assert result.product_id == "PROD-001"
    assert result.quantity_available == 100
    assert result.quantity_reserved == 0
    assert result.status == "AVAILABLE"


def test_get_inventory(service):
    service.update_inventory(
        "PROD-001",
        "WH-BLR-01",
        100,
    )

    result = service.get_inventory(
        "PROD-001",
        "WH-BLR-01",
    )

    assert result.quantity_available == 100


def test_missing_inventory(service):
    with pytest.raises(InventoryNotFoundError):
        service.get_inventory(
            "PROD-001",
            "WH-BLR-01",
        )


def test_reserve_inventory(service):
    service.update_inventory(
        "PROD-001",
        "WH-BLR-01",
        100,
    )

    result = service.reserve_inventory(
        "PROD-001",
        "WH-BLR-01",
        30,
    )

    assert result.quantity_available == 70
    assert result.quantity_reserved == 30


def test_reservation_cannot_exceed_inventory(service):
    service.update_inventory(
        "PROD-001",
        "WH-BLR-01",
        10,
    )

    with pytest.raises(InsufficientInventoryError):
        service.reserve_inventory(
            "PROD-001",
            "WH-BLR-01",
            20,
        )


def test_release_inventory(service):
    service.update_inventory(
        "PROD-001",
        "WH-BLR-01",
        100,
    )

    service.reserve_inventory(
        "PROD-001",
        "WH-BLR-01",
        30,
    )

    result = service.release_inventory(
        "PROD-001",
        "WH-BLR-01",
        10,
    )

    assert result.quantity_available == 80
    assert result.quantity_reserved == 20


def test_inventory_cannot_become_negative(service):
    with pytest.raises(InvalidInventoryOperationError):
        service.update_inventory(
            "PROD-001",
            "WH-BLR-01",
            -10,
        )
