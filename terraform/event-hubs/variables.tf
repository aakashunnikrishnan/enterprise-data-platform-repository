variable "resource_group_name" {
  description = "Existing resource group created by the AKS Terraform configuration."
  type        = string
  default     = "rg-retail-platform-dev"
}

variable "location" {
  description = "Azure region for the Event Hubs namespace."
  type        = string
  default     = "centralindia"
}

variable "namespace_name" {
  description = "Globally unique Azure Event Hubs namespace name."
  type        = string

  validation {
    condition = (
      length(var.namespace_name) >= 6 &&
      length(var.namespace_name) <= 50 &&
      can(regex("^[a-z][a-z0-9-]*[a-z0-9]$", var.namespace_name))
    )
    error_message = "namespace_name must be 6-50 characters, start with a letter, end with a letter or number, and contain only lowercase letters, numbers, or hyphens."
  }
}

variable "sku" {
  description = "Event Hubs namespace pricing tier."
  type        = string
  default     = "Standard"

  validation {
    condition     = contains(["Basic", "Standard"], var.sku)
    error_message = "This configuration supports Basic or Standard SKU."
  }
}

variable "capacity" {
  description = "Initial throughput units for the namespace."
  type        = number
  default     = 1

  validation {
    condition     = var.capacity >= 1 && var.capacity <= 20
    error_message = "capacity must be between 1 and 20."
  }
}

variable "auto_inflate_enabled" {
  description = "Whether Standard SKU can automatically increase throughput units."
  type        = bool
  default     = true
}

variable "maximum_throughput_units" {
  description = "Maximum throughput units when auto-inflate is enabled."
  type        = number
  default     = 4
}

variable "partition_count" {
  description = "Partition count for each event hub."
  type        = number
  default     = 2

  validation {
    condition     = var.partition_count >= 1 && var.partition_count <= 32
    error_message = "partition_count must be between 1 and 32."
  }
}

variable "message_retention_days" {
  description = "Number of days event data is retained in each hub."
  type        = number
  default     = 1

  validation {
    condition     = var.message_retention_days >= 1 && var.message_retention_days <= 7
    error_message = "For this Standard SKU configuration, message_retention_days must be between 1 and 7."
  }
}

variable "consumer_groups" {
  description = "Consumer groups created for each event hub."
  type        = set(string)
  default     = ["aks-consumers", "fabric-ingestion"]
}

variable "tags" {
  description = "Common resource tags."
  type        = map(string)
  default = {
    project     = "retail-platform"
    environment = "dev"
    managed_by  = "terraform"
  }
}
