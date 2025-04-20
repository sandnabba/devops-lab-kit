# Define variables
ZIP_FILE = app.zip
SOURCE_DIR = deployment

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