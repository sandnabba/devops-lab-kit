# Azure DNS Zone Module

This Terraform module creates an Azure DNS Zone along with common record types (A, CNAME, MX, TXT) as needed.

## Features

- Creates an Azure DNS Zone for domain management
- Supports creating multiple record types:
  - A records (IPv4 addresses)
  - CNAME records (canonical names/aliases)
  - MX records (mail exchange)
  - TXT records (text validation)
- Customizable SOA record settings
- Proper tagging support

## Usage

### Basic Example

```hcl
module "dns_zone" {
  source              = "./modules/dns-zone"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  zone_name           = "example.com"
}
```

### Complete Example with Records

```hcl
module "dns_zone" {
  source              = "./modules/dns-zone"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  zone_name           = "example.com"
  
  # Create various DNS records
  record_sets = {
    # A record for web server
    www = {
      name    = "www"
      type    = "A"
      ttl     = 300
      records = ["10.0.1.4"]
    },
    
    # CNAME record for app subdomain pointing to www
    app = {
      name    = "app"
      type    = "CNAME"
      ttl     = 300
      records = ["www.example.com"]
    },
    
    # MX record for mail server (format: "preference exchange")
    mail = {
      name    = "@"
      type    = "MX"
      ttl     = 3600
      records = ["10 mail.example.com"]
    },
    
    # TXT record for domain verification
    verification = {
      name    = "@"
      type    = "TXT"
      ttl     = 3600
      records = ["v=spf1 include:spf.example.com -all"]
    }
  }
  
  # Optional: Custom SOA record
  soa_record = {
    email     = "admin.example.com"  # Usually written as admin@example.com but @ is replaced with .
    host_name = "ns1.example.com"
    ttl       = 3600
  }
  
  tags = {
    environment = "production"
    project     = "devops-lab-kit"
    owner       = "infrastructure-team"
  }
}
```

## Input Variables

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| `resource_group_name` | The name of the resource group where the DNS zone will be created | `string` | - | yes |
| `location` | The Azure region where resources will be created | `string` | - | yes |
| `zone_name` | The name of the DNS zone (e.g., example.com) | `string` | - | yes |
| `tags` | A mapping of tags to assign to the DNS zone | `map(string)` | `{}` | no |
| `record_sets` | A map of record sets to create in the DNS zone | `map(object)` | `{}` | no |
| `soa_record` | The SOA record configuration for the DNS zone | `object` | `null` | no |

### Record Sets Format

The `record_sets` variable accepts a map of objects with the following structure:

```hcl
record_sets = {
  key_name = {
    name    = "subdomain"  # or "@" for root domain
    type    = "A"          # One of: "A", "CNAME", "MX", "TXT"
    ttl     = 300          # Time to live in seconds
    records = ["value"]    # Values depend on record type
  }
}
```

## Output Values

| Name | Description |
|------|-------------|
| `dns_zone_id` | The ID of the DNS zone |
| `dns_zone_name` | The name of the DNS zone |
| `name_servers` | The name servers for the DNS zone |
| `zone_fqdn` | The FQDN of the DNS zone |

## Record Type Formats

### A Records
IP addresses for the host:
```
records = ["192.0.2.1", "192.0.2.2"]
```

### CNAME Records
A single canonical name (only first value used):
```
records = ["destination.example.com"]
```

### MX Records
Format: "preference exchange" (only first value used):
```
records = ["10 mail.example.com"]
```

### TXT Records
Text values (only first value used):
```
records = ["v=spf1 include:spf.example.com -all"]
```

## Enabling the Module

To use this module, link it from the parent module's directory:

```bash
# From the /infrastructure/azure directory:
ln -s modules/dns-zone.tf .
```

Or directly reference it in your root module.
