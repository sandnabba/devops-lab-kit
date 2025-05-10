# Source local.env
-include ../local.env

ZIP_FILE = app.zip
SOURCE_DIR = deployment
# Use environment variables if they exist, otherwise use defaults
IDENTIFIER ?= devops-lab-kit
RESOURCE_GROUP_NAME ?= $(IDENTIFIER)-devops-lab-kit-rg
ACR_REGISTRY_NAME ?= $(CONTAINER_REGISTRY_NAME)
LOCATION ?= northeurope
APP_NAME ?= $(IDENTIFIER)-backend
APP_SERVICE_PLAN ?= $(IDENTIFIER)-plan
CONTAINER_APP_ENV ?= $(IDENTIFIER)-env

clean:
	@echo "Cleaning up..."
	rm -rf $(SOURCE_DIR) $(ZIP_FILE)
	@echo "Cleaned up."

#
# Container targets
#

# Create the devopslabkit network if it doesn't exist
docker-network:
	docker network inspect devopslabkit >/dev/null 2>&1 || docker network create devopslabkit

build-dev-container:
	docker build --target dev -t inventory-backend-dev .

run-dev-container: docker-network
	docker run -it --rm \
		--env-file Docker.env \
		--network devopslabkit \
		-p 5000:5000 \
		-v $(PWD)/src:/app \
		-v backend-dev-db-data:/app/instance \
		--name backend-dev-container \
		inventory-backend-dev


###
### Azure App Service Deployment
###

# Target to create the zip file
zip:
	mkdir -p deployment
	@echo "Preparing $(ZIP_FILE)..."
	cp requirements.txt $(SOURCE_DIR)/
	cp src/*.py $(SOURCE_DIR)/
	cd $(SOURCE_DIR) && zip -r ../$(ZIP_FILE) . -x "*.git*" "*.DS_Store"
	@echo "$(ZIP_FILE) created successfully."

# Target to set up the Azure resources (run only once)
setup:
	az appservice plan create --name $(APP_SERVICE_PLAN) --resource-group $(RESOURCE_GROUP_NAME) --sku B1 --is-linux
	az webapp create --resource-group $(RESOURCE_GROUP_NAME) --plan $(APP_SERVICE_PLAN) --name $(APP_NAME) --runtime "PYTHON:3.10"
	az webapp config appsettings set --resource-group $(RESOURCE_GROUP_NAME) --name $(APP_NAME) --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true

# Target to deploy the app (run this for updates)
deploy:
	az webapp deploy --resource-group $(RESOURCE_GROUP_NAME) --name $(APP_NAME) --src-path $(ZIP_FILE)

# Target to view logs
logs:
	az webapp log tail --resource-group $(RESOURCE_GROUP_NAME) --name $(APP_NAME)

ssh:
	az webapp ssh --resource-group $(RESOURCE_GROUP_NAME) --name $(APP_NAME)

###
### Azure Container targets
###

build-acr-image:
	az acr build --image devops-labkit/backend:latest --registry $(ACR_REGISTRY_NAME) .

create-container-instance:
	az container create --resource-group $(RESOURCE_GROUP_NAME) \
	--name $(IDENTIFIER)-backend-container \
	--image $(ACR_REGISTRY_NAME).azurecr.io/devops-labkit/backend:latest \
	--ports 5000 --os-type Linux --cpu 1 --memory 1 \
	--dns-name-label $(IDENTIFIER)-backend-aci-demo --location $(LOCATION) \
	--assign-identity \
	--registry-login-server $(ACR_REGISTRY_NAME).azurecr.io \
	--registry-username $(REGISTRY_USERNAME) \
	--registry-password $(REGISTRY_PASSWORD)

container-instance-show:
	az container list --resource-group $(RESOURCE_GROUP_NAME) --output table

container-app-environment:
	az containerapp env create \
		--name $(CONTAINER_APP_ENV) \
		--resource-group $(RESOURCE_GROUP_NAME) \
		--location $(LOCATION)

container-app-create:
	az containerapp create --name $(IDENTIFIER)-backend-app \
		--resource-group $(RESOURCE_GROUP_NAME) \
		--environment $(CONTAINER_APP_ENV) \
		--image $(ACR_REGISTRY_NAME).azurecr.io/devops-labkit/backend:latest \
		--target-port 5000 \
		--ingress external \
		--registry-server $(ACR_REGISTRY_NAME).azurecr.io \
		--registry-username $(REGISTRY_USERNAME) \
		--registry-password $(REGISTRY_PASSWORD) \
		--cpu 1.0 --memory 2.0Gi \
		--min-replicas 1 --max-replicas 1 \
