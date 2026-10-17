# AKS Infrastructure

Terraform configuration for the Enterprise Real-Time Retail Data Platform.

## Resources

- Azure Resource Group
- Virtual Network and AKS subnet
- Azure Container Registry (Basic SKU)
- Azure Kubernetes Service
- System-assigned AKS managed identity
- ACR pull permission for the AKS kubelet identity
- Log Analytics workspace and AKS monitoring integration
- Azure RBAC, OIDC issuer and Workload Identity

## Prerequisites

- Terraform >= 1.6
- Azure CLI
- An Azure subscription with permissions to create the resources
- Appropriate permissions to create Azure role assignments

## Authenticate

```bash
az login
az account set --subscription "<YOUR_SUBSCRIPTION_ID>"
az account show --output table
