# Fraud Detection Microservice

Real-time fraud scoring service for the Enterprise Real-Time Retail
Data Platform.

## Responsibilities

- Evaluate payment risk
- Calculate fraud score
- Classify risk level
- Generate fraud decision
- Expose health/readiness endpoints

## Fraud Rules

The current implementation contains three deterministic rules.

| Rule | Score |
|---|---:|
| High-value transaction | 40 |
| Customer velocity | 35 |
| Suspicious payment method | 30 |

Maximum score is capped at 100.

## Risk Classification

| Score | Risk | Decision |
|---:|---|---|
| 0-29 | LOW | APPROVE |
| 30-69 | MEDIUM | REVIEW |
| 70-100 | HIGH | BLOCK |

## API

### Score payment

```text
POST /api/v1/fraud/score
