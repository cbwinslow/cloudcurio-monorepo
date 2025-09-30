#!/bin/bash

# CloudCurio Kubernetes Deployment Script
# This script deploys the complete CloudCurio platform to a Kubernetes cluster

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}    CloudCurio Kubernetes Deployment        ${NC}"
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
        exit 1
    else
        print_success "kubectl is installed"
    fi
    
    # Check if Helm is installed (optional but recommended)
    if command -v helm &> /dev/null; then
        print_success "Helm is installed"
    else
        print_warning "Helm is not installed. Some features may not work."
    fi
    
    # Check if we can connect to a Kubernetes cluster
    if kubectl cluster-info &> /dev/null; then
        print_success "Connected to Kubernetes cluster"
    else
        print_error "Cannot connect to Kubernetes cluster. Please ensure kubectl is configured properly."
        exit 1
    fi
    
    # Check if we're in the right directory
    if [ ! -d "kubernetes" ] || [ ! -f "kubernetes/README.md" ]; then
        print_error "Not in CloudCurio project directory. Please run this script from the project root."
        exit 1
    fi
}

# Function to deploy the complete CloudCurio platform
deploy_complete_platform() {
    print_info "Deploying complete CloudCurio platform..."
    
    # Apply all manifests in order
    manifests=(
        "kubernetes/manifests/all-in-one.yaml"
        "kubernetes/manifests/postgres.yaml"
        "kubernetes/manifests/redis.yaml"
        "kubernetes/manifests/mcp-server.yaml"
        "kubernetes/manifests/config-editor.yaml"
        "kubernetes/manifests/ollama.yaml"
        "kubernetes/manifests/litellm.yaml"
        "kubernetes/manifests/open-webui.yaml"
        "kubernetes/manifests/monitoring.yaml"
    )
    
    for manifest in "${manifests[@]}"; do
        if [ -f "$manifest" ]; then
            print_info "Applying $manifest..."
            kubectl apply -f "$manifest"
            print_success "Applied $manifest"
        else
            print_warning "Manifest $manifest not found, skipping..."
        fi
    done
    
    print_success "Complete CloudCurio platform deployed!"
}

# Function to deploy individual components
deploy_component() {
    local component=$1
    local manifest="kubernetes/manifests/${component}.yaml"
    
    if [ -f "$manifest" ]; then
        print_info "Deploying $component..."
        kubectl apply -f "$manifest"
        print_success "Deployed $component"
    else
        print_error "Manifest for $component not found: $manifest"
        exit 1
    fi
}

# Function to undeploy the complete platform
undeploy_complete_platform() {
    print_info "Undeploying complete CloudCurio platform..."
    
    # Delete all manifests in reverse order
    manifests=(
        "kubernetes/manifests/monitoring.yaml"
        "kubernetes/manifests/open-webui.yaml"
        "kubernetes/manifests/litellm.yaml"
        "kubernetes/manifests/ollama.yaml"
        "kubernetes/manifests/config-editor.yaml"
        "kubernetes/manifests/mcp-server.yaml"
        "kubernetes/manifests/redis.yaml"
        "kubernetes/manifests/postgres.yaml"
        "kubernetes/manifests/all-in-one.yaml"
    )
    
    for manifest in "${manifests[@]}"; do
        if [ -f "$manifest" ]; then
            print_info "Deleting resources from $manifest..."
            kubectl delete -f "$manifest" --ignore-not-found=true
            print_success "Deleted resources from $manifest"
        else
            print_warning "Manifest $manifest not found, skipping..."
        fi
    done
    
    print_success "Complete CloudCurio platform undeployed!"
}

# Function to check deployment status
check_status() {
    print_info "Checking CloudCurio deployment status..."
    
    echo ""
    echo "Namespaces:"
    kubectl get namespaces | grep cloudcurio || echo "No CloudCurio namespaces found"
    
    echo ""
    echo "Deployments:"
    kubectl get deployments -n cloudcurio || echo "No CloudCurio deployments found"
    
    echo ""
    echo "Services:"
    kubectl get services -n cloudcurio || echo "No CloudCurio services found"
    
    echo ""
    echo "Pods:"
    kubectl get pods -n cloudcurio || echo "No CloudCurio pods found"
    
    echo ""
    echo "Monitoring Deployments:"
    kubectl get deployments -n cloudcurio-monitoring || echo "No monitoring deployments found"
    
    echo ""
    echo "Monitoring Services:"
    kubectl get services -n cloudcurio-monitoring || echo "No monitoring services found"
    
    print_success "Status check complete!"
}

# Function to get deployment logs
get_logs() {
    local component=${1:-"mcp-server"}
    
    print_info "Getting logs for $component..."
    
    case $component in
        "mcp-server")
            kubectl logs -n cloudcurio deployment/cloudcurio-mcp-server --tail=50
            ;;
        "config-editor")
            kubectl logs -n cloudcurio deployment/cloudcurio-config-editor --tail=50
            ;;
        "ollama")
            kubectl logs -n cloudcurio deployment/ollama-deployment --tail=50
            ;;
        "litellm")
            kubectl logs -n cloudcurio deployment/litellm-deployment --tail=50
            ;;
        "open-webui")
            kubectl logs -n cloudcurio deployment/open-webui-deployment --tail=50
            ;;
        "postgres")
            kubectl logs -n cloudcurio deployment/postgres-deployment --tail=50
            ;;
        "redis")
            kubectl logs -n cloudcurio deployment/redis-deployment --tail=50
            ;;
        "prometheus")
            kubectl logs -n cloudcurio-monitoring deployment/prometheus-deployment --tail=50
            ;;
        "grafana")
            kubectl logs -n cloudcurio-monitoring deployment/grafana-deployment --tail=50
            ;;
        "loki")
            kubectl logs -n cloudcurio-monitoring deployment/loki-deployment --tail=50
            ;;
        *)
            kubectl logs -n cloudcurio deployment/$component --tail=50
            ;;
    esac
}

# Function to scale components
scale_component() {
    local component=$1
    local replicas=$2
    
    if [ -z "$component" ] || [ -z "$replicas" ]; then
        print_error "Usage: scale <component> <replicas>"
        return 1
    fi
    
    print_info "Scaling $component to $replicas replicas..."
    kubectl scale deployment/$component -n cloudcurio --replicas=$replicas
    print_success "Scaled $component to $replicas replicas"
}

# Main function
main() {
    print_header
    
    # Parse command line arguments
    if [ $# -eq 0 ]; then
        echo "CloudCurio Kubernetes Deployment Script"
        echo ""
        echo "Usage: $0 [COMMAND] [OPTIONS]"
        echo ""
        echo "Commands:"
        echo "  deploy-full        Deploy the complete CloudCurio platform"
        echo "  deploy <component> Deploy a specific component"
        echo "  undeploy-full      Undeploy the complete CloudCurio platform"
        echo "  status             Check deployment status"
        echo "  logs <component>   Get logs for a component"
        echo "  scale <comp> <n>   Scale a component to n replicas"
        echo "  check-prereqs      Check deployment prerequisites"
        echo ""
        echo "Components: mcp-server, config-editor, ollama, litellm, open-webui, postgres, redis"
        echo "Monitoring: prometheus, grafana, loki"
        echo ""
        exit 0
    fi
    
    local command=$1
    shift
    
    case $command in
        "check-prereqs")
            check_prerequisites
            ;;
        "deploy-full")
            check_prerequisites
            deploy_complete_platform
            ;;
        "deploy")
            check_prerequisites
            if [ $# -eq 0 ]; then
                print_error "Component name required"
                exit 1
            fi
            deploy_component "$1"
            ;;
        "undeploy-full")
            undeploy_complete_platform
            ;;
        "status")
            check_status
            ;;
        "logs")
            if [ $# -eq 0 ]; then
                get_logs
            else
                get_logs "$1"
            fi
            ;;
        "scale")
            if [ $# -lt 2 ]; then
                print_error "Usage: scale <component> <replicas>"
                exit 1
            fi
            scale_component "$1" "$2"
            ;;
        *)
            print_error "Unknown command: $command"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"