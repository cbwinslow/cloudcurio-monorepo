#!/bin/bash

# CloudCurio Open WebUI Setup Script

set -e  # Exit on any error

echo "Setting up CloudCurio Open WebUI Integration..."

# Create necessary directories
mkdir -p open_webui_data
mkdir -p ollama_data
mkdir -p open_webui_config

# Create a default environment file
cat << 'EOF' > .env.openwebui
# CloudCurio Open WebUI Environment Configuration

# Open WebUI Settings
WEBUI_SECRET_KEY=$(openssl rand -base64 32)
WEBUI_AUTH=false
DEFAULT_MODEL=llama3
ENABLE_RAG_WEB_SEARCH=true
RAG_WEB_SEARCH_ENGINE=duckduckgo

# API URLs
OLLAMA_BASE_URL=http://localhost:11434
OPENAI_API_BASE_URLS=
API_BASE_URL=http://localhost:8000

# OpenAI Settings (if using OpenAI models)
OPENAI_API_KEY=your-openai-api-key-here

# Google Gemini Settings (if using Gemini models)
GEMINI_API_KEY=your-gemini-api-key-here

# Anthropic Settings (if using Claude models)
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# CloudCurio MCP Server Settings
MCP_SERVER_URL=http://localhost:8000
EOF

echo "Environment file created at .env.openwebui"

# Create a startup script for Open WebUI
cat << 'EOF' > start_open_webui.sh
#!/bin/bash

# Start CloudCurio Open WebUI and related services

echo "Starting CloudCurio Open WebUI Stack..."

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! command -v docker compose &> /dev/null; then
    echo "Error: Docker Compose is not installed."
    echo "Please install Docker Desktop or Docker Compose separately."
    exit 1
fi

# Use the correct command for Docker Compose
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
else
    COMPOSE_CMD="docker compose"
fi

# Start the services
echo "Starting services..."
cd open_webui
$COMPOSE_CMD up -d

echo "Services started successfully!"
echo ""
echo "Open WebUI should be available at: http://localhost:3000"
echo "Ollama should be available at: http://localhost:11434"
echo "LiteLLM should be available at: http://localhost:4000"
echo ""
echo "To view logs: $COMPOSE_CMD logs -f"
echo "To stop services: $COMPOSE_CMD down"
EOF

chmod +x start_open_webui.sh

echo "Open WebUI startup script created at start_open_webui.sh"

# Create a shutdown script
cat << 'EOF' > stop_open_webui.sh
#!/bin/bash

# Stop CloudCurio Open WebUI and related services

echo "Stopping CloudCurio Open WebUI Stack..."

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! command -v docker compose &> /dev/null; then
    echo "Error: Docker Compose is not installed."
    echo "Please install Docker Desktop or Docker Compose separately."
    exit 1
fi

# Use the correct command for Docker Compose
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
else
    COMPOSE_CMD="docker compose"
fi

# Stop the services
cd open_webui
$COMPOSE_CMD down

echo "Services stopped successfully!"
EOF

chmod +x stop_open_webui.sh

echo "Open WebUI shutdown script created at stop_open_webui.sh"

# Create a script to pull and run a single Open WebUI container (alternative to compose)
cat << 'EOF' > run_open_webui.sh
#!/bin/bash

# Run Open WebUI with Docker (single container, no compose)

echo "Running Open WebUI with Docker..."

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed."
    exit 1
fi

# Check if the data directory exists, create if not
if [ ! -d "open_webui_data" ]; then
    mkdir -p open_webui_data
fi

# Run Open WebUI container
docker run -d \
    --name cloudcurio-open-webui \
    -p 3000:8080 \
    -v $(pwd)/open_webui_data:/app/backend/data \
    --add-host=host.docker.internal:host-gateway \
    -e OLLAMA_BASE_URL="http://host.docker.internal:11434" \
    -e WEBUI_SECRET_KEY="$(openssl rand -base64 32)" \
    -e WEBUI_AUTH="false" \
    --restart unless-stopped \
    ghcr.io/open-webui/open-webui:main

echo "Open WebUI is now running!"
echo "Access it at: http://localhost:3000"
EOF

chmod +x run_open_webui.sh

echo "Single container script created at run_open_webui.sh"

echo ""
echo "Open WebUI setup completed!"
echo ""
echo "To start the full stack with Docker Compose:"
echo "  ./start_open_webui.sh"
echo ""
echo "To run just Open WebUI (single container):"
echo "  ./run_open_webui.sh"
echo ""
echo "To stop the services:"
echo "  ./stop_open_webui.sh"
echo ""
echo "Open WebUI will be available at http://localhost:3000"