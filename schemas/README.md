# Event Schemas

This directory contains the canonical event contracts used by the retail
real-time data platform.

## Supported Events

| Event | Kafka Topic | Purpose |
|---|---|---|
| ORDER_CREATED | orders | Customer order creation |
| PAYMENT_COMPLETED | payments | Successful payment |
| INVENTORY_UPDATED | inventory | Inventory changes |
| CUSTOMER_ACTIVITY | customer_activity | Customer behavior |

## Validation

Events are validated using Pydantic before being published to Kafka.

```text
Producer
   |
   v
Pydantic Validation
   |
   +---- Invalid ----> Reject / DLQ
   |
   v
JSON Serialization
   |
   v
Kafka / Event Hubs
