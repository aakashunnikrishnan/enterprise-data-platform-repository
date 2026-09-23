from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class FraudDecision(StrEnum):
    APPROVE = "APPROVE"
    REVIEW = "REVIEW"
    BLOCK = "BLOCK"


class RiskLevel(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class PaymentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payment_id: str = Field(min_length=1)
    order_id: str = Field(min_length=1)
    customer_id: str = Field(min_length=1)

    amount: Decimal = Field(gt=0)

    currency: str = Field(
        default="INR",
        min_length=3,
        max_length=3,
    )

    payment_method: str = Field(min_length=1)

    customer_transaction_count: int = Field(
        default=0,
        ge=0,
    )

    customer_transaction_amount: Decimal = Field(
        default=Decimal("0"),
        ge=0,
    )


class FraudRuleResult(BaseModel):
    rule_name: str
    score: int = Field(ge=0)
    triggered: bool
    reason: str


class FraudScoreResponse(BaseModel):
    payment_id: str
    customer_id: str

    fraud_score: int = Field(
        ge=0,
        le=100,
    )

    risk_level: RiskLevel
    decision: FraudDecision

    rules: list[FraudRuleResult]
