output "storage_account_name" {
  description = "The name of the storage account."
  value       = azurerm_storage_account.this.name
}

output "storage_account_connection_string" {
  # In a real-world scenario, a "Managed Identity" should be used to access the storage account.
  # This is just for demonstration purposes.
  description = "The connection string for the storage account."
  value       = azurerm_storage_account.this.primary_connection_string
  sensitive   = true
}

output "storage_account_id" {
  description = "The resource ID of the storage account."
  value       = azurerm_storage_account.this.id
}
