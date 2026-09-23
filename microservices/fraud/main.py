from fastapi import FastAPI

from microservices.fraud.config import FraudConfig
from microservices.fraud.routes import create_router
from microservices.fraud.rules import FraudRulesEngine
from microservices.fraud.service import FraudDetectionService

config = FraudConfig()

rules_engine = FraudRulesEngine(config)

service = FraudDetectionService(
    rules_engine,
)


app = FastAPI(
    title="Fraud Detection Service",
    description="Real-time fraud scoring service",
    version="1.0.0",
)

app.include_router(create_router(service))


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": "fraud-service",
    }


@app.get("/ready", tags=["health"])
def readiness() -> dict[str, str]:
    return {
        "status": "ready",
        "service": "fraud-service",
    }
