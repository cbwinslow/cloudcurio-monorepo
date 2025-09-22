#!/bin/bash

# OSINT Platform Management Script

# Load configuration
CONFIG_FILE="./config/osint-platform-config.yaml"

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

# Function to check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_status "Docker and Docker Compose are installed."
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
        
        # Initialize Ollama models
        print_status "Initializing Ollama models (this may take a while)..."
        ./scripts/init-ollama.sh &
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

# Function to restart the platform
restart_platform() {
    print_status "Restarting OSINT Platform..."
    docker-compose down
    sleep 5
    docker-compose up -d
    if [ $? -eq 0 ]; then
        print_status "OSINT Platform restarted successfully!"
    else
        print_error "Failed to restart OSINT Platform."
        exit 1
    fi
}

# Function to check platform status
status_platform() {
    print_status "Checking OSINT Platform status..."
    docker-compose ps
}

# Function to view logs
view_logs() {
    if [ $# -eq 0 ]; then
        print_status "Viewing all logs..."
        docker-compose logs -f
    else
        print_status "Viewing logs for $1..."
        docker-compose logs -f $1
    fi
}

# Function to backup the platform
backup_platform() {
    print_status "Creating backup of OSINT Platform..."
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    BACKUP_DIR="./backups"
    
    # Create backup directory if it doesn't exist
    mkdir -p $BACKUP_DIR
    
    # Backup data volumes
    docker-compose exec supabase-db pg_dump -U supabase supabase > "$BACKUP_DIR/supabase_backup_$TIMESTAMP.sql"
    print_status "Supabase database backup created: $BACKUP_DIR/supabase_backup_$TIMESTAMP.sql"
    
    # Backup Neo4j data
    docker-compose exec neo4j neo4j-admin dump --database=neo4j --to=/tmp/neo4j_backup.dump
    docker cp osint-neo4j:/tmp/neo4j_backup.dump "$BACKUP_DIR/neo4j_backup_$TIMESTAMP.dump"
    print_status "Neo4j database backup created: $BACKUP_DIR/neo4j_backup_$TIMESTAMP.dump"
    
    # Backup configuration
    tar -czf "$BACKUP_DIR/config_backup_$TIMESTAMP.tar.gz" ./config ./traefik ./kong ./searxng ./prometheus
    print_status "Configuration backup created: $BACKUP_DIR/config_backup_$TIMESTAMP.tar.gz"
    
    print_status "Backup completed successfully!"
}

# Function to restore the platform
restore_platform() {
    if [ $# -eq 0 ]; then
        print_error "Please specify a backup file to restore."
        exit 1
    fi
    
    BACKUP_FILE=$1
    
    if [ ! -f "$BACKUP_FILE" ]; then
        print_error "Backup file $BACKUP_FILE not found."
        exit 1
    fi
    
    print_status "Restoring OSINT Platform from $BACKUP_FILE..."
    
    # Stop the platform
    stop_platform
    
    # Restore based on file type
    if [[ "$BACKUP_FILE" == *.sql ]]; then
        # Restore Supabase database
        docker-compose up -d supabase-db
        sleep 10
        docker-compose exec -T supabase-db psql -U supabase supabase < "$BACKUP_FILE"
        print_status "Supabase database restored from $BACKUP_FILE"
    elif [[ "$BACKUP_FILE" == *.dump ]]; then
        # Restore Neo4j database
        docker-compose up -d neo4j
        sleep 10
        docker cp "$BACKUP_FILE" osint-neo4j:/tmp/neo4j_backup.dump
        docker-compose exec neo4j neo4j-admin load --from=/tmp/neo4j_backup.dump --database=neo4j --force
        print_status "Neo4j database restored from $BACKUP_FILE"
    elif [[ "$BACKUP_FILE" == *.tar.gz ]]; then
        # Restore configuration
        tar -xzf "$BACKUP_FILE"
        print_status "Configuration restored from $BACKUP_FILE"
    else
        print_error "Unknown backup file type."
        exit 1
    fi
    
    # Restart the platform
    start_platform
    
    print_status "Restore completed successfully!"
}

# Function to update the platform
update_platform() {
    print_status "Updating OSINT Platform..."
    
    # Pull latest images
    docker-compose pull
    
    # Recreate containers with new images
    docker-compose up -d --force-recreate
    
    print_status "OSINT Platform updated successfully!"
}

# Function to show help
show_help() {
    echo "OSINT Platform Management Script"
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  start     - Start the OSINT Platform"
    echo "  stop      - Stop the OSINT Platform"
    echo "  restart   - Restart the OSINT Platform"
    echo "  status    - Show status of OSINT Platform services"
    echo "  logs      - View logs (optionally specify service name)"
    echo "  backup    - Create a backup of the platform"
    echo "  restore   - Restore the platform from a backup file"
    echo "  update    - Update the platform to the latest versions"
    echo "  help      - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start"
    echo "  $0 logs beef"
    echo "  $0 restore ./backups/supabase_backup_20230101_120000.sql"
}

# Main script logic
case "$1" in
    start)
        check_docker
        start_platform
        ;;
    stop)
        check_docker
        stop_platform
        ;;
    restart)
        check_docker
        restart_platform
        ;;
    status)
        check_docker
        status_platform
        ;;
    logs)
        check_docker
        shift
        view_logs $@
        ;;
    backup)
        check_docker
        backup_platform
        ;;
    restore)
        check_docker
        shift
        restore_platform $@
        ;;
    update)
        check_docker
        update_platform
        ;;
    help)
        show_help
        ;;
    *)
        show_help
        exit 1
        ;;
esac