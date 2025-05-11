# Source local.env
-include ../local.env

# Create the devopslabkit network if it doesn't exist
docker-network:
	docker network inspect devopslabkit >/dev/null 2>&1 || docker network create devopslabkit

# Build the development Docker image
build-dev-container:
	docker build -t frontend-dev -f Dockerfile.dev .

# Build the production Docker image
build-prod:
	docker build -t devops-lab-kit-frontend:latest .

# Run the development container with live reload and code mounting
run-dev-container: docker-network
	docker run -it --rm \
		-p 5173:5173 \
		-v $$(pwd)/webapp:/app \
		-v /app/node_modules \
		--network devopslabkit \
		--name frontend-dev-container \
		frontend-dev

# Run the production container
run-prod: docker-network
	docker run -d --rm \
		-p 80:80 \
		--network devopslabkit \
		--name frontend-prod-container \
		devops-lab-kit-frontend:latest

# Remove the development container if it's running
stop-dev-container:
	-docker stop frontend-dev-container

# Remove the production container if it's running
stop-prod:
	-docker stop frontend-prod-container

.PHONY: build-dev-container build-prod run-dev-container run-prod stop-dev-container stop-prod docker-network
