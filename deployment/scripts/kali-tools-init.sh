#!/bin/bash

# Kali Linux Tools Initialization Script

# Configuration
KALI_CONTAINER_NAME="osint-kali"
KALI_DATA_DIR="./data/kali"

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

# Function to check if Docker is running
check_docker() {
    if ! docker info &> /dev/null; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
}

# Function to build Kali Linux container
build_kali_container() {
    print_status "Building Kali Linux container..."
    
    # Create data directory
    mkdir -p "$KALI_DATA_DIR"
    
    # Build the container
    docker build -t kali-osint ./deployment/docker/kali-osint
    
    if [ $? -eq 0 ]; then
        print_status "Kali Linux container built successfully"
    else
        print_error "Failed to build Kali Linux container"
        exit 1
    fi
}

# Function to start Kali Linux container
start_kali_container() {
    print_status "Starting Kali Linux container..."
    
    # Check if container is already running
    if docker ps | grep -q "$KALI_CONTAINER_NAME"; then
        print_status "Kali Linux container is already running"
        return
    fi
    
    # Start the container
    docker run -d \
        --name "$KALI_CONTAINER_NAME" \
        --privileged \
        -v "$KALI_DATA_DIR:/opt/osint/data" \
        -p 8086:80 \
        -p 8443:443 \
        kali-osint
    
    if [ $? -eq 0 ]; then
        print_status "Kali Linux container started successfully"
    else
        print_error "Failed to start Kali Linux container"
        exit 1
    fi
}

# Function to install additional Kali tools
install_kali_tools() {
    print_status "Installing additional Kali Linux tools..."
    
    # Tools to install
    TOOLS=(
        "recon-ng"
        "maltego"
        " eyewitness"
        "spiderfoot"
        "datasploit"
        "osrframework"
        "sn0int"
        "intrigue-core"
        "golismero"
        "dnsrecon"
        "fierce"
        "wafw00f"
        "sslscan"
        "testssl.sh"
        "amass"
        "subfinder"
        "assetfinder"
        "httprobe"
        "httpx"
        "nuclei"
        "ffuf"
        "wfuzz"
    )
    
    # Install tools in the container
    for tool in "${TOOLS[@]}"; do
        print_status "Installing $tool..."
        docker exec "$KALI_CONTAINER_NAME" apt-get install -y "$tool" || {
            print_warning "Failed to install $tool"
        }
    done
    
    print_status "Additional Kali tools installation completed"
}

# Function to configure Kali tools
configure_kali_tools() {
    print_status "Configuring Kali Linux tools..."
    
    # Create configuration directories
    docker exec "$KALI_CONTAINER_NAME" mkdir -p /opt/osint/config
    
    # Configure common tools
    # This is a placeholder - in practice, you would configure each tool individually
    docker exec "$KALI_CONTAINER_NAME" bash -c 'echo "Kali tools configured" > /opt/osint/config/README.md'
    
    print_status "Kali tools configuration completed"
}

# Function to test Kali tools
test_kali_tools() {
    print_status "Testing Kali Linux tools..."
    
    # Test basic tools
    TOOLS_TO_TEST=("nmap" "curl" "wget" "python3" "git")
    
    for tool in "${TOOLS_TO_TEST[@]}"; do
        if docker exec "$KALI_CONTAINER_NAME" command -v "$tool" &> /dev/null; then
            version=$(docker exec "$KALI_CONTAINER_NAME" "$tool" --version 2>/dev/null || echo "Version info not available")
            print_status "$tool is available: $version"
        else
            print_warning "$tool is not available"
        fi
    done
    
    print_status "Kali tools testing completed"
}

# Function to show completion message
show_completion() {
    print_status "=========================================="
    print_status "Kali Linux Tools Initialization Completed!"
    print_status "=========================================="
    echo ""
    print_status "Container name: $KALI_CONTAINER_NAME"
    print_status "Data directory: $KALI_DATA_DIR"
    print_status "Exposed ports: 8086 (HTTP), 8443 (HTTPS)"
    echo ""
    print_status "Next steps:"
    print_status "1. Access the container: docker exec -it $KALI_CONTAINER_NAME bash"
    print_status "2. Use Kali tools for OSINT operations"
    print_status "3. Store data in $KALI_DATA_DIR"
    echo ""
    print_status "Management commands:"
    print_status "- Start container: docker start $KALI_CONTAINER_NAME"
    print_status "- Stop container: docker stop $KALI_CONTAINER_NAME"
    print_status "- View logs: docker logs $KALI_CONTAINER_NAME"
    print_status "=========================================="
}

# Main initialization process
print_status "Starting Kali Linux Tools Initialization..."

# Check if Docker is running
check_docker

# Build Kali Linux container
build_kali_container

# Start Kali Linux container
start_kali_container

# Install additional Kali tools
install_kali_tools

# Configure Kali tools
configure_kali_tools

# Test Kali tools
test_kali_tools

# Show completion message
show_completion

print_status "Kali Linux tools initialization script completed successfully!"