#!/bin/bash

# OSINT Platform Setup Script

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    else
        print_status "Docker is installed: $(docker --version)"
    fi
    
    # Check if Docker Compose is installed
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    else
        print_status "Docker Compose is installed: $(docker-compose --version)"
    fi
    
    # Check if Git is installed
    if ! command -v git &> /dev/null; then
        print_warning "Git is not installed. Some features may not work properly."
    else
        print_status "Git is installed: $(git --version)"
    fi
    
    print_status "All prerequisites checked successfully!"
}

# Function to create directory structure
create_directories() {
    print_status "Creating directory structure..."
    
    mkdir -p \
        traefik/letsencrypt \
        kong \
        searxng \
        data/supabase \
        data/neo4j/neo4j \
        data/neo4j/plugins \
        data/bitwarden \
        data/n8n \
        data/localai/models \
        data/openwebui \
        data/localrecall \
        data/flowise \
        data/rabbitmq \
        prometheus \
        data/prometheus \
        data/grafana \
        data/netdata \
        fluentd/conf \
        data/sentry \
        config \
        scripts \
        backups
    
    print_status "Directory structure created successfully!"
}

# Function to generate certificates for Traefik
generate_certificates() {
    print_status "Setting up Traefik certificates..."
    
    # Create empty acme.json file with correct permissions
    touch traefik/letsencrypt/acme.json
    chmod 600 traefik/letsencrypt/acme.json
    
    print_status "Traefik certificates setup completed!"
}

# Function to pull Docker images
pull_images() {
    print_status "Pulling Docker images..."
    
    # List of images to pull
    IMAGES=(
        "traefik:v2.10"
        "kong:3.4"
        "supabase/postgres:15.1.0.147"
        "neo4j:5.12"
        "bitwarden/self-host:beta"
        "searxng/searxng:latest"
        "n8nio/n8n:latest"
        "quay.io/go-skynet/local-ai:latest"
        "ghcr.io/openwebui/openwebui:main"
        "ghcr.io/mudler/localrecall:latest"
        "flowiseai/flowise:latest"
        "ghcr.io/modelcontextprotocol/server:latest"
        "rabbitmq:3-management"
        "prom/prometheus:latest"
        "grafana/grafana-enterprise"
        "netdata/netdata:latest"
        "grafana/loki:latest"
        "fluent/fluentd:latest"
        "sentry:latest"
        "redis:latest"
        "ghcr.io/archon-sec/archon:latest"
    )
    
    for image in "${IMAGES[@]}"; do
        print_status "Pulling $image..."
        docker pull $image
    done
    
    print_status "All Docker images pulled successfully!"
}

# Function to initialize databases
initialize_databases() {
    print_status "Initializing databases..."
    
    # Start only the database services
    docker-compose up -d supabase-db neo4j
    
    # Wait for services to start
    print_status "Waiting for databases to start..."
    sleep 30
    
    # Initialize Neo4j
    print_status "Initializing Neo4j..."
    # Set initial password
    docker-compose exec neo4j cypher-shell -u neo4j -p neo4j -d system "ALTER USER neo4j SET PASSWORD 'neo4j123'"
    
    print_status "Databases initialized successfully!"
}

# Function to create initial configurations
create_initial_configs() {
    print_status "Creating initial configurations..."
    
    # Check if config files already exist
    if [ ! -f "config/osint-platform-config.yaml" ]; then
        print_warning "Main configuration file not found. Please create it manually."
    fi
    
    # Check if Traefik config exists
    if [ ! -f "traefik/traefik.yml" ]; then
        print_warning "Traefik configuration not found. Please create it manually."
    fi
    
    # Check if Kong config exists
    if [ ! -f "kong/kong.yml" ]; then
        print_warning "Kong configuration not found. Please create it manually."
    fi
    
    # Check if Prometheus config exists
    if [ ! -f "prometheus/prometheus.yml" ]; then
        print_warning "Prometheus configuration not found. Please create it manually."
    fi
    
    # Check if SearXNG config exists
    if [ ! -f "searxng/settings.yml" ]; then
        print_warning "SearXNG configuration not found. Please create it manually."
    fi
    
    print_status "Initial configurations checked!"
}

# Function to show completion message
show_completion() {
    print_status "=========================================="
    print_status "OSINT Platform Setup Completed!"
    print_status "=========================================="
    echo ""
    print_status "Next steps:"
    print_status "1. Review the configuration files in the config/ directory"
    print_status "2. Start the platform using: ./scripts/manage-platform.sh start"
    print_status "3. Access the platform at http://localhost"
    print_status "4. Traefik Dashboard: http://localhost:8080"
    echo ""
    print_status "Default credentials:"
    print_status "- BeEF: beef / SecurePassword123!"
    print_status "- Grafana: admin / grafana123"
    print_status "- Neo4j: neo4j / neo4j123"
    print_status "- RabbitMQ: rabbitmq / rabbitmq123"
    echo ""
    print_status "Management commands:"
    print_status "- Start: ./scripts/manage-platform.sh start"
    print_status "- Stop: ./scripts/manage-platform.sh stop"
    print_status "- View logs: ./scripts/manage-platform.sh logs"
    print_status "- Backup: ./scripts/manage-platform.sh backup"
    print_status "- Restore: ./scripts/manage-platform.sh restore <backup_file>"
    print_status "=========================================="
}

# Main setup process
print_status "Starting OSINT Platform Setup..."

# Check prerequisites
check_prerequisites

# Create directory structure
create_directories

# Generate certificates
generate_certificates

# Pull Docker images
pull_images

# Initialize databases
initialize_databases

# Create initial configurations
create_initial_configs

# Show completion message
show_completion

print_status "Setup script completed successfully!"