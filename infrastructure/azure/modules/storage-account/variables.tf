variable "resource_group_name" {
  description = "The name of the resource group."
  type        = string
}

variable "location" {
  description = "The Azure region for the storage account."
  type        = string
}

variable "storage_account_name" {
  description = "Globally unique name for the storage account (3-24 lowercase letters/numbers)."
  type        = string
}

variable "tags" {
  description = "A mapping of tags to assign to the resources."
  type        = map(string)
  default     = {}
}
