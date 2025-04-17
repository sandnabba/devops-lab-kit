# --- Base Stage ---
# Contains common setup for both prod and dev
FROM python:3.12-slim AS base

# Install curl (useful for healthcheck in prod, potentially dev)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Use --no-cache-dir to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code from the src directory
# This is done in the base stage so both prod and dev have access
# For dev, this will be overlaid by the volume mount, but it's needed for the build context
COPY src/ .

# --- Production Stage (default) ---
# Builds on 'base' and sets up for production
FROM base AS prod
# No need to copy files again, they are inherited from 'base'

# Make port 5000 available
EXPOSE 5000

# Add healthcheck instruction for production
HEALTHCHECK --interval=10s --timeout=5s --start-period=15s --retries=1 \
  CMD curl -f http://localhost:5000/healthcheck || exit 1

# Define environment variables for Flask production
ENV FLASK_APP=app
ENV FLASK_ENV=production

# Run the application using Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--access-logfile", "-", "app:app"]


# --- Development Stage ---
# Builds on 'base' and sets up for development with reload
FROM base AS dev
# No need to copy files again, they are inherited from 'base'

# Make port 5000 available
EXPOSE 5000

# Define environment variable for Flask (dev is default, but explicit is fine)
ENV FLASK_APP=app
# ENV FLASK_ENV=development # Optional: Explicitly set if needed

# Run the application using Gunicorn with reload enabled for development
# Note: Source code should be mounted via volume when running this stage
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--reload", "--access-logfile", "-", "app:app"]

# Note: The final stage in the Dockerfile without an alias is the default build target (prod in this case).
# To build the 'dev' stage, use 'docker build --target dev ...'