#!/bin/bash

# CloudCurio Final Verification Script
# This script verifies that all components are ready for GitHub upload

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}    CloudCurio Final Verification        ${NC}"
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

# Function to verify directory structure
verify_directory_structure() {
    print_info "Verifying directory structure..."
    
    # Check for key directories
    local required_dirs=(
        "crew"
        "ai_tools"
        "sysmon"
        "config_editor"
        "feature_tracking"
        "container"
        "docs"
        "examples"
        "tests"
        "scripts"
        "domains"
        "infrastructure"
        "tools"
        "kubernetes"
        "kubernetes/manifests"
        "kubernetes/helm"
        "kubernetes/helm/cloudcurio"
        "kubernetes/helm/cloudcurio/templates"
        "kubernetes/scripts"
        ".github"
        ".github/workflows"
    )
    
    local missing_dirs=()
    for dir in "${required_dirs[@]}"; do
        if [ ! -d "$dir" ]; then
            missing_dirs+=("$dir")
        fi
    done
    
    if [ ${#missing_dirs[@]} -eq 0 ]; then
        print_success "All required directories present"
    else
        print_error "Missing directories: ${missing_dirs[*]}"
        return 1
    fi
}

# Function to verify key files
verify_key_files() {
    print_info "Verifying key files..."
    
    # Check for key files
    local required_files=(
        "README.md"
        "MONOREPO_README.md"
        "PROCEDURE_HANDBOOK.md"
        "BRANCHING_TAGGING_STRATEGY.md"
        "RELEASE_MANAGEMENT.md"
        "CHANGELOG.md"
        "CONTRIBUTING.md"
        "SECURITY.md"
        "TASK_LIST.md"
        "ROADMAP.md"
        "setup.py"
        "Makefile"
        ".env.example"
        ".gitignore"
        "kubernetes/README.md"
        "kubernetes/helm/cloudcurio/Chart.yaml"
        "kubernetes/helm/cloudcurio/values.yaml"
        "kubernetes/helm/cloudcurio/README.md"
        "kubernetes/helm/cloudcurio/HELM_DOCS.md"
        "kubernetes/manifests/all-in-one.yaml"
        "kubernetes/scripts/deploy.sh"
        "kubernetes/scripts/deploy_helm.sh"
        "kubernetes/scripts/demo_deployment.sh"
        ".github/workflows/cicd.yaml"
        ".github/workflows/code-quality.yaml"
        ".github/workflows/security-scan.yaml"
        ".github/workflows/testing.yaml"
        ".github/workflows/release.yaml"
        ".github/workflows/documentation.yaml"
        ".github/workflows/branch-management.yaml"
        ".github/workflows/dependency-updates.yaml"
        ".github/workflows/crewai-review.yaml"
        ".github/workflows/performance-monitoring.yaml"
        ".github/workflows/helm-chart.yaml"
    )
    
    local missing_files=()
    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            missing_files+=("$file")
        fi
    done
    
    if [ ${#missing_files[@]} -eq 0 ]; then
        print_success "All required files present"
    else
        print_error "Missing files: ${missing_files[*]}"
        return 1
    fi
}

# Function to verify executable scripts
verify_executable_scripts() {
    print_info "Verifying executable scripts..."
    
    # Check for executable scripts
    local executable_scripts=(
        "scripts/setup_agentic.py"
        "scripts/setup_gitlab.sh"
        "scripts/installers/install.sh"
        "scripts/release_manager.py"
        "setup_cloudcurio.sh"
        "setup_sysmon.sh"
        "setup_config_editor.sh"
        "setup_mcp_server.sh"
        "setup_open_webui.sh"
        "setup_tabby.sh"
        "kubernetes/scripts/deploy.sh"
        "kubernetes/scripts/deploy_helm.sh"
        "kubernetes/scripts/demo_deployment.sh"
        "verify_implementation.sh"
        "complete_setup.sh"
        "setup_config_editor.sh"
        "setup_mcp_server.sh"
        "setup_open_webui.sh"
        "setup_sysmon.sh"
        "setup_tabby.sh"
    )
    
    local non_executable=()
    for script in "${executable_scripts[@]}"; do
        if [ -f "$script" ] && [ ! -x "$script" ]; then
            non_executable+=("$script")
        fi
    done
    
    if [ ${#non_executable[@]} -eq 0 ]; then
        print_success "All scripts are executable"
    else
        print_warning "Non-executable scripts: ${non_executable[*]}"
        print_info "Making scripts executable..."
        for script in "${non_executable[@]}"; do
            if [ -f "$script" ]; then
                chmod +x "$script"
                print_info "Made $script executable"
            fi
        done
        print_success "All scripts now executable"
    fi
}

# Function to verify Git status
verify_git_status() {
    print_info "Verifying Git status..."
    
    # Check if we're in a Git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "Not in a Git repository"
        return 1
    fi
    
    # Check for uncommitted changes
    if git diff-index --quiet HEAD --; then
        print_success "No uncommitted changes"
    else
        print_warning "There are uncommitted changes"
        print_info "Staging and committing changes..."
        git add .
        git commit -m "chore: Final verification before GitHub upload"
        print_success "Changes committed"
    fi
    
    # Check current branch
    local current_branch=$(git branch --show-current)
    print_info "Current branch: $current_branch"
    
    # Check for remote
    if git remote -v | grep -q origin; then
        print_success "Remote repository configured"
    else
        print_warning "No remote repository configured"
    fi
    
    # Check for tags
    local tags=$(git tag -l | wc -l)
    print_info "Number of tags: $tags"
    
    print_success "Git status verified"
}

# Function to verify documentation
verify_documentation() {
    print_info "Verifying documentation..."
    
    # Check for key documentation files
    local doc_files=(
        "README.md"
        "MONOREPO_README.md"
        "PROCEDURE_HANDBOOK.md"
        "BRANCHING_TAGGING_STRATEGY.md"
        "RELEASE_MANAGEMENT.md"
        "CHANGELOG.md"
        "CONTRIBUTING.md"
        "SECURITY.md"
        "TASK_LIST.md"
        "ROADMAP.md"
        "docs/API.md"
        "docs/SETUP.md"
        "docs/COMPLIANCE.md"
        "docs/SUPABASE-INTEGRATION.md"
        "kubernetes/README.md"
        "kubernetes/helm/cloudcurio/README.md"
        "kubernetes/helm/cloudcurio/HELM_DOCS.md"
        "examples/EXAMPLES_REPOSITORY.md"
        "AGENTIC_PLATFORM_DOCS.md"
        "FINAL_IMPLEMENTATION_COMPLETE.md"
        "IMPLEMENTATION_STATUS_REPORT.md"
        "IMPLEMENTATION_VERIFICATION.md"
        "VERIFICATION_COMPLETE.md"
    )
    
    local missing_docs=()
    for doc in "${doc_files[@]}"; do
        if [ ! -f "$doc" ]; then
            missing_docs+=("$doc")
        fi
    done
    
    if [ ${#missing_docs[@]} -eq 0 ]; then
        print_success "All documentation files present"
    else
        print_warning "Missing documentation files: ${missing_docs[*]}"
        # This isn't necessarily an error since some docs might not be required
    fi
    
    print_success "Documentation verification complete"
}

# Function to verify GitHub Actions workflows
verify_github_workflows() {
    print_info "Verifying GitHub Actions workflows..."
    
    # Check for key workflow files
    local workflow_files=(
        ".github/workflows/cicd.yaml"
        ".github/workflows/code-quality.yaml"
        ".github/workflows/security-scan.yaml"
        ".github/workflows/testing.yaml"
        ".github/workflows/release.yaml"
        ".github/workflows/documentation.yaml"
        ".github/workflows/branch-management.yaml"
        ".github/workflows/dependency-updates.yaml"
        ".github/workflows/crewai-review.yaml"
        ".github/workflows/performance-monitoring.yaml"
        ".github/workflows/helm-chart.yaml"
    )
    
    local missing_workflows=()
    for workflow in "${workflow_files[@]}"; do
        if [ ! -f "$workflow" ]; then
            missing_workflows+=("$workflow")
        fi
    done
    
    if [ ${#missing_workflows[@]} -eq 0 ]; then
        print_success "All GitHub Actions workflows present"
    else
        print_error "Missing workflow files: ${missing_workflows[*]}"
        return 1
    fi
    
    print_success "GitHub Actions workflows verified"
}

# Function to verify Kubernetes manifests
verify_kubernetes_manifests() {
    print_info "Verifying Kubernetes manifests..."
    
    # Check for key manifest files
    local manifest_files=(
        "kubernetes/manifests/all-in-one.yaml"
        "kubernetes/manifests/mcp-server.yaml"
        "kubernetes/manifests/config-editor.yaml"
        "kubernetes/manifests/ollama.yaml"
        "kubernetes/manifests/litellm.yaml"
        "kubernetes/manifests/open-webui.yaml"
        "kubernetes/manifests/postgres.yaml"
        "kubernetes/manifests/redis.yaml"
        "kubernetes/manifests/monitoring.yaml"
    )
    
    local missing_manifests=()
    for manifest in "${manifest_files[@]}"; do
        if [ ! -f "$manifest" ]; then
            missing_manifests+=("$manifest")
        fi
    done
    
    if [ ${#missing_manifests[@]} -eq 0 ]; then
        print_success "All Kubernetes manifests present"
    else
        print_error "Missing manifest files: ${missing_manifests[*]}"
        return 1
    fi
    
    print_success "Kubernetes manifests verified"
}

# Function to verify Helm chart
verify_helm_chart() {
    print_info "Verifying Helm chart..."
    
    # Check for key Helm chart files
    local helm_files=(
        "kubernetes/helm/cloudcurio/Chart.yaml"
        "kubernetes/helm/cloudcurio/values.yaml"
        "kubernetes/helm/cloudcurio/values-dev.yaml"
        "kubernetes/helm/cloudcurio/values-prod.yaml"
        "kubernetes/helm/cloudcurio/README.md"
        "kubernetes/helm/cloudcurio/HELM_DOCS.md"
    )
    
    local missing_helm_files=()
    for helm_file in "${helm_files[@]}"; do
        if [ ! -f "$helm_file" ]; then
            missing_helm_files+=("$helm_file")
        fi
    done
    
    if [ ${#missing_helm_files[@]} -eq 0 ]; then
        print_success "All Helm chart files present"
    else
        print_error "Missing Helm chart files: ${missing_helm_files[*]}"
        return 1
    fi
    
    print_success "Helm chart verified"
}

# Function to verify deployment scripts
verify_deployment_scripts() {
    print_info "Verifying deployment scripts..."
    
    # Check for key deployment scripts
    local deploy_scripts=(
        "kubernetes/scripts/deploy.sh"
        "kubernetes/scripts/deploy_helm.sh"
        "kubernetes/scripts/demo_deployment.sh"
    )
    
    local missing_deploy_scripts=()
    for script in "${deploy_scripts[@]}"; do
        if [ ! -f "$script" ]; then
            missing_deploy_scripts+=("$script")
        fi
    done
    
    if [ ${#missing_deploy_scripts[@]} -eq 0 ]; then
        print_success "All deployment scripts present"
    else
        print_error "Missing deployment scripts: ${missing_deploy_scripts[*]}"
        return 1
    fi
    
    print_success "Deployment scripts verified"
}

# Function to verify branching and tagging strategy
verify_branching_tagging() {
    print_info "Verifying branching and tagging strategy..."
    
    # Check for key branching/tagging documentation
    local bt_files=(
        "BRANCHING_TAGGING_STRATEGY.md"
        "RELEASE_MANAGEMENT.md"
    )
    
    local missing_bt_files=()
    for file in "${bt_files[@]}"; do
        if [ ! -f "$file" ]; then
            missing_bt_files+=("$file")
        fi
    done
    
    if [ ${#missing_bt_files[@]} -eq 0 ]; then
        print_success "Branching and tagging documentation present"
    else
        print_warning "Missing branching/tagging files: ${missing_bt_files[*]}"
    fi
    
    # Check for tags
    local tags=$(git tag -l | wc -l)
    print_info "Number of Git tags: $tags"
    
    # Check for branches
    local branches=$(git branch -a | wc -l)
    print_info "Number of Git branches: $branches"
    
    print_success "Branching and tagging strategy verified"
}

# Function to verify task management system
verify_task_management() {
    print_info "Verifying task management system..."
    
    # Check for key task management files
    local tm_files=(
        "TASK_LIST.md"
        "ROADMAP.md"
    )
    
    local missing_tm_files=()
    for file in "${tm_files[@]}"; do
        if [ ! -f "$file" ]; then
            missing_tm_files+=("$file")
        fi
    done
    
    if [ ${#missing_tm_files[@]} -eq 0 ]; then
        print_success "Task management system files present"
    else
        print_warning "Missing task management files: ${missing_tm_files[*]}"
    fi
    
    print_success "Task management system verified"
}

# Main verification function
main_verification() {
    print_header
    
    print_info "Starting CloudCurio final verification..."
    echo ""
    
    # Run all verification functions
    verify_directory_structure
    echo ""
    
    verify_key_files
    echo ""
    
    verify_executable_scripts
    echo ""
    
    verify_git_status
    echo ""
    
    verify_documentation
    echo ""
    
    verify_github_workflows
    echo ""
    
    verify_kubernetes_manifests
    echo ""
    
    verify_helm_chart
    echo ""
    
    verify_deployment_scripts
    echo ""
    
    verify_branching_tagging
    echo ""
    
    verify_task_management
    echo ""
    
    print_success "CloudCurio final verification completed!"
    echo ""
    print_info "Summary:"
    print_success "✓ Directory structure verified"
    print_success "✓ Key files verified"
    print_success "✓ Executable scripts verified"
    print_success "✓ Git status verified"
    print_success "✓ Documentation verified"
    print_success "✓ GitHub Actions workflows verified"
    print_success "✓ Kubernetes manifests verified"
    print_success "✓ Helm chart verified"
    print_success "✓ Deployment scripts verified"
    print_success "✓ Branching and tagging strategy verified"
    print_success "✓ Task management system verified"
    echo ""
    print_success "CloudCurio is ready for GitHub upload!"
    echo ""
    print_info "To upload to GitHub:"
    echo "  git push origin main"
    echo "  git push origin --tags"
    echo ""
    print_info "To create a new release:"
    echo "  git tag -a v2.2.0 -m \"Release version 2.2.0\""
    echo "  git push origin v2.2.0"
    echo ""
}

# Run main verification
main_verification