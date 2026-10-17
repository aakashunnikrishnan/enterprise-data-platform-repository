output "eventhub_namespace_name" {
  description = "Provisioned Event Hubs namespace."
  value       = azurerm_eventhub_namespace.main.name
}

output "eventhub_namespace_id" {
  description = "Resource ID of the Event Hubs namespace."
  value       = azurerm_eventhub_namespace.main.id
}

output "kafka_bootstrap_servers" {
  description = "Kafka-compatible bootstrap endpoint for Event Hubs."
  value       = "${azurerm_eventhub_namespace.main.name}.servicebus.windows.net:9093"
}

output "event_hub_names" {
  description = "Event hubs created by this configuration."
  value       = sort(tolist(local.event_hub_names))
}

output "consumer_groups" {
  description = "Consumer group names configured for each event hub."
  value       = sort(tolist(var.consumer_groups))
}
