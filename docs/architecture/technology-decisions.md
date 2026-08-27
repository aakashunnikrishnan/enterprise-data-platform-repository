# Technology Decisions

## Microsoft Fabric

### Decision

Use Microsoft Fabric as the primary analytical data platform.

### Why

- Native OneLake integration
- Lakehouse architecture
- Spark-based processing
- Eventstream capabilities
- Semantic models
- Power BI integration
- Centralized analytics platform

---

## Azure Event Hubs

### Decision

Use Azure Event Hubs as the cloud event ingestion layer.

### Why

- Fully managed Azure service
- High-throughput event ingestion
- Kafka-compatible protocol
- Native Azure integration
- Partition-based scalability

---

## Kafka Compatibility

### Decision

Use Kafka APIs where appropriate rather than coupling application producers directly to proprietary APIs.

### Why

This demonstrates portability between:

- Apache Kafka
- Azure Event Hubs
- Other Kafka-compatible platforms

---

## Azure Kubernetes Service

### Decision

Use AKS for containerized microservices.

### Why

- Managed Kubernetes
- Horizontal scaling
- Self-healing workloads
- Container orchestration
- Azure integration
- Production-grade deployment model

---

## Delta Lake

### Decision

Use Delta Lake as the primary lakehouse storage format.

### Why

- ACID transactions
- Schema enforcement
- Schema evolution
- Time travel
- MERGE operations
- Change Data Feed
- Reliable incremental processing

---

## Terraform

### Decision

Use Terraform for infrastructure provisioning.

### Why

- Infrastructure as Code
- Reproducibility
- Version control
- Environment consistency
- Automated infrastructure deployment

---

## GitHub Actions

### Decision

Use GitHub Actions for CI/CD.

### Why

- Native GitHub integration
- Automated testing
- Docker image builds
- Terraform workflows
- AKS deployments
- Environment approvals

---

## Prometheus

### Decision

Use Prometheus for application and Kubernetes metrics.

### Why

- Cloud-native
- Kubernetes ecosystem integration
- Flexible metric model
- Alerting support
- Grafana integration

---

## Grafana

### Decision

Use Grafana for operational dashboards.

### Why

Provides a unified view of:

- Kubernetes health
- Application metrics
- Streaming throughput
- Consumer lag
- Pipeline performance

---

## Azure Monitor

### Decision

Use Azure Monitor and Log Analytics for Azure-native monitoring.

### Why

- Native Azure integration
- Centralized logs
- Platform metrics
- Alerts
- Integration with AKS and Azure services

---

## Design Principle

The architecture intentionally combines managed cloud services with open-source technologies.

Managed Azure Services
        +
Open Source Technologies
        +
Microsoft Fabric
        =
Cloud-Native Data Platform
