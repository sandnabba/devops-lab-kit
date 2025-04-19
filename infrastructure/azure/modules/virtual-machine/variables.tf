variable "resource_group_name" {
  description = "The name of the resource group."
  type        = string
}

variable "location" {
  description = "The Azure region where resources will be created."
  type        = string
}

variable "subnet_id" {
  description = "The ID of the subnet to attach the VM's NIC to."
  type        = string
}

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

variable "admin_username" {
  description = "The admin username for the VM."
  type        = string
  default     = "azureuser"
}

variable "admin_ssh_key_public" {
  description = "The public SSH key used to authenticate the admin user."
  type        = string
  sensitive   = true
}

variable "public_ip_name" {
  description = "The name of the Public IP address resource."
  type        = string
  default     = "devops-lab-vm-pip"
}

variable "nsg_name" {
  description = "The name of the Network Security Group."
  type        = string
  default     = "devops-lab-vm-nsg"
}

variable "nic_name" {
  description = "The name of the Network Interface."
  type        = string
  default     = "devops-lab-vm-nic"
}
