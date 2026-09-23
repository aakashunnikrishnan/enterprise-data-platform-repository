from fastapi.testclient import TestClient

from microservices.fraud.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    assert response.json()["status"] == "healthy"


def test_readiness():
    response = client.get("/ready")

    assert response.status_code == 200

    assert response.json()["status"] == "ready"


def test_low_risk_payment():
    response = client.post(
        "/api/v1/fraud/score",
        json={
            "payment_id": "PAY-001",
            "order_id": "ORD-001",
            "customer_id": "CUS-001",
            "amount": "1000",
            "currency": "INR",
            "payment_method": "UPI",
            "customer_transaction_count": 1,
            "customer_transaction_amount": "1000",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["fraud_score"] == 0
    assert body["risk_level"] == "LOW"
    assert body["decision"] == "APPROVE"


def test_high_risk_payment():
    response = client.post(
        "/api/v1/fraud/score",
        json={
            "payment_id": "PAY-002",
            "order_id": "ORD-002",
            "customer_id": "CUS-002",
            "amount": "150000",
            "currency": "INR",
            "payment_method": "PREPAID_CARD",
            "customer_transaction_count": 15,
            "customer_transaction_amount": "600000",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["fraud_score"] == 100
    assert body["risk_level"] == "HIGH"
    assert body["decision"] == "BLOCK"


def test_invalid_payment():
    response = client.post(
        "/api/v1/fraud/score",
        json={
            "payment_id": "PAY-003",
            "order_id": "ORD-003",
            "customer_id": "CUS-003",
            "amount": "-100",
            "currency": "INR",
            "payment_method": "UPI",
        },
    )

    assert response.status_code == 422
