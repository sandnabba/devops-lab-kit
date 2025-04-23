# Create the devopslabkit network if it doesn't exist
docker-network:
	docker network inspect devopslabkit >/dev/null 2>&1 || docker network create devopslabkit

# Build the development Docker image
build-dev-container:
	docker build -t frontend-dev -f Dockerfile.dev .

# Run the development container with live reload and code mounting
run-dev-container: docker-network
	docker run -it --rm \
		-p 5173:5173 \
		-v $$(pwd)/webapp:/app \
		-v /app/node_modules \
		--network devopslabkit \
		--name frontend-dev-container \
		frontend-dev

# Remove the development container if it's running
stop-dev-container:
	-docker stop frontend-dev-container

.PHONY: build-dev-container run-dev-container stop-dev-container network
