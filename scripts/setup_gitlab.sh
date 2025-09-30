#!/bin/bash

# CloudCurio GitLab Setup Script

set -e  # Exit on any error

echo "Setting up CloudCurio on GitLab..."

# Check if git remote for GitLab already exists
if git remote get-url gitlab >/dev/null 2>&1; then
    echo "GitLab remote already exists"
else
    # Get GitLab repository URL from user
    read -p "Enter GitLab repository URL (e.g., https://gitlab.com/username/cloudcurio.git): " GITLAB_URL
    
    # Add GitLab as a remote
    git remote add gitlab "$GITLAB_URL"
    echo "Added GitLab remote: $GITLAB_URL"
fi

# Push all branches and tags to GitLab
echo "Pushing to GitLab..."
git push gitlab master
git push gitlab --tags

echo "Successfully pushed CloudCurio to GitLab!"
echo ""
echo "Your repository is now available on GitLab with:"
echo "- All source code"
echo "- Complete commit history" 
echo "- Version tags (including v2.0.0)"
echo "- CI/CD configurations for GitLab"
echo ""
echo "GitLab repository: $GITLAB_URL"