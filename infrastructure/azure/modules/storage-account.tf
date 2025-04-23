module "storage_account" {
  source                = "./modules/storage-account"
  resource_group_name   = azurerm_resource_group.rg.name
  location              = azurerm_resource_group.rg.location
  storage_account_name  = "devopslabkitstorage" # must be globally unique, 3-24 lowercase letters/numbers
  tags = {
    environment = "devops-lab-kit"
    purpose     = "blob-storage"
  }
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

#
# Create a blob container for pastebin
#

resource "azurerm_storage_container" "pastebin" {
  name                  = "pastebin"
  storage_account_id    = module.storage_account.storage_account_id
  container_access_type = "blob"
}

resource "azurerm_storage_management_policy" "pastebin_expiry" {
  storage_account_id = module.storage_account.storage_account_id

  rule {
    name    = "expire-pastebin-blobs-after-1-day"
    enabled = true

    filters {
      blob_types   = ["blockBlob"]
      prefix_match = ["pastebin/"]
    }

    actions {
      base_blob {
        delete_after_days_since_modification_greater_than = 1
      }
    }
  }
}

output "pastebin_container_url" {
  description = "The URL of the pastebin blob container."
  value       = "https://${module.storage_account.storage_account_name}.blob.core.windows.net/pastebin"
}
