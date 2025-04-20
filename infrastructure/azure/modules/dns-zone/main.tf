resource "azurerm_dns_zone" "zone" {
  name                = var.zone_name
  resource_group_name = var.resource_group_name
  tags                = var.tags
}

# Create A records
resource "azurerm_dns_a_record" "a_records" {
  for_each = { for k, v in var.record_sets : k => v if v.type == "A" }

  name                = each.value.name
  zone_name           = azurerm_dns_zone.zone.name
  resource_group_name = var.resource_group_name
  ttl                 = each.value.ttl
  records             = each.value.records
  tags                = var.tags
}

# Create CNAME records
resource "azurerm_dns_cname_record" "cname_records" {
  for_each = { for k, v in var.record_sets : k => v if v.type == "CNAME" }

  name                = each.value.name
  zone_name           = azurerm_dns_zone.zone.name
  resource_group_name = var.resource_group_name
  ttl                 = each.value.ttl
  record              = each.value.records[0]  # CNAME can only have one record
  tags                = var.tags
}

# Create MX records
resource "azurerm_dns_mx_record" "mx_records" {
  for_each = { for k, v in var.record_sets : k => v if v.type == "MX" }

  name                = each.value.name
  zone_name           = azurerm_dns_zone.zone.name
  resource_group_name = var.resource_group_name
  ttl                 = each.value.ttl
  
  # MX records require special formatting: "<preference> <exchange>"
  # The module expects records in format "10 mail.example.com"
  record {
    preference = split(" ", each.value.records[0])[0]
    exchange   = split(" ", each.value.records[0])[1]
  }
  
  tags = var.tags
}

# Create TXT records
resource "azurerm_dns_txt_record" "txt_records" {
  for_each = { for k, v in var.record_sets : k => v if v.type == "TXT" }

  name                = each.value.name
  zone_name           = azurerm_dns_zone.zone.name
  resource_group_name = var.resource_group_name
  ttl                 = each.value.ttl
  
  record {
    value = each.value.records[0]
  }
  
  tags = var.tags
}
