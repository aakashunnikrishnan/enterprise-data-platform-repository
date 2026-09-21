from fastapi import FastAPI

from microservices.inventory.repository import InventoryRepository
from microservices.inventory.routes import create_router
from microservices.inventory.service import InventoryService

repository = InventoryRepository()
service = InventoryService(repository)


app = FastAPI(
    title="Inventory Service",
    description="Inventory management microservice for the retail platform",
    version="1.0.0",
)

app.include_router(create_router(service))


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": "inventory-service",
    }


@app.get("/ready", tags=["health"])
def readiness() -> dict[str, str]:
    return {
        "status": "ready",
        "service": "inventory-service",
    }
