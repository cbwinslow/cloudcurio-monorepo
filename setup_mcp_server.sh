#!/bin/bash

# CloudCurio MCP Server Setup Script

set -e  # Exit on any error

echo "Setting up CloudCurio MCP Server..."

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

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "pip is not installed. Installing pip..."
    python3 -m ensurepip --upgrade
fi

# Install uv if not available
if ! command -v uv &> /dev/null; then
    echo "Installing uv package manager..."
    pip install uv
fi

# Create a virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install required packages
echo "Installing required packages..."
pip install -r crew/mcp_server/requirements.txt

# Check if .env file exists, if not create a template
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env || echo "Could not find .env.example, please create .env file with required environment variables"
fi

echo "Setup complete! To start the server, run:"
echo "  source venv/bin/activate"
echo "  python crew/mcp_server/start_server.py"