ZIP_FILE = app.zip
SOURCE_DIR = deployment
ACR_REGISTRY_NAME = devopslabkitrgacr
LOCATION ?= northeurope

clean:
	@echo "Cleaning up..."
	rm -rf $(SOURCE_DIR) $(ZIP_FILE)
	@echo "Cleaned up."

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
	az appservice plan create --name devops-lab-kit-plan --resource-group devops-lab-kit-rg --sku B1 --is-linux
	az webapp create --resource-group devops-lab-kit-rg --plan devops-lab-kit-plan --name devops-lab-kit-backend --runtime "PYTHON:3.10"
	az webapp config appsettings set --resource-group devops-lab-kit-rg --name devops-lab-kit-backend --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true

# Target to deploy the app (run this for updates)
deploy:
	az webapp deploy --resource-group devops-lab-kit-rg --name devops-lab-kit-backend --src-path $(ZIP_FILE)

# Target to view logs
logs:
	az webapp log tail --resource-group devops-lab-kit-rg --name devops-lab-kit-backend

ssh:
	az webapp ssh --resource-group devops-lab-kit-rg --name devops-lab-kit-backend

###
### Azure Container targets
###

build-acr-image:
	az acr build --image devops-labkit/backend:latest --registry $(ACR_REGISTRY_NAME) .

create-container-instance:
	az container create --resource-group devops-lab-kit-rg \
	--name devops-labkit-backend-container \
	--image $(ACR_REGISTRY_NAME).azurecr.io/devops-labkit/backend:latest \
	--ports 5000 --os-type Linux --cpu 1 --memory 1 \
	--dns-name-label devopslabkit-backend-aci-demo --location $(LOCATION) \
	--assign-identity \
	--registry-login-server devopslabkitrgacr.azurecr.io \
	--registry-username $(REGISTRY_USERNAME) \
	--registry-password $(REGISTRY_PASSWORD)

container-instance-show:
	az container list --resource-group devops-lab-kit-rg --output table

container-app-environment:
	az containerapp env create \
		--name devops-labkit-env \
		--resource-group devops-lab-kit-rg \
		--location $(LOCATION)

container-app-create:
	az containerapp create --name devops-labkit-backend-app \
		--resource-group devops-lab-kit-rg \
		--environment devops-labkit-env \
		--image $(ACR_REGISTRY_NAME).azurecr.io/devops-labkit/backend:latest \
		--target-port 5000 \
		--ingress external \
		--registry-server $(ACR_REGISTRY_NAME).azurecr.io \
		--registry-username $(REGISTRY_USERNAME) \
		--registry-password $(REGISTRY_PASSWORD) \
		--cpu 1.0 --memory 2.0Gi \
		--min-replicas 1 --max-replicas 1 \
