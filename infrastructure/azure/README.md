# Azure Infrastructure

This directory contains Terraform configurations for Azure infrastructure.

## Structure

- **`main.tf`**: Defines the main Azure resources including Resource Group, VNet, and Subnet
- **`variables.tf`**: Defines variables for the root module
- **`provider.tf`**: Configures the Azure provider
- **`outputs.tf`**: Defines output values from the root module
- **`terraform.tfvars`**: Contains values for variables (may contain sensitive information)
- **`virtual-machine/`**: Child module for Virtual Machine resources
  - **`main.tf`**: Defines VM-specific resources
  - **`variables.tf`**: Defines VM-specific variables
  - **`outputs.tf`**: Defines VM-specific outputs

## Provider Configuration

The Azure provider is configured at the root module level and inherited by child modules. This approach follows the Terraform best practice of configuring providers only in the root module.

## SSH Key Configuration

The virtual machine requires an SSH key for authentication. You must provide this key in your `terraform.tfvars` file:

```hcl
admin_ssh_key_public = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ..."
```

To generate a new SSH key pair:

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/devops_lab_key
```

Then copy the contents of `~/.ssh/devops_lab_key.pub` to the `admin_ssh_key_public` variable in `terraform.tfvars`.

## Usage

1. Navigate to the `/infrastructure/azure` directory:
   ```bash
   cd infrastructure/azure
   ```

2. Initialize Terraform:
   ```bash
   terraform init
   ```

3. Review the plan:
   ```bash
   terraform plan
   ```

4. Apply the configuration:
   ```bash
   terraform apply
   ```

5. To destroy resources when done:
   ```bash
   terraform destroy
   ```

## Notes

- The `terraform.tfvars` file should not be committed to version control if it contains sensitive information like subscription IDs or SSH keys.
- The virtual-machine module is a child module that creates a VM in the subnet defined in the parent module.
