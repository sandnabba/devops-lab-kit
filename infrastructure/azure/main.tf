# Shared resources for all Azure infrastructure
# * Resource Group
# * Virtual Network
# * Subnet

# --- Resource Group ---
resource "azurerm_resource_group" "rg" {
  name     = local.resource_group_name
  location = var.location
}

# --- Network Resources (Top Level) ---
resource "azurerm_virtual_network" "vnet" {
  name                = local.vnet_name
  address_space       = var.vnet_address_space
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  lifecycle {
    ignore_changes = [tags]
  }
}

resource "azurerm_subnet" "subnet" {
  name                 = var.subnet_name
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = var.subnet_address_prefix

  lifecycle {
    ignore_changes = [delegation]
  }
}

