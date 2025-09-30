#!/bin/bash

# CloudCurio Configuration Editor Setup Script

set -e  # Exit on any error

echo "Setting up CloudCurio Configuration Editor..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r config_editor/requirements.txt

# Create necessary directories
mkdir -p ~/.cloudcurio/config_editor

echo "Configuration Editor setup complete!"

echo ""
echo "To start the Configuration Editor:"
echo "  python config_editor/launcher.py"
echo ""
echo "The web interface will be available at http://localhost:8081"