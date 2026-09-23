from microservices.fraud.models import (
    FraudDecision,
    FraudScoreResponse,
    PaymentRequest,
    RiskLevel,
)
from microservices.fraud.rules import FraudRulesEngine


class FraudDetectionService:
    def __init__(
        self,
        rules_engine: FraudRulesEngine,
    ) -> None:
        self.rules_engine = rules_engine

    def evaluate(
        self,
        payment: PaymentRequest,
    ) -> FraudScoreResponse:
        rules = self.rules_engine.evaluate(payment)

        fraud_score = min(
            sum(rule.score for rule in rules),
            100,
        )

        risk_level = self._risk_level(fraud_score)
        decision = self._decision(risk_level)

        return FraudScoreResponse(
            payment_id=payment.payment_id,
            customer_id=payment.customer_id,
            fraud_score=fraud_score,
            risk_level=risk_level,
            decision=decision,
            rules=rules,
        )

    @staticmethod
    def _risk_level(score: int) -> RiskLevel:
        if score >= 70:
            return RiskLevel.HIGH

        if score >= 30:
            return RiskLevel.MEDIUM

        return RiskLevel.LOW

    @staticmethod
    def _decision(
        risk_level: RiskLevel,
    ) -> FraudDecision:
        if risk_level == RiskLevel.HIGH:
            return FraudDecision.BLOCK

        if risk_level == RiskLevel.MEDIUM:
            return FraudDecision.REVIEW

        return FraudDecision.APPROVE
