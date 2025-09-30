#!/bin/bash

# CloudCurio Complete Setup Script

set -e  # Exit on any error

echo "==========================================="
echo "CloudCurio - Complete AI Development Platform"
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

# Function to install Python dependencies
install_python_deps() {
    echo "Installing Python dependencies..."
    
    # Check if pip is available
    if ! command -v pip &> /dev/null; then
        echo "Installing pip..."
        python3 -m ensurepip --upgrade
    fi
    
    # Install core dependencies
    echo "Installing core dependencies..."
    pip install -r crew/requirements.txt
    
    # Install configuration editor dependencies
    echo "Installing configuration editor dependencies..."
    pip install -r config_editor/requirements.txt
    
    echo "Python dependencies installed!"
}

# Function to setup the complete environment
setup_complete() {
    echo "Setting up complete CloudCurio environment..."
    
    # Setup MCP server
    echo "Setting up MCP server..."
    if [ ! -f .env ]; then
        cp .env.example .env
        echo "Created .env file. Please update with your API keys."
    fi
    
    # Setup system monitoring
    echo "Setting up system monitoring..."
    ./setup_sysmon.sh
    
    # Setup configuration editor
    echo "Setting up configuration editor..."
    ./setup_config_editor.sh
    
    # Setup Tabby terminal
    echo "Setting up Tabby terminal..."
    ./setup_tabby.sh
    
    # Setup Open WebUI
    echo "Setting up Open WebUI..."
    ./setup_open_webui.sh
    
    # Setup main environment
    echo "Running main setup..."
    ./setup_cloudcurio.sh
    
    echo "Complete environment setup finished!"
}

# Function to show usage instructions
show_usage() {
    echo ""
    echo "CloudCurio Usage Instructions:"
    echo ""
    echo "1. MCP Server (AI Crew Management):"
    echo "   python crew/mcp_server/start_server.py"
    echo "   API will be available at http://localhost:8000"
    echo ""
    echo "2. Configuration Editor (Web Interface):"
    echo "   python config_editor/launcher.py"
    echo "   Web interface will be available at http://localhost:8081"
    echo ""
    echo "3. System Monitoring:"
    echo "   cloudcurio-sysmon setup                    # Initial setup"
    echo "   cloudcurio-sysmon snapshot                 # Create snapshot"
    echo "   cloudcurio-sysmon events                   # View events"
    echo "   cloudcurio-sysmon monitor --continuous     # Continuous monitoring"
    echo ""
    echo "4. Tabby Terminal:"
    echo "   cloudcurio-terminal                        # Launch with CloudCurio config"
    echo ""
    echo "5. Open WebUI:"
    echo "   ./start_open_webui.sh                      # Start services"
    echo "   Access at http://localhost:3000"
    echo ""
    echo "6. AI Provider Configuration:"
    echo "   python -m ai_tools.cli setup"
    echo "   python -m ai_tools.cli add-credential openai"
    echo "   python -m ai_tools.cli set-default openrouter"
    echo ""
    echo "For more details, check the README.md file."
}

# Main execution
echo "This script will set up the complete CloudCurio environment."
echo ""

if confirm "Do you want to install Python dependencies?"; then
    install_python_deps
fi

if confirm "Do you want to set up the complete environment?"; then
    setup_complete
fi

if confirm "Do you want to see usage instructions?"; then
    show_usage
fi

echo ""
echo "==========================================="
echo "CloudCurio Complete Setup Finished!"
echo "==========================================="
echo ""
echo "To get started, run: ./init_github.sh"
echo "This will initialize your GitHub repository for the project."
echo ""