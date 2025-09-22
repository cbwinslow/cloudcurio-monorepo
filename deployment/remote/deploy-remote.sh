#!/bin/bash

# Remote Deployment Script for OSINT Platform

# Configuration
REMOTE_HOST=""
REMOTE_USER=""
REMOTE_PORT="22"
REMOTE_PATH="/opt/osint-platform"
SSH_KEY=""

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

# Function to show usage
show_usage() {
    echo "Usage: $0 -h <host> -u <user> [-p <port>] [-k <ssh_key>] [-r <remote_path>]"
    echo ""
    echo "Options:"
    echo "  -h <host>         Remote host (IP or hostname)"
    echo "  -u <user>         Remote user"
    echo "  -p <port>         Remote SSH port (default: 22)"
    echo "  -k <ssh_key>      SSH private key file"
    echo "  -r <remote_path>  Remote installation path (default: /opt/osint-platform)"
    echo ""
    echo "Example:"
    echo "  $0 -h 192.168.1.100 -u deploy -k ~/.ssh/id_rsa"
}

# Function to parse command line arguments
parse_args() {
    while getopts "h:u:p:k:r:" opt; do
        case $opt in
            h)
                REMOTE_HOST=$OPTARG
                ;;
            u)
                REMOTE_USER=$OPTARG
                ;;
            p)
                REMOTE_PORT=$OPTARG
                ;;
            k)
                SSH_KEY=$OPTARG
                ;;
            r)
                REMOTE_PATH=$OPTARG
                ;;
            \?)
                print_error "Invalid option: -$OPTARG"
                show_usage
                exit 1
                ;;
            :)
                print_error "Option -$OPTARG requires an argument"
                show_usage
                exit 1
                ;;
        esac
    done
    
    # Check required arguments
    if [ -z "$REMOTE_HOST" ] || [ -z "$REMOTE_USER" ]; then
        print_error "Remote host and user are required"
        show_usage
        exit 1
    fi
}

# Function to build SSH command
build_ssh_cmd() {
    local ssh_cmd="ssh"
    
    if [ -n "$SSH_KEY" ]; then
        ssh_cmd="$ssh_cmd -i $SSH_KEY"
    fi
    
    ssh_cmd="$ssh_cmd -p $REMOTE_PORT $REMOTE_USER@$REMOTE_HOST"
    
    echo "$ssh_cmd"
}

# Function to build SCP command
build_scp_cmd() {
    local scp_cmd="scp"
    
    if [ -n "$SSH_KEY" ]; then
        scp_cmd="$scp_cmd -i $SSH_KEY"
    fi
    
    scp_cmd="$scp_cmd -P $REMOTE_PORT"
    
    echo "$scp_cmd"
}

# Function to check remote connectivity
check_remote_connectivity() {
    print_status "Checking remote connectivity to $REMOTE_HOST..."
    
    local ssh_cmd=$(build_ssh_cmd)
    
    if $ssh_cmd "echo 'Connected successfully'" &> /dev/null; then
        print_status "Remote connectivity established"
    else
        print_error "Failed to connect to remote host"
        exit 1
    fi
}

# Function to check remote prerequisites
check_remote_prerequisites() {
    print_status "Checking remote prerequisites..."
    
    local ssh_cmd=$(build_ssh_cmd)
    
    # Check if Docker is installed
    if $ssh_cmd "command -v docker" &> /dev/null; then
        print_status "Docker is installed: $($ssh_cmd "docker --version")"
    else
        print_error "Docker is not installed on the remote host"
        exit 1
    fi
    
    # Check if Docker Compose is installed
    if $ssh_cmd "command -v docker-compose" &> /dev/null; then
        print_status "Docker Compose is installed: $($ssh_cmd "docker-compose --version")"
    else
        print_error "Docker Compose is not installed on the remote host"
        exit 1
    fi
    
    # Check if Git is installed
    if $ssh_cmd "command -v git" &> /dev/null; then
        print_status "Git is installed: $($ssh_cmd "git --version")"
    else
        print_warning "Git is not installed on the remote host. Some features may not work properly."
    fi
}

# Function to create remote directory structure
create_remote_directories() {
    print_status "Creating remote directory structure..."
    
    local ssh_cmd=$(build_ssh_cmd)
    
    $ssh_cmd "mkdir -p $REMOTE_PATH" || {
        print_error "Failed to create remote directory"
        exit 1
    }
    
    $ssh_cmd "mkdir -p \
        $REMOTE_PATH/data/supabase \
        $REMOTE_PATH/data/neo4j/neo4j \
        $REMOTE_PATH/data/neo4j/plugins \
        $REMOTE_PATH/data/bitwarden \
        $REMOTE_PATH/data/n8n \
        $REMOTE_PATH/data/localai/models \
        $REMOTE_PATH/data/openwebui \
        $REMOTE_PATH/data/localrecall \
        $REMOTE_PATH/data/flowise \
        $REMOTE_PATH/data/rabbitmq \
        $REMOTE_PATH/data/prometheus \
        $REMOTE_PATH/data/grafana \
        $REMOTE_PATH/data/netdata \
        $REMOTE_PATH/data/sentry \
        $REMOTE_PATH/data/portainer \
        $REMOTE_PATH/data/ollama \
        $REMOTE_PATH/traefik/letsencrypt \
        $REMOTE_PATH/kong \
        $REMOTE_PATH/searxng \
        $REMOTE_PATH/prometheus \
        $REMOTE_PATH/fluentd/conf \
        $REMOTE_PATH/backups" || {
        print_error "Failed to create remote directory structure"
        exit 1
    }
    
    print_status "Remote directory structure created successfully!"
}

# Function to copy files to remote host
copy_files_to_remote() {
    print_status "Copying files to remote host..."
    
    local scp_cmd=$(build_scp_cmd)
    
    # Copy docker-compose.yml
    $scp_cmd docker-compose.yml $REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH/ || {
        print_error "Failed to copy docker-compose.yml"
        exit 1
    }
    
    # Copy configuration directories
    $scp_cmd -r config $REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH/ || {
        print_error "Failed to copy config directory"
        exit 1
    }
    
    # Copy scripts directory
    $scp_cmd -r scripts $REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH/ || {
        print_error "Failed to copy scripts directory"
        exit 1
    }
    
    # Copy service configuration directories
    for dir in traefik kong searxng prometheus fluentd; do
        if [ -d "$dir" ]; then
            $scp_cmd -r $dir $REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH/ || {
                print_error "Failed to copy $dir directory"
                exit 1
            }
        fi
    done
    
    print_status "Files copied to remote host successfully!"
}

# Function to pull Docker images on remote host
pull_remote_images() {
    print_status "Pulling Docker images on remote host..."
    
    local ssh_cmd=$(build_ssh_cmd)
    
    $ssh_cmd "cd $REMOTE_PATH && docker-compose pull" || {
        print_error "Failed to pull Docker images"
        exit 1
    }
    
    print_status "Docker images pulled successfully!"
}

# Function to deploy platform on remote host
deploy_remote_platform() {
    print_status "Deploying OSINT Platform on remote host..."
    
    local ssh_cmd=$(build_ssh_cmd)
    
    # Start the platform
    $ssh_cmd "cd $REMOTE_PATH && docker-compose up -d" || {
        print_error "Failed to start OSINT Platform"
        exit 1
    }
    
    print_status "OSINT Platform deployed successfully on remote host!"
}

# Function to show completion message
show_completion() {
    print_status "=========================================="
    print_status "OSINT Platform Remote Deployment Completed!"
    print_status "=========================================="
    echo ""
    print_status "Platform deployed to: $REMOTE_HOST:$REMOTE_PORT"
    print_status "Installation path: $REMOTE_PATH"
    echo ""
    print_status "Next steps:"
    print_status "1. SSH to the remote host: ssh $REMOTE_USER@$REMOTE_HOST"
    print_status "2. Navigate to the installation directory: cd $REMOTE_PATH"
    print_status "3. Check logs: ./scripts/manage-platform.sh logs"
    print_status "4. Access the platform at http://$REMOTE_HOST"
    print_status "5. Traefik Dashboard: http://$REMOTE_HOST:8080"
    print_status "6. Portainer: http://$REMOTE_HOST:9001"
    echo ""
    print_status "Management commands:"
    print_status "- Start: ./scripts/manage-platform.sh start"
    print_status "- Stop: ./scripts/manage-platform.sh stop"
    print_status "- View logs: ./scripts/manage-platform.sh logs"
    print_status "- Backup: ./scripts/manage-platform.sh backup"
    print_status "- Restore: ./scripts/manage-platform.sh restore <backup_file>"
    print_status "=========================================="
}

# Main deployment process
print_status "Starting OSINT Platform Remote Deployment..."

# Parse command line arguments
parse_args "$@"

# Check remote connectivity
check_remote_connectivity

# Check remote prerequisites
check_remote_prerequisites

# Create remote directory structure
create_remote_directories

# Copy files to remote host
copy_files_to_remote

# Pull Docker images on remote host
pull_remote_images

# Deploy platform on remote host
deploy_remote_platform

# Show completion message
show_completion

print_status "Remote deployment script completed successfully!"