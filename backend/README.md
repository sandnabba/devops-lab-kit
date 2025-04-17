# Backend API Service

This directory contains the backend API service for the Inventory Management System.

## Table of Contents

1.  [Overview](#overview)
2.  [Features](#features)
3.  [Running Locally (Docker Recommended)](#running-locally-docker-recommended)
4.  [Database](#database)
5.  [API Endpoints](#api-endpoints)
6.  [Docker](#docker)
    *   [Production Container](#production-container)
    *   [Development Container (with Live Reload)](#development-container-with-live-reload)
7.  [Local Development (Alternative)](#local-development-alternative)

## Overview

The backend is a simple RESTful API built with Python using the Flask framework. It handles CRUD (Create, Read, Update, Delete) operations for inventory items and stores data in a database.

## Features

*   **Flask Framework**: Lightweight and flexible Python web framework.
*   **Flask-SQLAlchemy**: Provides ORM capabilities for database interaction.
*   **SQLite Database**: Simple file-based database, stored in the `instance/` directory.
*   **Flask-CORS**: Handles Cross-Origin Resource Sharing for frontend integration.
*   **RESTful API**: Provides standard HTTP endpoints for managing inventory items.
*   **Docker Support**: Includes a multi-stage Dockerfile for development and production builds.

## Running Locally (Docker Recommended)

The recommended way to run the backend locally for development is using the [Docker Development Container](#development-container-with-live-reload). This provides a consistent environment and includes live reloading.

See the [Docker](#docker) section below for instructions on building and running the development container.

## Database

*   The application uses SQLite by default. The database file (`database.db`) is automatically created inside the `instance/` directory when the application first runs ([`src/app.py`](src/app.py), [`src/database.py`](src/database.py)). When running via Docker, this directory should ideally be mounted as a volume for persistence.
*   The database schema is defined in [`src/database.py`](src/database.py) using the `Inventory` model.
*   Database initialization and table creation happen automatically on startup ([`database.init_db`](src/database.py)).

## API Endpoints

| Method | Endpoint             | Description                               | Payload                            |
| :----- | :------------------- | :---------------------------------------- | :--------------------------------- |
| `GET`  | `/inventory/`        | Retrieves all inventory items.            | None                               |
| `POST` | `/inventory/`        | Adds a new inventory item.                | JSON with `name`, `quantity`, `price` |
| `PUT`  | `/inventory/<item_id>` | Updates an inventory item by ID.          | JSON with fields to update         |
| `DELETE`| `/inventory/<item_id>` | Deletes an inventory item by ID.          | None                               |
| `GET`  | `/healthcheck`       | Checks app status and database connectivity. | None                               |

### Example: Adding an Item using `curl`

To add a new item named "Example Widget" with quantity 50 and price 19.95, you can use the following `curl` command (assuming the server is running locally on port 5000):

```bash
curl -X POST \
  http://localhost:5000/inventory/ \
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

## Docker

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
    docker run -it --rm \
      -p 5000:5000 \
      -v $(pwd)/src:/app \
      -v backend-dev-db-data:/app/instance \
      --name backend-dev-container \
      inventory-backend-dev
    ```
    *   `-it`: Runs the container interactively so you can see logs and stop with Ctrl+C.
    *   `--rm`: Automatically removes the container when it exits.
    *   `-v $(pwd)/src:/app`: Mounts your local `src` folder into `/app` in the container. Changes you make locally will trigger `gunicorn` to reload. **Important:** This mount overlays the code copied during the image build.
    *   `-v backend-dev-db-data:/app/instance`: Creates a named volume `backend-dev-db-data` to store the SQLite database (`instance/database.db`) persistently, separate from the container lifecycle.
    *   The API will be available at `http://localhost:5000`. Changes to Python files in your local `src` directory should cause the server inside the container to automatically restart.

## Local Development (Alternative)

If you prefer not to use Docker, you can set up a local Python environment. Instructions for this method can be found here:

*   **[Local Python Environment Setup](./docs/local-setup.md)**