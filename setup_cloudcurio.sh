#!/bin/bash

# CloudCurio Main Setup Script
# This script sets up the complete CloudCurio development environment

set -e  # Exit on any error

echo "==========================================="
echo "CloudCurio Complete Setup"
echo "==========================================="

# Function to ask for user confirmation
confirm() {
    read -r -p "$1 [y/N] " response
    case "$response" in
        [yY][eE][sS]|[yY]) 
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

# Function to install dependencies
install_dependencies() {
    echo "Installing system dependencies..."
    
    if command -v apt-get &> /dev/null; then
        # Ubuntu/Debian
        sudo apt-get update
        sudo apt-get install -y curl wget gnupg
    elif command -v brew &> /dev/null; then
        # macOS with Homebrew
        brew install curl wget gnupg
    else
        echo "Please install curl, wget, and gnupg manually"
    fi
}

# Function to setup Python environment
setup_python() {
    echo "Setting up Python environment..."
    
    # Check if Python 3.10+ is available
    if ! command -v python3 &> /dev/null; then
        echo "Python3 is not installed. Please install Python 3.10 or higher."
        exit 1
    fi

    PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    if [[ "$PYTHON_VERSION" < "3.10" ]]; then
        echo "Python version $PYTHON_VERSION is too old. Please use Python 3.10 or higher."
        exit 1
    fi

    # Create a virtual environment
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate

    # Upgrade pip
    pip install --upgrade pip

    # Install required packages
    echo "Installing required packages..."
    pip install -r crew/requirements.txt
}

# Function to setup MCP server
setup_mcp_server() {
    echo "Setting up MCP Server..."
    
    # Create .env file if it doesn't exist
    if [ ! -f .env ]; then
        cp .env.example .env
        echo "Created .env file from example. Please update with your API keys."
    fi
    
    echo "MCP Server setup complete!"
}

# Function to setup Tabby terminal
setup_tabby() {
    echo "Setting up Tabby terminal..."
    ./setup_tabby.sh
    echo "Tabby terminal setup complete!"
}

# Function to setup Open WebUI
setup_open_webui() {
    echo "Setting up Open WebUI..."
    ./setup_open_webui.sh
    echo "Open WebUI setup complete!"
}

# Function to setup AI credentials
setup_credentials() {
    echo "Setting up AI credentials..."
    echo "Please configure your AI provider credentials using the CLI:"
    echo ""
    echo "1. Setup configuration directory:"
    echo "   python -m ai_tools.cli setup"
    echo ""
    echo "2. Add API keys for providers you want to use:"
    echo "   python -m ai_tools.cli add-credential openai"
    echo "   python -m ai_tools.cli add-credential gemini"
    echo "   python -m ai_tools.cli add-credential openrouter"
    echo "   # ... etc for other providers"
    echo ""
    echo "3. Set default provider:"
    echo "   python -m ai_tools.cli set-default openrouter"
    echo ""
}

# Main execution
echo "This script will set up the complete CloudCurio environment."
echo ""

if confirm "Do you want to install system dependencies?"; then
    install_dependencies
fi

if confirm "Do you want to set up the Python environment?"; then
    setup_python
fi

if confirm "Do you want to set up the MCP server?"; then
    setup_mcp_server
fi

if confirm "Do you want to set up Tabby terminal?"; then
    setup_tabby
fi

if confirm "Do you want to set up Open WebUI?"; then
    setup_open_webui
fi

if confirm "Do you want to see instructions for setting up AI credentials?"; then
    setup_credentials
fi

echo ""
echo "==========================================="
echo "CloudCurio setup complete!"
echo "==========================================="
echo ""
echo "Next steps:"
echo "1. Start the MCP server: python crew/mcp_server/start_server.py"
echo "2. Or use Docker: docker build -f Dockerfile.mcp -t cloudcurio-mcp . && docker run -p 8000:8000 cloudcurio-mcp"
echo "3. Access the API at http://localhost:8000"
echo "4. Launch Tabby terminal: cloudcurio-terminal"
echo "5. Start Open WebUI: ./start_open_webui.sh"
echo ""