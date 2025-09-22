#!/bin/bash

# Podman Compose Compatibility Script

# This script provides compatibility between Docker Compose and Podman Compose

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

# Function to check if podman-compose is installed
check_podman_compose() {
    if ! command -v podman-compose &> /dev/null; then
        print_error "podman-compose is not installed"
        print_status "Installing podman-compose..."
        
        # Try to install podman-compose
        if command -v pip3 &> /dev/null; then
            pip3 install podman-compose
        elif command -v pip &> /dev/null; then
            pip install podman-compose
        else
            print_error "Neither pip3 nor pip is installed. Please install pip first."
            exit 1
        fi
    fi
    
    print_status "podman-compose is installed: $(podman-compose --version)"
}

# Function to convert docker-compose.yml for Podman
convert_compose_file() {
    print_status "Converting docker-compose.yml for Podman compatibility..."
    
    # Create a backup of the original file
    cp docker-compose.yml docker-compose.yml.backup
    
    # Remove or modify incompatible options
    # This is a simple example - in practice, you might need more complex transformations
    sed -i 's/docker.sock/podman.sock/g' docker-compose.yml
    sed -i 's/\/var\/run\/docker.sock/\/run\/podman\/podman.sock/g' docker-compose.yml
    
    print_status "docker-compose.yml converted for Podman compatibility"
}

# Function to start services with Podman Compose
podman_compose_up() {
    print_status "Starting services with Podman Compose..."
    
    podman-compose up -d "$@"
    
    if [ $? -eq 0 ]; then
        print_status "Services started successfully with Podman Compose"
    else
        print_error "Failed to start services with Podman Compose"
        exit 1
    fi
}

# Function to stop services with Podman Compose
podman_compose_down() {
    print_status "Stopping services with Podman Compose..."
    
    podman-compose down "$@"
    
    if [ $? -eq 0 ]; then
        print_status "Services stopped successfully with Podman Compose"
    else
        print_error "Failed to stop services with Podman Compose"
        exit 1
    fi
}

# Function to show help
show_help() {
    echo "Podman Compose Compatibility Script"
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  up      - Start services with Podman Compose"
    echo "  down    - Stop services with Podman Compose"
    echo "  convert - Convert docker-compose.yml for Podman compatibility"
    echo "  help    - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 up"
    echo "  $0 down"
    echo "  $0 convert"
}

# Main script logic
case "$1" in
    up)
        check_podman_compose
        podman_compose_up "${@:2}"
        ;;
    down)
        check_podman_compose
        podman_compose_down "${@:2}"
        ;;
    convert)
        convert_compose_file
        ;;
    help)
        show_help
        ;;
    *)
        show_help
        exit 1
        ;;
esac