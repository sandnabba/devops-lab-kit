# Azure Developer Associate

How this repo can be used while studying the "Develop Solutions for Microsoft Azure" (AZ-204T00-A) course, useful for taking the "Azure Developer Associate" (AZ-204) certification.

## App services

Both the backend and the frontend can be deployed as "App services" in Azure.
However, they are not linked together in this lab.

In the `backend/Makefile`, there are some targets for Azure App Service deployment:

- `zip`: Prepares a zip file for deployment.
- `setup`: Creates the Azure App Service plan and web app.
- `deploy`: Deploys the zip file to Azure App Service.
- `logs`: Tails logs from the App Service.
- `ssh`: Opens an SSH shell in the App Service container.

* Use the `/environment` endpoint to verify environment variables.

## Container services

Use the backend API.

Relevant Makefile targets for Azure Container Instances and Container Apps:

- `build-acr-image`: Builds and pushes the Docker image to Azure Container Registry.
- `create-container-instance`: Deploys the container image to Azure Container Instances.
- `container-instance-show`: Lists running container instances.
- `container-app-environment`: Creates a Container Apps environment.
- `container-app-create`: Deploys the backend as a Container App.

## Blob storage

For experimenting with blob storage:
1. Apply the `storage-account` Terraform module, that will create a public `pastebin` container + a life cycle policy.
2. Use the `/pastebin` API endpoint in the backend API.