output "vm_public_ip" {
  description = "The public IP address of the virtual machine."
  value       = azurerm_public_ip.pip.ip_address
}

output "ssh_command" {
  description = "Command to SSH into the VM."
  value       = "ssh ${var.admin_username}@${azurerm_public_ip.pip.ip_address}"
}

output "vm_id" {
  description = "The Azure Resource ID of the virtual machine."
  value       = azurerm_linux_virtual_machine.vm.id
}
