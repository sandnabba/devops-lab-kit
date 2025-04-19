# Virtual Machine Module

This module deploys an Ubuntu virtual machine in Azure along with its required networking components.

## Usage

```hcl
module "virtual_machine" {
  source = "./virtual-machine"

  subscription_id      = var.subscription_id
  resource_group_name  = azurerm_resource_group.rg.name
  location             = azurerm_resource_group.rg.location
  subnet_id            = azurerm_subnet.subnet.id
  admin_ssh_key_public = var.admin_ssh_key_public
  
  # Optional parameters with defaults
  vm_name              = "devops-lab-vm" # Optional: Override default VM name
  vm_size              = "Standard_B1s"  # Optional: Override default VM size
  admin_username       = "azureuser"     # Optional: Override default admin username
}
```

## Required Input Variables

| Name | Description |
|------|-------------|
| `resource_group_name` | The name of the resource group where the VM will be created. |
| `location` | The Azure region where the VM will be created. |
| `subnet_id` | The ID of the subnet where the VM's network interface will be attached. |
| `admin_ssh_key_public` | The public SSH key for authenticating to the VM. |

## Optional Input Variables

| Name | Description | Default |
|------|-------------|---------|
| `vm_name` | The name of the virtual machine. | `"devops-lab-vm"` |
| `vm_size` | The size/SKU of the virtual machine. | `"Standard_B1s"` |
| `admin_username` | The admin username for the VM. | `"azureuser"` |
| `public_ip_name` | Name for the public IP resource. | `"devops-lab-vm-pip"` |
| `nsg_name` | Name for the network security group. | `"devops-lab-vm-nsg"` |
| `nic_name` | Name for the network interface. | `"devops-lab-vm-nic"` |

## Outputs

| Name | Description |
|------|-------------|
| `vm_public_ip` | The public IP address of the virtual machine. |
| `ssh_command` | Ready-to-use SSH command to connect to the VM. |
| `vm_id` | The Azure Resource ID of the virtual machine. |

## Resources Created

- Public IP address
- Network Security Group with SSH, HTTP, and API access
- Network Interface
- Network Interface <-> NSG Association
- Linux Virtual Machine (Ubuntu)
