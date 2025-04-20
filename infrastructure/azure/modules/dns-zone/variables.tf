variable "resource_group_name" {
  description = "The name of the resource group where the DNS zone will be created."
  type        = string
}

variable "location" {
  description = "The Azure region where resources will be created."
  type        = string
}

variable "zone_name" {
  description = "The name of the DNS zone (e.g., example.com)."
  type        = string
}

variable "tags" {
  description = "A mapping of tags to assign to the DNS zone."
  type        = map(string)
  default     = {}
}

variable "record_sets" {
  description = "A map of record sets to create in the DNS zone."
  type = map(object({
    name      = string
    type      = string
    ttl       = number
    records   = list(string)
  }))
  default = {}
}
