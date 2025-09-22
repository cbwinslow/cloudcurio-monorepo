#!/bin/bash

# Podman Configuration Script for OSINT Platform

# Configuration
PODMAN_SOCKET="/run/podman/podman.sock"
PODMAN_DATA_DIR="./data/podman"

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

# Function to check if Podman is installed
check_podman() {
    print_status "Checking if Podman is installed..."
    
    if ! command -v podman &> /dev/null; then
        print_error "Podman is not installed. Please install Podman first."
        exit 1
    else
        print_status "Podman is installed: $(podman --version)"
    fi
    
    # Check if podman-compose is installed
    if ! command -v podman-compose &> /dev/null; then
        print_warning "podman-compose is not installed. Some features may not work properly."
    else
        print_status "podman-compose is installed: $(podman-compose --version)"
    fi
}

# Function to create Podman directories
create_podman_directories() {
    print_status "Creating Podman directories..."
    
    mkdir -p "$PODMAN_DATA_DIR"
    
    # Create socket directory if it doesn't exist
    SOCKET_DIR=$(dirname "$PODMAN_SOCKET")
    if [ ! -d "$SOCKET_DIR" ]; then
        sudo mkdir -p "$SOCKET_DIR"
    fi
    
    print_status "Podman directories created successfully!"
}

# Function to configure Podman socket
configure_podman_socket() {
    print_status "Configuring Podman socket..."
    
    # Check if socket already exists
    if [ -S "$PODMAN_SOCKET" ]; then
        print_status "Podman socket already exists"
        return
    fi
    
    # Start Podman socket service
    if systemctl is-active --quiet podman.socket; then
        print_status "Podman socket service is already running"
    else
        print_status "Starting Podman socket service..."
        sudo systemctl start podman.socket
        
        if systemctl is-active --quiet podman.socket; then
            print_status "Podman socket service started successfully"
        else
            print_warning "Failed to start Podman socket service"
        fi
    fi
    
    # Create symlink to Docker socket for compatibility
    if [ ! -S "/var/run/docker.sock" ]; then
        sudo ln -sf "$PODMAN_SOCKET" /var/run/docker.sock
        print_status "Created symlink to Docker socket for compatibility"
    fi
}

# Function to create Podman systemd service
create_podman_service() {
    print_status "Creating Podman systemd service..."
    
    # Create service file
    sudo tee /etc/systemd/system/osint-podman.service > /dev/null << EOF
[Unit]
Description=OSINT Platform Podman Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/podman system service --time=0
KillMode=process

[Install]
WantedBy=multi-user.target
EOF
    
    # Reload systemd and enable service
    sudo systemctl daemon-reload
    sudo systemctl enable osint-podman.service
    
    print_status "Podman systemd service created and enabled"
}

# Function to test Podman configuration
test_podman_configuration() {
    print_status "Testing Podman configuration..."
    
    # Test basic Podman commands
    if podman info &> /dev/null; then
        print_status "Podman is working correctly"
    else
        print_warning "Podman is not working correctly"
    fi
    
    # Test Docker compatibility
    if docker info &> /dev/null; then
        print_status "Docker compatibility is working"
    else
        print_warning "Docker compatibility is not working"
    fi
}

# Function to show completion message
show_completion() {
    print_status "=========================================="
    print_status "Podman Configuration Completed!"
    print_status "=========================================="
    echo ""
    print_status "Next steps:"
    print_status "1. Start the OSINT Platform with Podman: podman-compose up -d"
    print_status "2. Access Portainer at http://localhost:9001"
    print_status "3. Use Podman commands to manage containers"
    echo ""
    print_status "Podman commands:"
    print_status "- podman ps (list containers)"
    print_status "- podman logs <container> (view logs)"
    print_status "- podman exec -it <container> bash (enter container)"
    print_status "- podman-compose up -d (start platform)"
    print_status "- podman-compose down (stop platform)"
    print_status "=========================================="
}

# Main configuration process
print_status "Starting Podman Configuration..."

# Check if Podman is installed
check_podman

# Create Podman directories
create_podman_directories

# Configure Podman socket
configure_podman_socket

# Create Podman systemd service
create_podman_service

# Test Podman configuration
test_podman_configuration

# Show completion message
show_completion

print_status "Podman configuration script completed successfully!"