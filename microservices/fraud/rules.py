from decimal import Decimal

from microservices.fraud.config import FraudConfig
from microservices.fraud.models import (
    FraudRuleResult,
    PaymentRequest,
)


class FraudRulesEngine:
    def __init__(self, config: FraudConfig | None = None):
        self.config = config or FraudConfig()

    def evaluate(
        self,
        payment: PaymentRequest,
    ) -> list[FraudRuleResult]:
        return [
            self._high_value_rule(payment),
            self._velocity_rule(payment),
            self._payment_method_rule(payment),
        ]

    def _high_value_rule(
        self,
        payment: PaymentRequest,
    ) -> FraudRuleResult:
        triggered = payment.amount >= Decimal(str(self.config.high_value_threshold))

        return FraudRuleResult(
            rule_name="HIGH_VALUE_TRANSACTION",
            score=40 if triggered else 0,
            triggered=triggered,
            reason=(
                "Transaction exceeds high-value threshold"
                if triggered
                else "Transaction is below high-value threshold"
            ),
        )

    def _velocity_rule(
        self,
        payment: PaymentRequest,
    ) -> FraudRuleResult:
        triggered = (
            payment.customer_transaction_count >= self.config.velocity_threshold
            or payment.customer_transaction_amount
            >= Decimal(str(self.config.velocity_amount_threshold))
        )

        return FraudRuleResult(
            rule_name="CUSTOMER_VELOCITY",
            score=35 if triggered else 0,
            triggered=triggered,
            reason=(
                "Customer transaction velocity exceeds threshold"
                if triggered
                else "Customer transaction velocity is normal"
            ),
        )

    def _payment_method_rule(
        self,
        payment: PaymentRequest,
    ) -> FraudRuleResult:
        triggered = payment.payment_method.upper() in self.config.suspicious_payment_methods

        return FraudRuleResult(
            rule_name="SUSPICIOUS_PAYMENT_METHOD",
            score=30 if triggered else 0,
            triggered=triggered,
            reason=(
                "Payment method requires additional verification"
                if triggered
                else "Payment method is not flagged"
            ),
        )
