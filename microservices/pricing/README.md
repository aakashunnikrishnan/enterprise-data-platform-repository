# Pricing Microservice

FastAPI-based pricing service for the Enterprise Real-Time Retail Data Platform.

## Responsibilities

- Product price lookup
- Product price updates
- Discount calculation
- Price deactivation
- Health checks
- Readiness checks

## Architecture

```text
Client
  |
  v
FastAPI
  |
  v
Pricing Service
  |
  v
Pricing Repository
  |
  v
Storage
