module "storage_account" {
  source                = "./modules/storage-account"
  resource_group_name   = azurerm_resource_group.rg.name
  location              = azurerm_resource_group.rg.location
  storage_account_name  = "${var.identifier}labkitstorage" # must be globally unique, 3-24 lowercase letters/numbers
}

output "storage_account_name" {
  description = "The name of the storage account."
  value       = module.storage_account.storage_account_name
}

output "storage_account_connection_string" {
  # In a real-world scenario, a "Managed Identity" should be used to access the storage account.
  # This is just for demonstration purposes.
  description = "The connection string for the storage account."
  value       = module.storage_account.storage_account_connection_string
  sensitive   = true
}
