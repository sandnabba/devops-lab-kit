# Azure Infrastructure
This directory contains Terraform configurations for provisioning Azure infrastructure.

## Directory Structure

- **`main.tf`**: Defines core Azure resources such as Resource Group, Virtual Network (VNet), and Subnet.
- **`variables.tf`**: Declares input variables for the root module.
- **`provider.tf`**: Configures the Azure provider.
- **`outputs.tf`**: Specifies output values from the root module.
- **`terraform.tfvars`**: Stores variable values (may include sensitive data).
- **`modules/{module}/`**: Each subdirectory under `modules/` is a reusable Terraform module for a specific resource or set of resources. For example:
   - **`main.tf`**: Defines module-specific resources.
   - **`variables.tf`**: Declares module-specific variables.
   - **`outputs.tf`**: Specifies module-specific outputs.
- **`modules/{module}.tf`**: A template file to use the module, e.g.:
  ```hcl
  module "{module}" {
    source = "./modules/{module}"
    # ...module input variables...
  }
  ```

To enable a module, create a symlink from the root/top level:
```bash
# From the azure directory:
ln -s modules/{module}.tf .
```

## Provider Setup

The Azure provider is configured in the root module and inherited by all child modules, following Terraform best practices.

## SSH Key Setup

A public SSH key is required for authenticating to the virtual machine. Add your public key to the `terraform.tfvars` file:

```hcl
admin_ssh_key_public = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ..."
```

## Usage

1. Change to the Azure infrastructure directory:
    ```bash
    cd infrastructure/azure
    ```
2. Initialize the Terraform working directory:
    ```bash
    terraform init
    ```
3. Review the execution plan:
    ```bash
    terraform plan
    ```
4. Apply the configuration to provision resources:
    ```bash
    terraform apply
    ```
5. Destroy resources when they are no longer needed:
    ```bash
    terraform destroy
    ```

## Additional Notes

### Variable Files

- Do not commit `terraform.tfvars` to version control if it contains sensitive information such as subscription IDs or SSH keys.
- Each module is a reusable Terraform module that provisions specific resources or sets of resources.

### Permissions and Service Principals

Service Principals (SPNs) are typically used for authenticating automated services to Azure resources. In this lab, SPN creation was not possible due to limited account privileges.
