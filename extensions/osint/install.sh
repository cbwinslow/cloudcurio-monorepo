#!/bin/bash

# OSINT Extension Installation Script for BeEF
# This script installs all dependencies and sets up the OSINT extension

set -e  # Exit on any error

echo "Installing OSINT Extension for BeEF..."

# Check if we're in the BeEF root directory
if [ ! -f "beef" ]; then
    echo "Error: This script must be run from the BeEF root directory"
    exit 1
fi

echo "Checking system requirements..."

# Check for Ruby
if ! command -v ruby &> /dev/null; then
    echo "Error: Ruby is not installed"
    exit 1
fi

# Check for Node.js
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed"
    exit 1
fi

echo "Installing Ruby gems..."

# Install required Ruby gems
gem install neo4j-core
gem install crew
gem install langchain

echo "Installing Python dependencies..."

# Install required Python packages for CrewAI
pip install crewai
pip install langchain
pip install neo4j

echo "Setting up Neo4j database..."

# Check if Neo4j is installed
if ! command -v neo4j &> /dev/null; then
    echo "Neo4j is not installed. Please install Neo4j manually:"
    echo "  - Ubuntu/Debian: apt-get install neo4j"
    echo "  - CentOS/RHEL: yum install neo4j"
    echo "  - macOS: brew install neo4j"
    echo "  - Or download from https://neo4j.com/download/"
else
    echo "Neo4j is already installed"
fi

echo "Setting up Ollama..."

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "Ollama is not installed. Please install Ollama manually:"
    echo "  - Visit https://ollama.com/download for installation instructions"
else
    echo "Ollama is already installed"
    echo "Pulling required Dolphin models..."
    ollama pull dolphin-llama3
    ollama pull dolphin-mistral
fi

echo "Creating reports directory..."

# Create reports directory
mkdir -p extensions/osint/reports/saved

echo "Initializing Neo4j schema..."

# This would run the Neo4j schema setup
# For now, we'll just create a placeholder
echo "Neo4j schema initialization would be performed here"

echo "Installation complete!"

echo "
Next steps:
1. Start Neo4j database (if not already running)
2. Start Ollama service (if not already running)
3. Configure the extension in extensions/osint/config.yaml
4. Start BeEF: ./beef
"