module "dns_zone" {
  # Comment out the source line below to disable this module
  source = "./modules/dns-zone"

  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  zone_name           = var.dns_zone_name
}

# Expose DNS module outputs at the parent level
output "dns_zone_name" {
  description = "The name of the DNS zone."
  value       = module.dns_zone.dns_zone_name
}

output "dns_name_servers" {
  description = "The name servers for the DNS zone."
  value       = module.dns_zone.name_servers
}
