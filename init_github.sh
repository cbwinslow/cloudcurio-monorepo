#!/bin/bash

# GitHub Repository Initialization Script for CloudCurio

set -e  # Exit on any error

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Git is not installed. Please install Git first."
    exit 1
fi

# Check if we're in the CloudCurio project directory
if [ ! -f "README.md" ] || [ ! -d "crew" ] || [ ! -d "ai_tools" ]; then
    echo "This script must be run from the CloudCurio project root directory."
    exit 1
fi

# Get repository information from user
echo "Setting up CloudCurio GitHub repository..."
echo "Please enter your GitHub repository details:"
read -p "Repository name (default: cloudcurio): " REPO_NAME
REPO_NAME=${REPO_NAME:-cloudcurio}

read -p "Repository description: " REPO_DESC

# Initialize git repository if not already initialized
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
else
    echo "Git repository already exists."
fi

# Ensure we have the latest changes staged
echo "Staging all files..."
git add .

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo "No changes to commit. Repository is up to date."
else
    # Create initial commit
    echo "Creating initial commit..."
    git commit -m "Initial commit: CloudCurio AI-Powered Development Platform
    
CloudCurio is an AI-powered platform designed to automate code review, 
documentation generation, and vulnerability assessment for software projects. 
The system leverages CrewAI to orchestrate teams of AI agents that can 
analyze codebases, generate documentation, and identify security vulnerabilities.

Features:
- Automated code review with AI agents
- Documentation generation from codebase analysis  
- Vulnerability assessment and security scanning
- REST API for crew management
- Support for multiple AI providers (OpenRouter, OpenAI, Google Gemini, Ollama, 
  LocalAI, Qwen, Groq, Grok, LM Studio, SambaNova, DeepInfra, Models.dev, LiteLLM)
- Secure credential storage using GPG encryption
- Portable configuration system with persistent agent configurations
- System monitoring tool (SysMon) for tracking changes
- Web-based configuration editor with AI-powered action recording
- Terminal tools integration (Tabby)
- Web interface integration (Open WebUI)
"
fi

# Add the remote origin
read -p "GitHub repository URL (e.g., https://github.com/username/cloudcurio.git or git@github.com:username/cloudcurio.git): " REPO_URL

echo "Adding remote origin: $REPO_URL"
git remote add origin "$REPO_URL"

# Push to GitHub (create the repo if needed)
echo "Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "==========================================="
echo "GitHub repository setup complete!"
echo "==========================================="
echo ""
echo "Repository: $REPO_URL"
echo "Branch: main"
echo ""
echo "Your CloudCurio project is now on GitHub!"
echo ""
echo "Next steps:"
echo "1. Visit your repository at: $REPO_URL"
echo "2. Set up any additional branches as needed"
echo "3. Configure GitHub Actions for CI/CD if desired"
echo "4. Add collaborators as needed"
echo ""
echo "The repository includes:"
echo "- AI-powered code review and documentation generation"
echo "- Multiple AI provider support"
echo "- Secure credential management"
echo "- System monitoring and configuration tracking"
echo "- Web-based configuration editor with action recording"
echo "- Terminal and web interface integrations"
echo ""