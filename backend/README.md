# Backend API Service

The backend is part of a DevOps Lab Kit designed for hands-on learning and experimentation. It provides a simple RESTful API built with Python and Flask, supporting CRUD (Create, Read, Update, Delete) operations for inventory items stored in a database.

Beyond inventory management, the API includes endpoints for retrieving service environment details, performing health checks, and a basic hello endpoint. These features are useful for exploring deployment strategies, environment configuration, and service monitoring in various DevOps scenarios.

## Table of Contents

1.  [Features](#features)
2.  [Configuration](#configuration)
3.  [Database](#database)
4.  [API Endpoints](#api-endpoints)
5.  [Deployment options](#deployment-options)
    *   [Using Docker container (Recommended)](#using-docker-container-recommended)
        *   [Production Container](#production-container)
        *   [Development Container (with Live Reload)](#development-container-with-live-reload)
    *   [Python Virtual Environment](#python-virtual-environment)
    *   [Azure deployment](#azure-deployment)

## Features

* **Flask Framework**: Lightweight and flexible Python web framework.
  * **Flask-SQLAlchemy**: Provides ORM capabilities for database interaction. Uses SQLite (a simple file-based database stored in the `instance/` directory) by default. Transitioning to other databases like MySQL or PostgreSQL is straightforward with minimal code changes.
  * **Flask-CORS**: Handles Cross-Origin Resource Sharing for frontend integration.
*   **RESTful API**: Provides standard HTTP endpoints for managing inventory items.
*   **Docker Support**: Includes a multi-stage Dockerfile for development and production builds.

## Configuration

The application can be configured using environment variables. Below are the key configuration options:

| Environment Variable         | Default Value                          | Description                                                                 |
|------------------------------|----------------------------------------|-----------------------------------------------------------------------------|
| `SQLALCHEMY_DATABASE_URI`    | `sqlite:///instance/database.db`      | The database connection string. Defaults to a local SQLite database.       |
| `PORT`                       | `5000`                                | The port the application listens on. Azure App Services overrides this.    |


## Database

*   The application uses SQLite by default. The database file (`database.db`) is automatically created inside the `instance/` directory when the application first runs ([`src/app.py`](src/app.py), [`src/database.py`](src/database.py)). When running via Docker, this directory should ideally be mounted as a volume for persistence.
*   The database schema is defined in [`src/database.py`](src/database.py) using the `Inventory` model.
*   Database initialization and table creation happen automatically on startup ([`database.init_db`](src/database.py)).

## API Endpoints

| Method   | Endpoint             | Description                                         | Payload                                 |
| :------- | :------------------- | :--------------------------------------------------| :--------------------------------------- |
| `GET`    | `/database/`         | Retrieves all inventory items.                      | None                                    |
| `POST`   | `/database/`         | Adds a new inventory item.                          | JSON with `name`, `quantity`, `price`   |
| `PUT`    | `/database/<item_id>`| Updates an inventory item by ID.                    | JSON with fields to update              |
| `DELETE` | `/database/<item_id>`| Deletes an inventory item by ID.                    | None                                    |
| `GET`    | `/healthcheck`       | Checks app status and database connectivity.        | None                                    |
| `GET`    | `/environment`       | Retrieves all environment variables.                | None                                    |
| `GET`    | `/hello`             | Simple endpoint that responds with 'Hello, World!'. | None                                    |
| `POST`   | `/log`               | Triggers a log message at a specified level.        | JSON with `level`, `message`            |
| `POST`   | `/crash`             | Intentionally crashes the entire application.       | None                                    |
| `POST`   | `/pastebin`          | Uploads text to Azure Blob Storage and returns a URL (expires in 24h). | JSON with `text` |

### Example: Adding an Item using `curl`

To add a new item named "Example Widget" with quantity 50 and price 19.95, you can use the following `curl` command (assuming the server is running locally on port 5000):

```bash
curl -X POST \
  http://localhost:5000/database/ \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Example Widget",
    "quantity": 50,
    "price": 19.95
  }'
```

**Expected Response (201 Created):**

```json
{
  "id": 1, // The ID will be assigned by the database
  "name": "Example Widget",
  "price": 19.95,
  "quantity": 50
}
```

### Example: Logging a Message

To log a message at the `warning` level:

```bash
curl -X POST \
  http://localhost:5000/log \
  -H 'Content-Type: application/json' \
  -d '{
    "level": "warning",
    "message": "This is a test warning from the API"
  }'
```

**Expected Response (200 OK):**

```json
{
  "status": "logged",
  "level": "warning",
  "message": "This is a test warning from the API"
}
```

### Example: Crashing the Application

To intentionally crash the entire application (for testing purposes):

```bash
curl -X POST http://localhost:5000/crash
```

**Note:**  
This will terminate the whole Gunicorn process (all workers and master). Use with caution.

### Example: Uploading Text to Pastebin (Azure Blob Storage)

To upload a text snippet and get a temporary URL (valid for 24 hours):

```bash
curl -X POST \
  http://localhost:5000/pastebin \
  -H 'Content-Type: application/json' \
  -d '{
    "text": "This is a test paste for Azure Blob Storage."
  }'
```

**Expected Response (201 Created):**

```json
{
  "url": "https://<your-storage-account>.blob.core.windows.net/pastebin/pastebin-<uuid>.txt?<sas-token>",
  "expires_at": "2024-05-01T12:34:56.789012Z"
}
```

You can use the returned `url` to access the uploaded text until the expiry time.

## Deployment options 

### Using Docker container (Recommended)

You can build and run the backend service using Docker with the provided multi-stage `Dockerfile`.

### Production Container

1.  **Build the production Docker image**:
    ```bash
    # This builds the default (production) stage in the Dockerfile
    docker build -t inventory-backend .
    ```
2.  **Run the production Docker container**:
    ```bash
    # Make sure port 5000 is free or map to a different host port
    docker run -d --rm \
      -p 5000:5000 \
      --name backend-prod-container \
      inventory-backend
    ```
    This will start the container in detached mode (`-d`), running the application with Gunicorn workers optimized for production. The database file will be stored *inside* the container. For persistent storage, mount a volume to `/app/instance`: `-v backend-db-data:/app/instance`. Use `docker logs backend-prod-container` to view logs and `docker stop backend-prod-container` to stop it.

### Development Container (with Live Reload)

This is the **recommended method for local development**. It uses the `dev` stage from the `Dockerfile`, runs `gunicorn` with the `--reload` flag, and mounts your local source code for live updates.

1.  **Build the development Docker image**:
    ```bash
    # Explicitly target the 'dev' stage in the Dockerfile
    docker build --target dev -t inventory-backend-dev .
    ```
2.  **Run the development Docker container**:
    ```bash
    # Mount the local 'src' directory into the container's '/app' directory
    # Mount a volume for the 'instance' directory to persist the database
    # Load environment variables from Docker.env file
    docker run -it --rm \
      --env-file Docker.env \
      -p 5000:5000 \
      -v $(pwd)/src:/app \
      -v backend-dev-db-data:/app/instance \
      --name backend-dev-container \
      inventory-backend-dev
    ```
    *   `--env-file Docker.env`: Loads environment variables from a local `Docker.env` file (see below).
    *   `-it`: Runs the container interactively so you can see logs and stop with Ctrl+C.
    *   `--rm`: Automatically removes the container when it exits.
    *   `-v $(pwd)/src:/app`: Mounts your local `src` folder into `/app` in the container. Changes you make locally will trigger `gunicorn` to reload. **Important:** This mount overlays the code copied during the image build.
    *   `-v backend-dev-db-data:/app/instance`: Creates a named volume `backend-dev-db-data` to store the SQLite database (`instance/database.db`) persistently, separate from the container lifecycle.
    *   The API will be available at `http://localhost:5000`. Changes to Python files in your local `src` directory should cause the server inside the container to automatically restart.

#### Using a `Docker.env` file for local development

For local Docker development, you can store all required environment variables in a `Docker.env` file in the backend directory. This file is loaded automatically by Docker when you use the `--env-file Docker.env` flag.

Example `Docker.env` file:

```
# Docker.env
PORT=5000
SQLALCHEMY_DATABASE_URI=sqlite:///instance/database.db
AZURE_STORAGE_CONNECTION_STRING=your-azure-connection-string
AZURE_STORAGE_CONTAINER=pastebin
```

**Note:**  
Never commit your `Docker.env` file to version control if it contains secrets.

### Python Virtual Environment

If you prefer not to use Docker, you can set up a local Python environment. Instructions for this method can be found here:

*   **[Local Python Environment Setup](./docs/local-setup.md)**

### Azure deployment

The backend API can be deployed to Azure using either **App Services** or **Azure Container Instances**.

A `Makefile` is provided with targets for both deployment options, utilizing the `Azure CLI (az)` command.

**Note:** For production environments, it is recommended to manage the app or container infrastructure using Terraform or another infrastructure-as-code platform.

#### Azure App Services

- `zip`: Creates the application .zip file for deployment.
- `setup`: Initializes the Azure App Service resources.
- `deploy`: Deploys the zip file to the App Service.
- `logs`: Tails Azure App Service logs.
- `ssh`: Opens an SSH shell in the App Service container.

#### Azure Container Instances

- `acr-image`: Builds and pushes a Docker image to Azure Container Registry.
- `container-deploy`: Deploys the container image to Azure Container Instances.  
  *Note: You must provide `REGISTRY_USERNAME` and `REGISTRY_PASSWORD` as environment variables when running this target to avoid hardcoding secrets.*
- `container-show`: Lists running container instances.

Refer to the `Makefile` for usage details and required environment variables.
