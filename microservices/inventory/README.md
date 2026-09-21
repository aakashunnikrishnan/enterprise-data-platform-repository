# Inventory Microservice

FastAPI-based inventory management service for the Enterprise Real-Time
Retail Data Platform.

## Responsibilities

- Query inventory
- Update inventory
- Reserve inventory
- Release inventory
- Expose health and readiness endpoints

## Architecture

```text
Client
  |
  v
FastAPI
  |
  v
Inventory Service
  |
  v
Inventory Repository
  |
  v
Storage
