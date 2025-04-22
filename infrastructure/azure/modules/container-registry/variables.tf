variable "name" {
  description = "Name of the Azure Container Registry. Must be globally unique."
  type        = string
  validation {
    condition     = can(regex("^[a-zA-Z0-9]+$", var.name)) && length(var.name) >= 5 && length(var.name) <= 50
    error_message = "ACR name must contain only alphanumeric characters, be between 5 and 50 characters."
  }
}

variable "resource_group_name" {
  description = "Name of the resource group where the ACR will be created."
  type        = string
}

variable "location" {
  description = "Azure region where the ACR will be deployed."
  type        = string
}

variable "sku" {
  description = "The SKU of the Azure Container Registry."
  type        = string
  default     = "Standard"
  validation {
    condition     = contains(["Basic", "Standard", "Premium"], var.sku)
    error_message = "The SKU must be one of: Basic, Standard, or Premium."
  }
}

variable "admin_enabled" {
  description = "Whether admin access is enabled for the ACR."
  type        = bool
  default     = false
}

variable "public_network_access_enabled" {
  description = "Whether public network access is enabled for the ACR."
  type        = bool
  default     = true
}

variable "zone_redundancy_enabled" {
  description = "Whether zone redundancy is enabled for the ACR. Only valid with Premium SKU."
  type        = bool
  default     = false
}

variable "network_rule_set" {
  description = "Network rule set for the ACR. Only applicable for Premium SKU."
  type = object({
    default_action = string       # "Allow" or "Deny"
    ip_rules       = list(string) # List of IP CIDR blocks
    subnet_ids     = list(string) # List of subnet IDs
  })
  default = {
    default_action = "Allow"
    ip_rules       = []
    subnet_ids     = []
  }
}

variable "georeplication_locations" {
  description = "List of Azure locations where the ACR should be geo-replicated. Only applicable for Premium SKU."
  type        = list(string)
  default     = null
}

variable "retention_policy" {
  description = "The retention policy for the ACR. Only applicable for Premium SKU."
  type = object({
    days    = number
    enabled = bool
  })
  default = null
}

variable "enable_content_trust" {
  description = "Whether to enable content trust for the ACR. Only applicable for Premium SKU."
  type        = bool
  default     = false
}

variable "tags" {
  description = "A mapping of tags to assign to the ACR."
  type        = map(string)
  default     = {}
}
