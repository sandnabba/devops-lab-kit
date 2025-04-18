# --- Virtual Machine Module ---
module "virtual_machine" {
  source = "./modules/virtual-machine"

  resource_group_name  = azurerm_resource_group.rg.name
  location             = azurerm_resource_group.rg.location
  subnet_id            = azurerm_subnet.subnet.id
  admin_ssh_key_public = var.admin_ssh_key_public
  vm_name              = var.vm_name
  vm_size              = var.vm_size
}

# Expose Virtual Machine module outputs at the parent level
output "vm_public_ip" {
  description = "The public IP address of the virtual machine."
  value       = module.virtual_machine.vm_public_ip
}

output "ssh_command" {
  description = "Command to SSH into the VM."
  value       = module.virtual_machine.ssh_command
}

output "vm_id" {
  description = "The Azure Resource ID of the virtual machine."
  value       = module.virtual_machine.vm_id
}
