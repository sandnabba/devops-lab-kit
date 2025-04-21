variable "subscription_id" {
  description = "The Azure Subscription ID."
  type        = string
}

variable "resource_group_name" {
  description = "The name of the main resource group for the lab kit."
  type        = string
  default     = "devops-lab-kit-rg"
}

variable "location" {
  description = "The Azure region where the main resource group will be created."
  type        = string
  default     = "Sweden Central"
}

# --- Network Variables ---
variable "vnet_name" {
  description = "The name of the Virtual Network."
  type        = string
  default     = "devops-lab-vnet"
}

variable "vnet_address_space" {
  description = "The address space for the Virtual Network."
  type        = list(string)
  default     = ["10.0.0.0/16"]
}

variable "subnet_name" {
  description = "The name of the Subnet."
  type        = string
  default     = "default"
}

variable "subnet_address_prefix" {
  description = "The address prefix for the Subnet."
  type        = list(string)
  default     = ["10.0.1.0/24"]
}

# --- VM Variables ---
variable "vm_name" {
  description = "The name of the Virtual Machine."
  type        = string
  default     = "devops-lab-vm"
}

variable "vm_size" {
  description = "The size (SKU) of the Virtual Machine."
  type        = string
  default     = "Standard_B1s"
}

variable "admin_ssh_key_public" {
  description = "The public SSH key used to authenticate the admin user."
  type        = string
  sensitive   = true
  # No default - value must be provided
}

variable "dns_zone_name" {
  description = "The name of the DNS zone."
  type        = string
  default     = "example.com"
}