# Terraform Modules

This is a placeholder for code or modules not currently used in any lab.

For each module, also create a `.tf` file that uses the module:

```
modules/
├── my_module/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
└── my_module.tf
```

In this way, it becomes very simple to enable the module by just adding a symlink from the root/top level:
```bash
# From the `azure` directory:
ln -s modules/my_module.tf .
```