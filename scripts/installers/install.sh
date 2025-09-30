#!/bin/bash

# CloudCurio Platform Installer
# Comprehensive installation script for CloudCurio platform

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}    CloudCurio Installer        ${NC}"
    echo -e "${BLUE}================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Function to detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    else
        print_error "Unsupported OS: $OSTYPE"
        exit 1
    fi
    print_info "Detected OS: $OS"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install Python 3.10+
install_python() {
    print_info "Checking Python version..."
    
    if command_exists python3; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
        if [[ "$PYTHON_VERSION" < "3.10" ]]; then
            print_warning "Python version $PYTHON_VERSION is too old. Installing Python 3.10+..."
            if [[ "$OS" == "linux" ]]; then
                # For Ubuntu/Debian
                if command_exists apt-get; then
                    sudo apt-get update
                    sudo apt-get install -y python3.10 python3.10-venv python3.10-dev python3-pip
                # For CentOS/RHEL/Fedora
                elif command_exists dnf; then
                    sudo dnf install -y python3.10 python3.10-pip
                elif command_exists yum; then
                    sudo yum install -y python3.10 python3.10-pip
                fi
            elif [[ "$OS" == "macos" ]]; then
                if command_exists brew; then
                    brew install python@3.10
                else
                    print_error "Homebrew is required to install Python on macOS. Please install it first."
                    exit 1
                fi
            fi
        else
            print_success "Python version $PYTHON_VERSION is sufficient"
        fi
    else
        print_error "Python 3 is not installed. Please install Python 3.10+ manually."
        exit 1
    fi
}

# Function to install Docker
install_docker() {
    print_info "Checking Docker installation..."
    
    if ! command_exists docker; then
        print_warning "Docker is not installed. Installing Docker..."
        
        if [[ "$OS" == "linux" ]]; then
            # Install Docker using convenience script
            curl -fsSL https://get.docker.com -o get-docker.sh
            sh get-docker.sh
            sudo usermod -aG docker $USER
            print_info "Docker installed. You may need to log out and back in for group changes to take effect."
        elif [[ "$OS" == "macos" ]]; then
            if command_exists brew; then
                brew install --cask docker
                print_info "Please start Docker Desktop manually after installation."
            else
                print_error "Docker installation requires Homebrew on macOS."
                exit 1
            fi
        fi
    else
        print_success "Docker is already installed"
    fi
}

# Function to install system dependencies
install_dependencies() {
    print_info "Installing system dependencies..."
    
    if [[ "$OS" == "linux" ]]; then
        if command_exists apt-get; then
            sudo apt-get update
            sudo apt-get install -y curl wget git build-essential libssl-dev libffi-dev python3-dev
        elif command_exists dnf; then
            sudo dnf install -y curl wget git gcc openssl-devel libffi-devel python3-devel
        elif command_exists yum; then
            sudo yum install -y curl wget git gcc openssl-devel libffi-devel python3-devel
        fi
    elif [[ "$OS" == "macos" ]]; then
        xcode-select --install 2>/dev/null || true
        if command_exists brew; then
            brew install curl wget git
        fi
    fi
    
    print_success "System dependencies installed"
}

# Function to create project directory structure
create_structure() {
    print_info "Creating CloudCurio directory structure..."
    
    # Create main directory if it doesn't exist
    if [ ! -d "$INSTALL_DIR" ]; then
        mkdir -p "$INSTALL_DIR"
    fi
    
    # Create subdirectories
    mkdir -p "$INSTALL_DIR/{bin,config,data,logs,backups}"
    
    print_success "Directory structure created at $INSTALL_DIR"
}

# Function to install CloudCurio via pip
install_cloudcurio_pip() {
    print_info "Installing CloudCurio using pip..."
    
    # Create virtual environment
    python3 -m venv "$INSTALL_DIR/venv"
    source "$INSTALL_DIR/venv/bin/activate"
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install CloudCurio
    pip install cloudcurio
    
    print_success "CloudCurio installed via pip"
}

# Function to install CloudCurio from source
install_cloudcurio_source() {
    print_info "Installing CloudCurio from source..."
    
    CDIR=$(pwd)
    
    # Clone the repository if not already present
    if [ ! -d "$INSTALL_DIR/source" ]; then
        git clone https://github.com/cbwinslow/cloudcurio.git "$INSTALL_DIR/source"
    else
        cd "$INSTALL_DIR/source"
        git pull origin main
    fi
    
    # Create virtual environment
    python3 -m venv "$INSTALL_DIR/venv"
    source "$INSTALL_DIR/venv/bin/activate"
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install from source
    cd "$INSTALL_DIR/source"
    pip install -r crew/requirements.txt
    pip install -r config_editor/requirements.txt
    pip install -e .
    
    # Create symlinks for executables
    mkdir -p "$INSTALL_DIR/bin"
    ln -sf "$INSTALL_DIR/source/cloudcurio" "$INSTALL_DIR/bin/cloudcurio"
    ln -sf "$INSTALL_DIR/source/cloudcurio-sysmon" "$INSTALL_DIR/bin/cloudcurio-sysmon"
    
    cd $CDIR
    
    print_success "CloudCurio installed from source"
}

# Function to install systemd services (Linux only)
install_systemd_services() {
    if [[ "$OS" == "linux" ]]; then
        print_info "Installing systemd services..."
        
        # Create systemd user directory if it doesn't exist
        mkdir -p ~/.config/systemd/user
        
        # Copy service files
        cp "$INSTALL_DIR/source/sysmon/cloudcurio-sysmon.service" ~/.config/systemd/user/
        
        # Reload systemd
        systemctl --user daemon-reload
        
        print_success "Systemd services installed"
    fi
}

# Function to install and configure Ollama (for local AI)
install_local_ai() {
    if [ "$INSTALL_LOCAL_AI" = true ]; then
        print_info "Installing Ollama for local AI models..."
        
        if ! command_exists ollama; then
            # Install Ollama
            curl -fsSL https://ollama.ai/install.sh | sh
            print_success "Ollama installed"
            
            # Start Ollama service
            if [[ "$OS" == "linux" ]]; then
                sudo systemctl start ollama
                sudo systemctl enable ollama
            elif [[ "$OS" == "macos" ]]; then
                # Ollama should start automatically on macOS after installation
                print_info "Please start Ollama service manually if needed"
            fi
        else
            print_success "Ollama is already installed"
        fi
        
        # Pull a default model
        print_info "Pulling default model (llama3)..."
        ollama pull llama3 || print_warning "Failed to pull llama3 model, but continuing..."
    fi
}

# Function to create configuration files
create_configs() {
    print_info "Creating configuration files..."
    
    CONFIG_DIR="$INSTALL_DIR/config"
    
    # Create default config file if it doesn't exist
    if [ ! -f "$CONFIG_DIR/cloudcurio.conf" ]; then
        mkdir -p "$CONFIG_DIR"
        cat > "$CONFIG_DIR/cloudcurio.conf" << EOF
# CloudCurio Configuration File

# MCP Server settings
MCP_HOST=0.0.0.0
MCP_PORT=8000
MCP_DEBUG=False

# Database settings
DATABASE_URL=sqlite:///./cloudcurio.db

# Default AI provider
DEFAULT_AI_PROVIDER=openrouter

# Logging settings
LOG_LEVEL=INFO
LOG_FILE=$INSTALL_DIR/logs/cloudcurio.log

# SysMon settings
SYSMON_ENABLED=True
SNAPSHOT_INTERVAL=3600
EOF
        print_success "Configuration file created at $CONFIG_DIR/cloudcurio.conf"
    else
        print_info "Configuration file already exists"
    fi
}

# Function to display completion message
display_completion_message() {
    print_success "CloudCurio installation completed successfully!"
    echo ""
    echo "Installation directory: $INSTALL_DIR"
    echo ""
    echo "Next steps:"
    echo "1. Add to PATH: export PATH=\"\$PATH:$INSTALL_DIR/bin\""
    echo "2. Set configuration: Edit $INSTALL_DIR/config/cloudcurio.conf"
    echo "3. Start services: cloudcurio-mcp, cloudcurio-sysmon, etc."
    echo ""
    echo "For local AI, make sure Ollama is running: ollama serve"
    echo ""
    echo "For more information, visit: https://github.com/cbwinslow/cloudcurio"
    echo ""
}

# Main execution
main() {
    print_header
    
    # Parse command line arguments
    INSTALL_DIR="$HOME/.cloudcurio"
    INSTALL_SOURCE=false
    INSTALL_LOCAL_AI=false
    SKIP_DOCKER=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --install-dir)
                INSTALL_DIR="$2"
                shift 2
                ;;
            --install-source)
                INSTALL_SOURCE=true
                shift
                ;;
            --install-local-ai)
                INSTALL_LOCAL_AI=true
                shift
                ;;
            --skip-docker)
                SKIP_DOCKER=true
                shift
                ;;
            --help)
                echo "CloudCurio Installer"
                echo ""
                echo "Usage: $0 [OPTIONS]"
                echo ""
                echo "Options:"
                echo "  --install-dir DIR     Set installation directory (default: ~/.cloudcurio)"
                echo "  --install-source      Install from source instead of pip"
                echo "  --install-local-ai    Install Ollama for local AI models"
                echo "  --skip-docker         Skip Docker installation"
                echo "  --help               Show this help message"
                echo ""
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    print_info "Installation directory: $INSTALL_DIR"
    print_info "Install from source: $INSTALL_SOURCE"
    print_info "Install local AI: $INSTALL_LOCAL_AI"
    print_info "Skip Docker: $SKIP_DOCKER"
    
    # Detect OS
    detect_os
    
    # Install dependencies
    install_dependencies
    
    # Install Python if needed
    install_python
    
    # Install Docker if needed
    if [ "$SKIP_DOCKER" = false ]; then
        install_docker
    fi
    
    # Create directory structure
    create_structure
    
    # Install CloudCurio
    if [ "$INSTALL_SOURCE" = true ]; then
        install_cloudcurio_source
    else
        install_cloudcurio_pip
    fi
    
    # Install local AI if requested
    install_local_ai
    
    # Create configuration files
    create_configs
    
    # Install systemd services (Linux only)
    install_systemd_services
    
    # Display completion message
    display_completion_message
}

# Run main function with all arguments
main "$@"