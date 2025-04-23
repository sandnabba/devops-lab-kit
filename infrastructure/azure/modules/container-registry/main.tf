resource "azurerm_container_registry" "acr" {
  name                          = var.name
  resource_group_name           = var.resource_group_name
  location                      = var.location
  sku                           = var.sku
  admin_enabled                 = var.admin_enabled
  public_network_access_enabled = var.public_network_access_enabled
  zone_redundancy_enabled       = var.zone_redundancy_enabled && var.sku == "Premium"
  
  identity {
    type = "SystemAssigned"
  }

  # Network rules are only valid for Premium SKU
  dynamic "network_rule_set" {
    for_each = var.sku == "Premium" && length(var.network_rule_set) > 0 ? [var.network_rule_set] : []
    
    content {
      default_action = network_rule_set.value.default_action

      dynamic "ip_rule" {
        for_each = network_rule_set.value.ip_rules != null ? network_rule_set.value.ip_rules : []
        
        content {
          action   = "Allow"
          ip_range = ip_rule.value
        }
      }
    }
  }

  # Georeplication is only available for Premium SKU
  dynamic "georeplications" {
    for_each = var.sku == "Premium" && var.georeplication_locations != null ? var.georeplication_locations : []
    
    content {
      location                = georeplications.value
      zone_redundancy_enabled = var.zone_redundancy_enabled
      tags                    = var.tags
    }
  }

  tags = var.tags

  lifecycle {
    ignore_changes = [tags]
  }
}
