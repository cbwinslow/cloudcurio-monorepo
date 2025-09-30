#!/bin/bash

# CloudCurio Docker Build and Push Script

set -e  # Exit on any error

# Check if required commands are available
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed or not in PATH. Please install Docker first."
    exit 1
fi

# Check if user is logged into Docker Hub
if ! docker info &> /dev/null; then
    echo "Docker daemon is not running. Please start Docker and try again."
    exit 1
fi

# Check if user is logged into Docker Hub
if ! docker system info | grep -q "Username:"; then
    echo "You are not logged into Docker Hub. Please run 'docker login' first."
    exit 1
fi

# Get the version from command line argument or use default
VERSION=${1:-latest}

# Docker Hub repository name (change this as needed)
REPO_NAME="cbwinslow/cloudcurio-mcp"

echo "Building CloudCurio MCP Server Docker image..."

# Build the Docker image
docker build -f Dockerfile.mcp -t $REPO_NAME:$VERSION .

echo "Docker image built successfully."

# Tag the image as latest as well if not already
if [ "$VERSION" != "latest" ]; then
    echo "Tagging with 'latest' as well..."
    docker tag $REPO_NAME:$VERSION $REPO_NAME:latest
fi

echo "Pushing image to Docker Hub..."

# Push the image to Docker Hub
docker push $REPO_NAME:$VERSION

# Push the latest tag as well if not already
if [ "$VERSION" != "latest" ]; then
    docker push $REPO_NAME:latest
fi

echo "Docker image pushed successfully to $REPO_NAME:$VERSION"
echo "You can now run the container with:"
echo "  docker run -p 8000:8000 -e OPENAI_API_KEY=your_key_here $REPO_NAME:$VERSION"