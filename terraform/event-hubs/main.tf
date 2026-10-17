variable "sku" {
  description = "Event Hubs namespace pricing tier."
  type        = string
  default     = "Standard"

  validation {
    condition     = var.sku == "Standard"
    error_message = "This configuration requires the Standard SKU."
  }
}
