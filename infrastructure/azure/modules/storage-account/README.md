# Azure Storage Account Module

This Terraform module creates an Azure Storage Account suitable for use by the backend API (e.g., for blob storage).

## Features

- Creates a Storage Account with secure defaults
- Creates a Blob Container (default: `pastebin`)
- Outputs connection string and container name

## Usage

```hcl
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

resource "azurerm_storage_container" "pastebin" {
  name                  = "pastebin"
  storage_account_id    = module.storage_account.storage_account_name
  container_access_type = "private"
}
```

## Inputs

| Name                  | Description                                      | Type   | Default     | Required |
|-----------------------|--------------------------------------------------|--------|-------------|----------|
| resource_group_name   | Name of the resource group                       | string | n/a         | yes      |
| location              | Azure region                                     | string | n/a         | yes      |
| storage_account_name  | Globally unique storage account name (3-24 chars)| string | n/a         | yes      |
| container_name        | Name of the blob container                       | string | "pastebin"  | no       |
| tags                  | Tags to apply                                    | map    | {}          | no       |

## Outputs

| Name                        | Description                                 |
|-----------------------------|---------------------------------------------|
| storage_account_name        | The name of the storage account             |
| storage_account_primary_key | The primary access key                      |
| storage_account_connection_string | The connection string for the account  |
| container_name              | The name of the blob container              |
| container_url               | The URL of the blob container               |
