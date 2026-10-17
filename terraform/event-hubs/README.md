# Azure Event Hubs Infrastructure

Terraform configuration for the retail platform's managed event streaming layer.

## Resources

- Standard Event Hubs namespace
- Orders, payments, inventory and customer activity event hubs
- AKS and Fabric consumer groups for each event hub
- Configurable partition count and message retention
- Optional namespace auto-inflate

## Prerequisites

- Terraform >= 1.6
- Azure CLI
- AzureRM provider 4.x
- Resource group created by the AKS infrastructure configuration
- Permissions to create Event Hubs resources

## Authenticate

```bash
az login
az account set --subscription "<YOUR_SUBSCRIPTION_ID>"
az account show --output table
