from fastapi.testclient import TestClient

from microservices.pricing.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_readiness():
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_create_price():
    response = client.put(
        "/api/v1/pricing/PROD-100",
        json={
            "base_price": "1999.99",
            "discount_percentage": "10",
            "currency": "INR",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["product_id"] == "PROD-100"
    assert body["currency"] == "INR"
    assert body["final_price"] == "1799.99"


def test_get_price():
    client.put(
        "/api/v1/pricing/PROD-200",
        json={
            "base_price": "1000.00",
            "discount_percentage": "20",
            "currency": "INR",
        },
    )

    response = client.get("/api/v1/pricing/PROD-200")

    assert response.status_code == 200
    assert response.json()["final_price"] == "800.00"


def test_missing_price():
    response = client.get("/api/v1/pricing/UNKNOWN")

    assert response.status_code == 404


def test_deactivate_price():
    client.put(
        "/api/v1/pricing/PROD-300",
        json={
            "base_price": "500.00",
            "discount_percentage": "0",
            "currency": "INR",
        },
    )

    response = client.delete("/api/v1/pricing/PROD-300")

    assert response.status_code == 200
    assert response.json()["status"] == "INACTIVE"
