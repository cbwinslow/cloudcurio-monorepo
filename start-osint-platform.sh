#!/bin/bash

# OSINT Platform Starter Script

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

print_header() {
    echo -e "${BLUE}$1${NC}"
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

# Function to show platform information
show_platform_info() {
    print_header "=========================================="
    print_header "     OSINT Platform - Starter Script      "
    print_header "=========================================="
    echo ""
    print_status "Welcome to the OSINT Platform!"
    print_status "This script will help you get started with the platform."
    echo ""
    print_status "The OSINT Platform includes:"
    print_status "  • 20+ integrated OSINT tools"
    print_status "  • Local AI models with LLM inference"
    print_status "  • Kali Linux and BlackArch tools"
    print_status "  • Comprehensive monitoring and logging"
    print_status "  • Plugin system for extensibility"
    print_status "  • Automated deployment and management"
    echo ""
    print_header "=========================================="
}

# Function to show menu
show_menu() {
    echo ""
    print_header "Main Menu:"
    echo "  1. Install OSINT Platform"
    echo "  2. Start OSINT Platform"
    echo "  3. Stop OSINT Platform"
    echo "  4. View Platform Status"
    echo "  5. View Platform Logs"
    echo "  6. Update OSINT Platform"
    echo "  7. Backup OSINT Platform"
    echo "  8. Restore OSINT Platform"
    echo "  9. Show Platform Information"
    echo "  10. Exit"
    echo ""
    read -p "Select an option (1-10): " choice
}

# Function to install the platform
install_platform() {
    print_status "Installing OSINT Platform..."
    
    # Check prerequisites
    check_prerequisites
    
    # Create directory structure
    print_status "Creating directory structure..."
    mkdir -p \
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
        data/prometheus \
        data/grafana \
        data/netdata \
        data/sentry \
        data/portainer \
        data/ollama \
        data/kali \
        data/blackarch \
        data/mcp \
        traefik/letsencrypt \
        kong \
        searxng \
        prometheus \
        fluentd/conf \
        backups
    
    # Set permissions
    print_status "Setting permissions..."
    chmod 600 traefik/letsencrypt/acme.json 2>/dev/null || touch traefik/letsencrypt/acme.json && chmod 600 traefik/letsencrypt/acme.json
    
    # Pull Docker images
    print_status "Pulling Docker images (this may take a while)..."
    docker-compose pull
    
    # Initialize databases
    print_status "Initializing databases..."
    docker-compose up -d supabase-db neo4j
    
    # Wait for services to start
    print_status "Waiting for databases to start..."
    sleep 30
    
    # Initialize Neo4j
    print_status "Initializing Neo4j..."
    docker-compose exec neo4j cypher-shell -u neo4j -p neo4j -d system "ALTER USER neo4j SET PASSWORD 'neo4j123'" 2>/dev/null || true
    
    # Initialize Ollama models
    print_status "Initializing Ollama models..."
    ./scripts/init-ollama.sh &
    
    print_status "OSINT Platform installation completed!"
    print_status "You can now start the platform using option 2."
}

# Function to start the platform
start_platform() {
    print_status "Starting OSINT Platform..."
    docker-compose up -d
    
    if [ $? -eq 0 ]; then
        print_status "OSINT Platform started successfully!"
        print_status "Access the platform at http://localhost"
        print_status "Traefik Dashboard: http://localhost:8080"
        print_status "Portainer: http://localhost:9001"
        print_status "Grafana: http://localhost:3001"
        print_status "Prometheus: http://localhost:9090"
    else
        print_error "Failed to start OSINT Platform."
        exit 1
    fi
}

# Function to stop the platform
stop_platform() {
    print_status "Stopping OSINT Platform..."
    docker-compose down
    
    if [ $? -eq 0 ]; then
        print_status "OSINT Platform stopped successfully!"
    else
        print_error "Failed to stop OSINT Platform."
        exit 1
    fi
}

# Function to check platform status
status_platform() {
    print_status "Checking OSINT Platform status..."
    docker-compose ps
}

# Function to view platform logs
logs_platform() {
    print_status "Viewing OSINT Platform logs..."
    docker-compose logs -f --tail=50
}

# Function to update the platform
update_platform() {
    print_status "Updating OSINT Platform..."
    
    # Pull latest images
    print_status "Pulling latest Docker images..."
    docker-compose pull
    
    # Recreate containers with new images
    print_status "Recreating containers with updated images..."
    docker-compose up -d --force-recreate
    
    print_status "OSINT Platform updated successfully!"
}

# Function to backup the platform
backup_platform() {
    print_status "Creating backup of OSINT Platform..."
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    BACKUP_DIR="./backups"
    
    # Create backup directory if it doesn't exist
    mkdir -p $BACKUP_DIR
    
    # Backup data volumes
    print_status "Backing up databases..."
    docker-compose exec supabase-db pg_dump -U supabase supabase > "$BACKUP_DIR/supabase_backup_$TIMESTAMP.sql" 2>/dev/null || true
    print_status "Supabase database backup created: $BACKUP_DIR/supabase_backup_$TIMESTAMP.sql"
    
    # Backup Neo4j data
    docker-compose exec neo4j neo4j-admin dump --database=neo4j --to=/tmp/neo4j_backup.dump 2>/dev/null || true
    docker cp osint-neo4j:/tmp/neo4j_backup.dump "$BACKUP_DIR/neo4j_backup_$TIMESTAMP.dump" 2>/dev/null || true
    print_status "Neo4j database backup created: $BACKUP_DIR/neo4j_backup_$TIMESTAMP.dump"
    
    # Backup configuration
    print_status "Backing up configuration..."
    tar -czf "$BACKUP_DIR/config_backup_$TIMESTAMP.tar.gz" ./config ./traefik ./kong ./searxng ./prometheus 2>/dev/null || true
    print_status "Configuration backup created: $BACKUP_DIR/config_backup_$TIMESTAMP.tar.gz"
    
    print_status "Backup completed successfully!"
}

# Function to restore the platform
restore_platform() {
    print_status "Listing available backups..."
    ls -la ./backups/
    
    read -p "Enter the backup file to restore: " backup_file
    
    if [ ! -f "./backups/$backup_file" ]; then
        print_error "Backup file $backup_file not found."
        return
    fi
    
    print_status "Restoring OSINT Platform from $backup_file..."
    
    # Stop the platform
    stop_platform
    
    # Restore based on file type
    if [[ "$backup_file" == *.sql ]]; then
        # Restore Supabase database
        print_status "Restoring Supabase database..."
        docker-compose up -d supabase-db
        sleep 10
        docker-compose exec -T supabase-db psql -U supabase supabase < "./backups/$backup_file"
        print_status "Supabase database restored from $backup_file"
    elif [[ "$backup_file" == *.dump ]]; then
        # Restore Neo4j database
        print_status "Restoring Neo4j database..."
        docker-compose up -d neo4j
        sleep 10
        docker cp "./backups/$backup_file" osint-neo4j:/tmp/neo4j_backup.dump
        docker-compose exec neo4j neo4j-admin load --from=/tmp/neo4j_backup.dump --database=neo4j --force
        print_status "Neo4j database restored from $backup_file"
    elif [[ "$backup_file" == *.tar.gz ]]; then
        # Restore configuration
        print_status "Restoring configuration..."
        tar -xzf "./backups/$backup_file"
        print_status "Configuration restored from $backup_file"
    else
        print_error "Unknown backup file type."
        return
    fi
    
    # Restart the platform
    start_platform
    
    print_status "Restore completed successfully!"
}

# Main script logic
show_platform_info

while true; do
    show_menu
    
    case $choice in
        1)
            install_platform
            ;;
        2)
            start_platform
            ;;
        3)
            stop_platform
            ;;
        4)
            status_platform
            ;;
        5)
            logs_platform
            ;;
        6)
            update_platform
            ;;
        7)
            backup_platform
            ;;
        8)
            restore_platform
            ;;
        9)
            show_platform_info
            ;;
        10)
            print_status "Thank you for using the OSINT Platform!"
            exit 0
            ;;
        *)
            print_error "Invalid option. Please select a number between 1 and 10."
            ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
done