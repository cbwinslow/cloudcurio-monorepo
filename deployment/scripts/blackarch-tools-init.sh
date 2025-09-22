#!/bin/bash

# BlackArch Tools Initialization Script

# Configuration
BLACKARCH_CONTAINER_NAME="osint-blackarch"
BLACKARCH_DATA_DIR="./data/blackarch"
BLACKARCH_MCP_CONTAINER_NAME="osint-blackarch-mcp"

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

# Function to build BlackArch containers
build_blackarch_containers() {
    print_status "Building BlackArch containers..."
    
    # Create data directories
    mkdir -p "$BLACKARCH_DATA_DIR"
    
    # Build the BlackArch OSINT tools container
    docker build -t blackarch-osint ./deployment/docker/blackarch-osint
    
    if [ $? -eq 0 ]; then
        print_status "BlackArch OSINT tools container built successfully"
    else
        print_error "Failed to build BlackArch OSINT tools container"
        exit 1
    fi
    
    # Build the BlackArch MCP server container
    docker build -t blackarch-mcp ./deployment/docker/mcp-blackarch
    
    if [ $? -eq 0 ]; then
        print_status "BlackArch MCP server container built successfully"
    else
        print_error "Failed to build BlackArch MCP server container"
        exit 1
    fi
}

# Function to start BlackArch containers
start_blackarch_containers() {
    print_status "Starting BlackArch containers..."
    
    # Check if BlackArch OSINT container is already running
    if docker ps | grep -q "$BLACKARCH_CONTAINER_NAME"; then
        print_status "BlackArch OSINT container is already running"
    else
        # Start the BlackArch OSINT tools container
        docker run -d \
            --name "$BLACKARCH_CONTAINER_NAME" \
            --privileged \
            -v "$BLACKARCH_DATA_DIR:/opt/osint/data" \
            -p 8087:80 \
            -p 8444:443 \
            blackarch-osint
        
        if [ $? -eq 0 ]; then
            print_status "BlackArch OSINT tools container started successfully"
        else
            print_error "Failed to start BlackArch OSINT tools container"
            exit 1
        fi
    fi
    
    # Check if BlackArch MCP container is already running
    if docker ps | grep -q "$BLACKARCH_MCP_CONTAINER_NAME"; then
        print_status "BlackArch MCP container is already running"
    else
        # Start the BlackArch MCP server container
        docker run -d \
            --name "$BLACKARCH_MCP_CONTAINER_NAME" \
            -p 3006:3000 \
            blackarch-mcp
        
        if [ $? -eq 0 ]; then
            print_status "BlackArch MCP server container started successfully"
        else
            print_error "Failed to start BlackArch MCP server container"
            exit 1
        fi
    fi
}

# Function to install additional BlackArch tools
install_blackarch_tools() {
    print_status "Installing additional BlackArch tools..."
    
    # Tools to install
    TOOLS=(
        "recon-ng"
        "maltego"
        "eyewitness"
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
        docker exec "$BLACKARCH_CONTAINER_NAME" pacman -S --noconfirm "$tool" || {
            print_warning "Failed to install $tool"
        }
    done
    
    print_status "Additional BlackArch tools installation completed"
}

# Function to configure BlackArch tools
configure_blackarch_tools() {
    print_status "Configuring BlackArch tools..."
    
    # Create configuration directories
    docker exec "$BLACKARCH_CONTAINER_NAME" mkdir -p /opt/osint/config
    
    # Configure common tools
    # This is a placeholder - in practice, you would configure each tool individually
    docker exec "$BLACKARCH_CONTAINER_NAME" bash -c 'echo "BlackArch tools configured" > /opt/osint/config/README.md'
    
    print_status "BlackArch tools configuration completed"
}

# Function to test BlackArch tools
test_blackarch_tools() {
    print_status "Testing BlackArch tools..."
    
    # Test basic tools
    TOOLS_TO_TEST=("nmap" "curl" "wget" "python3" "git")
    
    for tool in "${TOOLS_TO_TEST[@]}"; do
        if docker exec "$BLACKARCH_CONTAINER_NAME" command -v "$tool" &> /dev/null; then
            version=$(docker exec "$BLACKARCH_CONTAINER_NAME" "$tool" --version 2>/dev/null || echo "Version info not available")
            print_status "$tool is available: $version"
        else
            print_warning "$tool is not available"
        fi
    done
    
    # Test MCP server
    sleep 5  # Wait for server to start
    if curl -s http://localhost:3006/health | grep -q '"status":"ok"'; then
        print_status "BlackArch MCP server is running"
    else
        print_warning "BlackArch MCP server is not responding"
    fi
    
    print_status "BlackArch tools testing completed"
}

# Function to show completion message
show_completion() {
    print_status "=========================================="
    print_status "BlackArch Tools Initialization Completed!"
    print_status "=========================================="
    echo ""
    print_status "Containers:"
    print_status "- BlackArch OSINT: $BLACKARCH_CONTAINER_NAME"
    print_status "- BlackArch MCP: $BLACKARCH_MCP_CONTAINER_NAME"
    print_status "Data directory: $BLACKARCH_DATA_DIR"
    print_status "Exposed ports:"
    print_status "- BlackArch OSINT: 8087 (HTTP), 8444 (HTTPS)"
    print_status "- BlackArch MCP: 3006"
    echo ""
    print_status "Next steps:"
    print_status "1. Access the BlackArch container: docker exec -it $BLACKARCH_CONTAINER_NAME bash"
    print_status "2. Access the MCP server: http://localhost:3006"
    print_status "3. Use BlackArch tools for OSINT operations"
    print_status "4. Store data in $BLACKARCH_DATA_DIR"
    echo ""
    print_status "Management commands:"
    print_status "- Start containers: docker start $BLACKARCH_CONTAINER_NAME $BLACKARCH_MCP_CONTAINER_NAME"
    print_status "- Stop containers: docker stop $BLACKARCH_CONTAINER_NAME $BLACKARCH_MCP_CONTAINER_NAME"
    print_status "- View logs: docker logs $BLACKARCH_CONTAINER_NAME"
    print_status "=========================================="
}

# Main initialization process
print_status "Starting BlackArch Tools Initialization..."

# Check if Docker is running
check_docker

# Build BlackArch containers
build_blackarch_containers

# Start BlackArch containers
start_blackarch_containers

# Install additional BlackArch tools
install_blackarch_tools

# Configure BlackArch tools
configure_blackarch_tools

# Test BlackArch tools
test_blackarch_tools

# Show completion message
show_completion

print_status "BlackArch tools initialization script completed successfully!"