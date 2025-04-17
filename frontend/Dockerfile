# --- Stage 1: Build the React application ---
FROM node:lts-alpine AS builder

# Set the working directory inside the container
WORKDIR /app

# Ensure the 'node' user owns the working directory
# The node user/group (UID/GID 1000) is created in the base image
RUN chown node:node /app

# Copy package.json and package-lock.json first, setting ownership
# This leverages Docker layer caching
COPY --chown=node:node webapp/package*.json ./

# Switch to the non-root user 'node'
USER node

# Install dependencies using npm ci for faster, reliable builds from lock file
# Ensure package-lock.json exists in webapp/ directory!
RUN npm ci

# Copy the rest of your webapp source code, setting ownership
COPY --chown=node:node webapp/ .

# Run the build command defined in your package.json
# Output goes to /app/dist by default with Vite
RUN npm run build

# --- Stage 2: Serve the built application with Nginx ---
FROM nginx:stable-alpine

# Remove default Nginx welcome page
RUN rm -rf /usr/share/nginx/html/*

# Copy the built static files from the 'builder' stage
# The builder stage created the output in /app/dist
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80 for HTTP traffic
EXPOSE 80

# Nginx image's default command starts the server, so no CMD needed unless customization is required.
# Default CMD is ["nginx", "-g", "daemon off;"]
