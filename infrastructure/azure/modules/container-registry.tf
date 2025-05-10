module "container_registry" {
  # Comment out the source line below to disable this module
  source = "./modules/container-registry"

  # Required parameters
  name                = "${replace(lower(local.resource_group_name), "-", "")}acr"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  # Optional parameters with defaults
  sku                           = "Standard"
  admin_enabled                 = true
  public_network_access_enabled = true
  zone_redundancy_enabled       = false

  # Tagging
  tags = {
    environment = "devops-lab-kit"
    purpose     = "container-registry"
  }
}

# Expose Container Registry outputs at the parent level
output "acr_login_server" {
  description = "The login server URL of the Container Registry."
  value       = module.container_registry.login_server
}

output "acr_name" {
  description = "The name of the Container Registry."
  value       = module.container_registry.name
}
