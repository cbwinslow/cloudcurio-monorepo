#!/bin/bash

# GitLab Integration Script for OSINT Platform

# Configuration
GITLAB_URL="https://gitlab.com"
GITLAB_API_VERSION="v4"
GITLAB_PERSONAL_ACCESS_TOKEN=""
GITLAB_PROJECT_NAME="osint-platform"
GITLAB_USERNAME=""

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

# Function to load configuration
load_config() {
    if [ -f "deployment/config/gitlab.yml" ]; then
        # In a real implementation, we would parse the YAML file
        # For now, we'll just check if it exists
        print_status "GitLab configuration file found"
    else
        print_warning "GitLab configuration file not found"
    fi
}

# Function to validate GitLab credentials
validate_credentials() {
    print_status "Validating GitLab credentials..."
    
    if [ -z "$GITLAB_PERSONAL_ACCESS_TOKEN" ] || [ -z "$GITLAB_USERNAME" ]; then
        print_error "GitLab credentials not set"
        print_error "Please set GITLAB_PERSONAL_ACCESS_TOKEN and GITLAB_USERNAME environment variables"
        exit 1
    fi
    
    # Test API access
    response=$(curl -s -X GET "$GITLAB_URL/api/$GITLAB_API_VERSION/user" \
        -H "Authorization: Bearer $GITLAB_PERSONAL_ACCESS_TOKEN" \
        -H "Content-Type: application/json")
    
    if echo "$response" | grep -q '"username":"'"$GITLAB_USERNAME"'"'; then
        print_status "GitLab API credentials validated successfully"
    else
        print_error "Failed to validate GitLab API credentials"
        exit 1
    fi
}

# Function to create GitLab project
create_project() {
    print_status "Creating GitLab project..."
    
    response=$(curl -s -X POST "$GITLAB_URL/api/$GITLAB_API_VERSION/projects" \
        -H "Authorization: Bearer $GITLAB_PERSONAL_ACCESS_TOKEN" \
        -H "Content-Type: application/json" \
        --data '{
            "name":"'"$GITLAB_PROJECT_NAME"'",
            "description":"OSINT Platform - Comprehensive OSINT toolkit",
            "visibility":"private",
            "initialize_with_readme":true
        }')
    
    if echo "$response" | grep -q '"name":"'"$GITLAB_PROJECT_NAME"'"'; then
        project_id=$(echo "$response" | jq -r '.id')
        print_status "Created GitLab project: $GITLAB_PROJECT_NAME (ID: $project_id)"
    else
        print_warning "Failed to create GitLab project or project already exists"
        # Try to get existing project ID
        response=$(curl -s -X GET "$GITLAB_URL/api/$GITLAB_API_VERSION/projects?search=$GITLAB_PROJECT_NAME" \
            -H "Authorization: Bearer $GITLAB_PERSONAL_ACCESS_TOKEN" \
            -H "Content-Type: application/json")
        
        if echo "$response" | grep -q '"name":"'"$GITLAB_PROJECT_NAME"'"'; then
            project_id=$(echo "$response" | jq -r '.[0].id')
            print_status "Found existing GitLab project: $GITLAB_PROJECT_NAME (ID: $project_id)"
        else
            print_error "Could not find or create GitLab project"
            exit 1
        fi
    fi
}

# Function to create labels
create_labels() {
    print_status "Creating GitLab labels..."
    
    labels=("bug:#e11d21" "enhancement:#84b6eb" "documentation:#c2e0c6" "security:#e11d21" "osint:#5319e7" "plugin:#fbca04" "ai:#5319e7")
    
    for label in "${labels[@]}"; do
        name=$(echo "$label" | cut -d':' -f1)
        color=$(echo "$label" | cut -d':' -f2)
        
        response=$(curl -s -X POST "$GITLAB_URL/api/$GITLAB_API_VERSION/projects/$project_id/labels" \
            -H "Authorization: Bearer $GITLAB_PERSONAL_ACCESS_TOKEN" \
            -H "Content-Type: application/json" \
            --data '{
                "name":"'"$name"'",
                "color":"'"$color"'"
            }')
        
        if echo "$response" | grep -q '"name":"'"$name"'"'; then
            print_status "Created label: $name"
        else
            print_warning "Failed to create label: $name (may already exist)"
        fi
    done
}

# Function to create issue templates
create_issue_templates() {
    print_status "Creating issue templates..."
    
    # Create .gitlab directory if it doesn't exist
    mkdir -p .gitlab/issue_templates
    
    # Bug template
    cat > .gitlab/issue_templates/Bug.md << 'EOF'
## Description
Brief description of the bug

## Steps to Reproduce
1. 
2. 
3. 

## Expected Behavior
What you expected to happen

## Actual Behavior
What actually happened

## Screenshots
If applicable, add screenshots to help explain your problem

## Environment
- OS: [e.g. Ubuntu 20.04]
- Browser: [e.g. Chrome, Safari]
- Version: [e.g. 1.0.0]

## Additional Context
Add any other context about the problem here
EOF

    # Feature template
    cat > .gitlab/issue_templates/Feature.md << 'EOF'
## Description
Brief description of the feature

## Use Case
What problem does this solve?

## Proposed Solution
How should this be implemented?

## Alternatives Considered
Any alternative solutions or features you've considered

## Additional Context
Add any other context or screenshots about the feature request here
EOF

    print_status "Created issue templates"
}

# Function to create merge request templates
create_mr_templates() {
    print_status "Creating merge request templates..."
    
    # Create .gitlab directory if it doesn't exist
    mkdir -p .gitlab/merge_request_templates
    
    # Feature template
    cat > .gitlab/merge_request_templates/Feature.md << 'EOF'
## Description
Brief description of the feature

## Changes
- List of changes

## Testing
How was this tested?

## Related Issues
Fixes #issue-number
EOF

    # Bugfix template
    cat > .gitlab/merge_request_templates/Bugfix.md << 'EOF'
## Description
Brief description of the bug

## Root Cause
Explanation of what caused the bug

## Solution
Explanation of how the bug was fixed

## Testing
How was this tested?

## Related Issues
Fixes #issue-number
EOF

    print_status "Created merge request templates"
}

# Function to configure CI/CD
configure_ci_cd() {
    print_status "Configuring CI/CD..."
    
    # Create .gitlab-ci.yml
    cat > .gitlab-ci.yml << 'EOF'
stages:
  - build
  - test
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"

before_script:
  - docker info

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - echo "Building OSINT Platform..."
    - docker-compose build
  artifacts:
    paths:
      - docker-compose.yml
      - deployment/
  only:
    - main
    - merge_requests

test:
  stage: test
  image: python:3.11
  script:
    - echo "Running tests..."
    - pip install -r ai-agents/requirements.txt
    - python -m pytest ai-agents/tests/
  dependencies:
    - build
  only:
    - main
    - merge_requests

deploy:
  stage: deploy
  image: docker:latest
  services:
    - docker:dind
  script:
    - echo "Deploying OSINT Platform..."
    - docker-compose up -d
  environment:
    name: production
  only:
    - main
  when: manual
EOF

    print_status "Created .gitlab-ci.yml"
}

# Function to push to GitLab
push_to_gitlab() {
    print_status "Pushing to GitLab..."
    
    # Initialize git repository if not already done
    if [ ! -d ".git" ]; then
        git init
        git add .
        git commit -m "Initial commit: OSINT Platform"
    fi
    
    # Add GitLab remote
    git remote add gitlab "$GITLAB_URL/$GITLAB_USERNAME/$GITLAB_PROJECT_NAME.git" 2>/dev/null || true
    
    # Push to GitLab
    git push -u gitlab main 2>/dev/null || {
        print_warning "Failed to push to GitLab. Please check your credentials and network connection."
    }
    
    print_status "Pushed to GitLab"
}

# Function to show completion message
show_completion() {
    print_status "=========================================="
    print_status "GitLab Integration Completed!"
    print_status "=========================================="
    echo ""
    print_status "Project URL: $GITLAB_URL/$GITLAB_USERNAME/$GITLAB_PROJECT_NAME"
    print_status "Next steps:"
    print_status "1. Verify project in GitLab dashboard"
    print_status "2. Configure CI/CD runners if needed"
    print_status "3. Set up webhooks for integration"
    print_status "4. Review labels and templates"
    echo ""
    print_status "Management commands:"
    print_status "- Re-run this script to update configuration"
    print_status "- Check GitLab project for status"
    print_status "=========================================="
}

# Main integration process
print_status "Starting GitLab Integration..."

# Load configuration
load_config

# Validate credentials
validate_credentials

# Create GitLab project
create_project

# Create labels
create_labels

# Create issue templates
create_issue_templates

# Create merge request templates
create_mr_templates

# Configure CI/CD
configure_ci_cd

# Push to GitLab
push_to_gitlab

# Show completion message
show_completion

print_status "GitLab integration script completed successfully!"