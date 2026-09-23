from fastapi import APIRouter

from microservices.fraud.models import (
    FraudScoreResponse,
    PaymentRequest,
)
from microservices.fraud.service import FraudDetectionService


def create_router(
    service: FraudDetectionService,
) -> APIRouter:
    router = APIRouter(
        prefix="/api/v1/fraud",
        tags=["fraud"],
    )

    @router.post(
        "/score",
        response_model=FraudScoreResponse,
    )
    def score_payment(
        payment: PaymentRequest,
    ) -> FraudScoreResponse:
        return service.evaluate(payment)

    return router
