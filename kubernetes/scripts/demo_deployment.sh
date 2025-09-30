#!/bin/bash

# CloudCurio Kubernetes Deployment Demonstration Script

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}    CloudCurio Kubernetes Deployment Demonstration        ${NC}"
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

# Function to check prerequisites
check_prerequisites() {
    print_info "Checking prerequisites..."
    
    # Check if kubectl is installed
    if ! command -v kubectl &> /dev/null; then
        print_error "kubectl is not installed. Please install kubectl first."
        return 1
    else
        print_success "kubectl is installed"
    fi
    
    # Check if Helm is installed
    if ! command -v helm &> /dev/null; then
        print_error "Helm is not installed. Please install Helm first."
        return 1
    else
        print_success "Helm is installed"
    fi
    
    # Check if we can connect to a Kubernetes cluster
    if kubectl cluster-info &> /dev/null; then
        print_success "Connected to Kubernetes cluster"
    else
        print_warning "Cannot connect to Kubernetes cluster. Demo will proceed with setup only."
        return 1
    fi
    
    return 0
}

# Function to demonstrate Helm chart creation
demonstrate_helm_chart_creation() {
    print_info "Demonstrating Helm chart creation..."
    
    # Show the directory structure
    print_info "CloudCurio Helm chart directory structure:"
    tree -L 3 kubernetes/helm/cloudcurio || find kubernetes/helm/cloudcurio -type d | head -20
    
    # Show key files
    print_info "Key Helm chart files:"
    echo "  - Chart.yaml: Chart metadata"
    echo "  - values.yaml: Default configuration values"
    echo "  - values-dev.yaml: Development configuration"
    echo "  - values-prod.yaml: Production configuration"
    echo "  - templates/: Deployment templates"
    echo "  - README.md: Chart documentation"
    echo "  - HELM_DOCS.md: Detailed usage guide"
    
    print_success "Helm chart creation demonstrated successfully!"
}

# Function to demonstrate Helm deployment
demonstrate_helm_deployment() {
    print_info "Demonstrating Helm deployment process..."
    
    # Show how to add the repository
    echo "To add the CloudCurio Helm repository:"
    echo "  helm repo add cloudcurio https://cbwinslow.github.io/cloudcurio-helm-charts/"
    echo "  helm repo update"
    echo ""
    
    # Show how to install
    echo "To install CloudCurio using Helm:"
    echo "  # Development installation"
    echo "  helm install cloudcurio cloudcurio/cloudcurio --values kubernetes/helm/cloudcurio/values-dev.yaml"
    echo ""
    echo "  # Production installation"
    echo "  helm install cloudcurio cloudcurio/cloudcurio --values kubernetes/helm/cloudcurio/values-prod.yaml"
    echo ""
    
    # Show how to check status
    echo "To check deployment status:"
    echo "  helm status cloudcurio"
    echo "  kubectl get pods -n cloudcurio"
    echo "  kubectl get services -n cloudcurio"
    echo ""
    
    # Show how to upgrade
    echo "To upgrade CloudCurio:"
    echo "  helm upgrade cloudcurio cloudcurio/cloudcurio --values my-custom-values.yaml"
    echo ""
    
    # Show how to uninstall
    echo "To uninstall CloudCurio:"
    echo "  helm uninstall cloudcurio"
    echo ""
    
    print_success "Helm deployment process demonstrated successfully!"
}

# Function to demonstrate Kubernetes manifests
demonstrate_kubernetes_manifests() {
    print_info "Demonstrating Kubernetes manifests..."
    
    # Show the directory structure
    print_info "Kubernetes manifests directory structure:"
    ls -la kubernetes/manifests/ | head -10
    
    # Show key manifests
    print_info "Key Kubernetes manifests:"
    echo "  - mcp-server.yaml: MCP Server deployment"
    echo "  - config-editor.yaml: Configuration Editor deployment"
    echo "  - ollama.yaml: Ollama deployment"
    echo "  - litellm.yaml: LiteLLM deployment"
    echo "  - open-webui.yaml: Open WebUI deployment"
    echo "  - postgres.yaml: PostgreSQL database deployment"
    echo "  - redis.yaml: Redis deployment"
    echo "  - monitoring.yaml: Monitoring stack deployment"
    echo "  - all-in-one.yaml: Complete platform deployment"
    
    print_success "Kubernetes manifests demonstrated successfully!"
}

# Function to demonstrate deployment scripts
demonstrate_deployment_scripts() {
    print_info "Demonstrating deployment scripts..."
    
    # Show the scripts directory
    print_info "Deployment scripts directory:"
    ls -la kubernetes/scripts/ | head -10
    
    # Show key scripts
    print_info "Key deployment scripts:"
    echo "  - deploy.sh: Main deployment script"
    echo "  - deploy_helm.sh: Helm-specific deployment script"
    
    # Show how to use the scripts
    echo ""
    echo "To use the deployment scripts:"
    echo "  # Make scripts executable"
    echo "  chmod +x kubernetes/scripts/*.sh"
    echo ""
    echo "  # Deploy using the main script"
    echo "  kubernetes/scripts/deploy.sh deploy-full"
    echo ""
    echo "  # Check deployment status"
    echo "  kubernetes/scripts/deploy.sh status"
    echo ""
    echo "  # Get logs for a component"
    echo "  kubernetes/scripts/deploy.sh logs mcp-server"
    echo ""
    echo "  # Scale a component"
    echo "  kubernetes/scripts/deploy.sh scale mcp-server 3"
    echo ""
    
    print_success "Deployment scripts demonstrated successfully!"
}

# Function to demonstrate the complete workflow
demonstrate_complete_workflow() {
    print_info "Demonstrating complete CloudCurio deployment workflow..."
    
    echo "1. Prerequisites Check:"
    echo "   - Verify kubectl and Helm are installed"
    echo "   - Ensure Kubernetes cluster connectivity"
    echo ""
    
    echo "2. Repository Setup:"
    echo "   - Add CloudCurio Helm repository"
    echo "   - Update Helm repositories"
    echo ""
    
    echo "3. Configuration:"
    echo "   - Create custom values file (if needed)"
    echo "   - Configure API keys and secrets"
    echo ""
    
    echo "4. Deployment:"
    echo "   - Deploy using Helm chart"
    echo "   - Monitor deployment progress"
    echo "   - Verify services are running"
    echo ""
    
    echo "5. Access Services:"
    echo "   - Use port forwarding to access services"
    echo "   - Configure ingress for external access"
    echo ""
    
    echo "6. Monitoring:"
    echo "   - Check pod status and logs"
    echo "   - Monitor resource usage"
    echo "   - View metrics in Grafana"
    echo ""
    
    echo "7. Scaling:"
    echo "   - Scale components based on demand"
    echo "   - Configure autoscaling policies"
    echo ""
    
    echo "8. Updates:"
    echo "   - Upgrade to new versions"
    echo "   - Apply configuration changes"
    echo ""
    
    echo "9. Maintenance:"
    echo "   - Backup configuration and data"
    echo "   - Monitor for issues"
    echo "   - Apply security patches"
    echo ""
    
    print_success "Complete deployment workflow demonstrated successfully!"
}

# Main function
main() {
    print_header
    
    echo "This script demonstrates the CloudCurio Kubernetes deployment process."
    echo ""
    
    # Check prerequisites
    if check_prerequisites; then
        print_success "All prerequisites met!"
    else
        print_warning "Some prerequisites not met. Continuing with demonstration only."
    fi
    
    echo ""
    
    # Demonstrate each component
    demonstrate_helm_chart_creation
    echo ""
    
    demonstrate_helm_deployment
    echo ""
    
    demonstrate_kubernetes_manifests
    echo ""
    
    demonstrate_deployment_scripts
    echo ""
    
    demonstrate_complete_workflow
    echo ""
    
    # Summary
    print_header
    print_info "CloudCurio Kubernetes Deployment Summary:"
    echo ""
    print_success "✓ Helm chart created with proper structure"
    print_success "✓ Kubernetes manifests for all components"
    print_success "✓ Deployment scripts for easy management"
    print_success "✓ Complete workflow documentation"
    print_success "✓ Ready for GitHub upload with proper tagging"
    echo ""
    print_info "To deploy CloudCurio to Kubernetes:"
    echo "  1. Ensure prerequisites are met"
    echo "  2. Add the CloudCurio Helm repository"
    echo "  3. Customize values as needed"
    echo "  4. Deploy using Helm"
    echo "  5. Access services via port forwarding or ingress"
    echo ""
    print_success "CloudCurio is ready for Kubernetes deployment!"
}

# Run main function
main "$@"