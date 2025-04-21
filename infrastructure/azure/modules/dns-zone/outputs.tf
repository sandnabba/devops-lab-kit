output "dns_zone_id" {
  description = "The ID of the DNS zone."
  value       = azurerm_dns_zone.zone.id
}

output "dns_zone_name" {
  description = "The name of the DNS zone."
  value       = azurerm_dns_zone.zone.name
}

output "name_servers" {
  description = "The name servers for the DNS zone."
  value       = azurerm_dns_zone.zone.name_servers
}

output "zone_fqdn" {
  description = "The FQDN of the DNS zone."
  value       = "${azurerm_dns_zone.zone.name}."
}
