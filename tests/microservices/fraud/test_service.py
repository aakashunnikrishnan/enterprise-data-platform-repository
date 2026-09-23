from decimal import Decimal

import pytest

from microservices.fraud.models import (
    FraudDecision,
    PaymentRequest,
    RiskLevel,
)
from microservices.fraud.rules import FraudRulesEngine
from microservices.fraud.service import FraudDetectionService


@pytest.fixture
def service():
    return FraudDetectionService(FraudRulesEngine())


def make_payment(
    amount: str = "1000",
    transaction_count: int = 1,
    transaction_amount: str = "1000",
    payment_method: str = "UPI",
) -> PaymentRequest:
    return PaymentRequest(
        payment_id="PAY-001",
        order_id="ORD-001",
        customer_id="CUS-001",
        amount=Decimal(amount),
        currency="INR",
        payment_method=payment_method,
        customer_transaction_count=transaction_count,
        customer_transaction_amount=Decimal(transaction_amount),
    )


def test_low_risk_payment(service):
    result = service.evaluate(make_payment())

    assert result.fraud_score == 0
    assert result.risk_level == RiskLevel.LOW
    assert result.decision == FraudDecision.APPROVE


def test_medium_risk_payment(service):
    result = service.evaluate(make_payment(amount="150000"))

    assert result.fraud_score == 40
    assert result.risk_level == RiskLevel.MEDIUM
    assert result.decision == FraudDecision.REVIEW


def test_high_risk_payment(service):
    result = service.evaluate(
        make_payment(
            amount="150000",
            transaction_count=15,
            payment_method="PREPAID_CARD",
        )
    )

    assert result.fraud_score == 100
    assert result.risk_level == RiskLevel.HIGH
    assert result.decision == FraudDecision.BLOCK
