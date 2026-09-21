from fastapi import FastAPI

from microservices.pricing.repository import PricingRepository
from microservices.pricing.routes import create_router
from microservices.pricing.service import PricingService

repository = PricingRepository()
service = PricingService(repository)


app = FastAPI(
    title="Pricing Service",
    description="Pricing management microservice for the retail platform",
    version="1.0.0",
)

app.include_router(create_router(service))


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": "pricing-service",
    }


@app.get("/ready", tags=["health"])
def readiness() -> dict[str, str]:
    return {
        "status": "ready",
        "service": "pricing-service",
    }
