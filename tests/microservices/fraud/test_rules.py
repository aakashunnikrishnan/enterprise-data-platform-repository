from decimal import Decimal

from microservices.fraud.models import PaymentRequest
from microservices.fraud.rules import FraudRulesEngine


def payment(
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


def test_normal_payment_has_no_triggered_rules():
    engine = FraudRulesEngine()

    results = engine.evaluate(payment())

    assert all(not rule.triggered for rule in results)


def test_high_value_transaction():
    engine = FraudRulesEngine()

    results = engine.evaluate(payment(amount="150000"))

    high_value_rule = next(rule for rule in results if rule.rule_name == "HIGH_VALUE_TRANSACTION")

    assert high_value_rule.triggered is True
    assert high_value_rule.score == 40


def test_velocity_rule():
    engine = FraudRulesEngine()

    results = engine.evaluate(payment(transaction_count=15))

    velocity_rule = next(rule for rule in results if rule.rule_name == "CUSTOMER_VELOCITY")

    assert velocity_rule.triggered is True
    assert velocity_rule.score == 35


def test_suspicious_payment_method():
    engine = FraudRulesEngine()

    results = engine.evaluate(payment(payment_method="PREPAID_CARD"))

    payment_method_rule = next(
        rule for rule in results if rule.rule_name == "SUSPICIOUS_PAYMENT_METHOD"
    )

    assert payment_method_rule.triggered is True
    assert payment_method_rule.score == 30
