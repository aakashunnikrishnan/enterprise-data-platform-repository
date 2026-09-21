from fastapi.testclient import TestClient

from microservices.inventory.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_readiness():
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_create_inventory():
    response = client.post(
        "/api/v1/inventory/PROD-100/WH-BLR-01/update",
        json={
            "quantity_change": 100,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["product_id"] == "PROD-100"
    assert body["quantity_available"] >= 100


def test_reserve_inventory():
    client.post(
        "/api/v1/inventory/PROD-200/WH-BLR-01/update",
        json={
            "quantity_change": 100,
        },
    )

    response = client.post(
        "/api/v1/inventory/PROD-200/WH-BLR-01/reserve",
        json={
            "quantity": 25,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["quantity_available"] == 75
    assert body["quantity_reserved"] == 25


def test_insufficient_inventory():
    client.post(
        "/api/v1/inventory/PROD-300/WH-BLR-01/update",
        json={
            "quantity_change": 10,
        },
    )

    response = client.post(
        "/api/v1/inventory/PROD-300/WH-BLR-01/reserve",
        json={
            "quantity": 20,
        },
    )

    assert response.status_code == 409
