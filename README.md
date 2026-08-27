# Enterprise Real-Time Data Platform

A cloud-native real-time data platform built using Microsoft Fabric, Azure, Delta Lake, Kafka/Event Hubs, Azure Kubernetes Service (AKS), Terraform, and GitHub Actions.

## Objectives

This project demonstrates the design and implementation of a scalable enterprise data platform capable of:

- Real-time event ingestion
- Event-driven microservices
- Cloud-native Kubernetes workloads
- Delta Lake Medallion Architecture
- Change Data Feed (CDF)
- Incremental data processing
- Data quality and governance
- Infrastructure as Code
- CI/CD automation
- End-to-end observability
- Real-time analytics and BI

## Architecture

The platform will progressively evolve from a local event-driven system into an Azure and Microsoft Fabric based production-style data platform.

```text
Event Producers
      |
      v
Kafka / Azure Event Hubs
      |
      v
AKS Microservices
      |
      v
Microsoft Fabric
      |
      +--> Bronze
      |
      +--> Silver
      |
      +--> Gold
      |
      v
Semantic Model
      |
      v
Power BI
