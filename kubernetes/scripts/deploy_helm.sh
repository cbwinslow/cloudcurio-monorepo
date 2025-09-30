#!/bin/bash

# CloudCurio Helm Deployment Script

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}    CloudCurio Helm Deployment        ${NC}"
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
    
    # Check if Helm is installed
    if ! command -v helm &> /dev/null; then
        print_error "Helm is not installed. Please install Helm first."
        exit 1
    else
        print_success "Helm is installed"
    fi
    
    # Check if kubectl is installed
    if ! command -v kubectl &> /dev/null; then
        print_error "kubectl is not installed. Please install kubectl first."
        exit 1
    else
        print_success "kubectl is installed"
    fi
    
    # Check if we can connect to a Kubernetes cluster
    if kubectl cluster-info &> /dev/null; then
        print_success "Connected to Kubernetes cluster"
    else
        print_error "Cannot connect to Kubernetes cluster. Please ensure kubectl is configured properly."
        exit 1
    fi
    
    # Check if we're in the right directory
    if [ ! -d "kubernetes/helm/cloudcurio" ] || [ ! -f "kubernetes/helm/cloudcurio/Chart.yaml" ]; then
        print_error "Not in CloudCurio project directory. Please run this script from the project root."
        exit 1
    fi
}

# Function to deploy CloudCurio using Helm
deploy_cloudcurio_helm() {
    local release_name=${1:-"cloudcurio"}
    local namespace=${2:-"cloudcurio"}
    local values_file=${3:-""}
    
    print_info "Deploying CloudCurio using Helm..."
    
    # Create namespace if it doesn't exist
    if ! kubectl get namespace "$namespace" &> /dev/null; then
        print_info "Creating namespace $namespace..."
        kubectl create namespace "$namespace"
        print_success "Namespace $namespace created"
    else
        print_info "Namespace $namespace already exists"
    fi
    
    # Add dependencies if needed
    print_info "Adding Helm dependencies..."
    helm dependency update kubernetes/helm/cloudcurio
    
    # Deploy using Helm
    print_info "Deploying CloudCurio Helm chart..."
    
    local helm_cmd="helm upgrade --install $release_name kubernetes/helm/cloudcurio --namespace $namespace"
    
    if [ -n "$values_file" ] && [ -f "$values_file" ]; then
        helm_cmd="$helm_cmd -f $values_file"
    fi
    
    # Execute the Helm command
    eval $helm_cmd
    
    if [ $? -eq 0 ]; then
        print_success "CloudCurio deployed successfully using Helm!"
        print_info "Release name: $release_name"
        print_info "Namespace: $namespace"
        
        # Show deployment status
        print_info "Deployment status:"
        helm status $release_name --namespace $namespace
        
        # Show services
        print_info "Available services:"
        kubectl get services --namespace $namespace
        
        # Show pods
        print_info "Running pods:"
        kubectl get pods --namespace $namespace
        
        print_success "CloudCurio is now running in your Kubernetes cluster!"
        print_info "Access services using port forwarding:"
        print_info "  kubectl port-forward svc/cloudcurio-mcp-server 8000:8000 --namespace $namespace"
        print_info "  kubectl port-forward svc/cloudcurio-config-editor 8081:8081 --namespace $namespace"
        print_info "  kubectl port-forward svc/ollama-service 11434:11434 --namespace $namespace"
        print_info "  kubectl port-forward svc/litellm-service 4000:4000 --namespace $namespace"
        print_info "  kubectl port-forward svc/open-webui-service 3000:3000 --namespace $namespace"
    else
        print_error "Failed to deploy CloudCurio using Helm"
        exit 1
    fi
}

# Function to undeploy CloudCurio using Helm
undeploy_cloudcurio_helm() {
    local release_name=${1:-"cloudcurio"}
    local namespace=${2:-"cloudcurio"}
    
    print_info "Undeploying CloudCurio using Helm..."
    
    # Check if release exists
    if helm status $release_name --namespace $namespace &> /dev/null; then
        print_info "Deleting CloudCurio release..."
        helm uninstall $release_name --namespace $namespace
        
        if [ $? -eq 0 ]; then
            print_success "CloudCurio release deleted successfully!"
        else
            print_error "Failed to delete CloudCurio release"
            exit 1
        fi
    else
        print_warning "CloudCurio release not found"
    fi
    
    # Optionally delete namespace
    read -p "Do you want to delete the namespace $namespace? [y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Deleting namespace $namespace..."
        kubectl delete namespace $namespace
        
        if [ $? -eq 0 ]; then
            print_success "Namespace $namespace deleted successfully!"
        else
            print_error "Failed to delete namespace $namespace"
            exit 1
        fi
    else
        print_info "Namespace $namespace not deleted"
    fi
    
    print_success "CloudCurio undeployed successfully!"
}

# Function to check deployment status
check_status() {
    local release_name=${1:-"cloudcurio"}
    local namespace=${2:-"cloudcurio"}
    
    print_info "Checking CloudCurio deployment status..."
    
    # Check Helm release status
    print_info "Helm release status:"
    helm status $release_name --namespace $namespace
    
    # Check Kubernetes resources
    print_info "Kubernetes resources:"
    echo ""
    echo "Namespaces:"
    kubectl get namespaces | grep $namespace || echo "Namespace $namespace not found"
    
    echo ""
    echo "Deployments:"
    kubectl get deployments --namespace $namespace || echo "No deployments found in namespace $namespace"
    
    echo ""
    echo "Services:"
    kubectl get services --namespace $namespace || echo "No services found in namespace $namespace"
    
    echo ""
    echo "Pods:"
    kubectl get pods --namespace $namespace || echo "No pods found in namespace $namespace"
    
    echo ""
    echo "PersistentVolumeClaims:"
    kubectl get pvc --namespace $namespace || echo "No PVCs found in namespace $namespace"
    
    print_success "Status check complete!"
}

# Function to scale components
scale_component() {
    local release_name=${1:-"cloudcurio"}
    local namespace=${2:-"cloudcurio"}
    local component=$3
    local replicas=$4
    
    if [ -z "$component" ] || [ -z "$replicas" ]; then
        print_error "Usage: scale <release_name> <namespace> <component> <replicas>"
        return 1
    fi
    
    print_info "Scaling $component to $replicas replicas..."
    
    # Use kubectl to scale the deployment
    kubectl scale deployment/$component --namespace $namespace --replicas=$replicas
    
    if [ $? -eq 0 ]; then
        print_success "Scaled $component to $replicas replicas"
    else
        print_error "Failed to scale $component"
        exit 1
    fi
}

# Function to get logs
get_logs() {
    local release_name=${1:-"cloudcurio"}
    local namespace=${2:-"cloudcurio"}
    local component=${3:-"cloudcurio-mcp-server"}
    
    print_info "Getting logs for $component..."
    
    kubectl logs deployment/$component --namespace $namespace --tail=50
    
    if [ $? -ne 0 ]; then
        print_error "Failed to get logs for $component"
        exit 1
    fi
}

# Main function
main() {
    print_header
    
    # Parse command line arguments
    if [ $# -eq 0 ]; then
        echo "CloudCurio Helm Deployment Script"
        echo ""
        echo "Usage: $0 [COMMAND] [OPTIONS]"
        echo ""
        echo "Commands:"
        echo "  deploy [release_name] [namespace] [values_file]  Deploy CloudCurio using Helm"
        echo "  undeploy [release_name] [namespace]              Undeploy CloudCurio using Helm"
        echo "  status [release_name] [namespace]                Check deployment status"
        echo "  scale [release_name] [namespace] [component] [replicas]  Scale a component"
        echo "  logs [release_name] [namespace] [component]      Get logs for a component"
        echo "  check-prereqs                                    Check deployment prerequisites"
        echo ""
        echo "Defaults:"
        echo "  release_name: cloudcurio"
        echo "  namespace: cloudcurio"
        echo "  values_file: (none)"
        echo "  component: cloudcurio-mcp-server"
        echo ""
        exit 0
    fi
    
    local command=$1
    shift
    
    case $command in
        "check-prereqs")
            check_prerequisites
            ;;
        "deploy")
            check_prerequisites
            deploy_cloudcurio_helm "$@"
            ;;
        "undeploy")
            undeploy_cloudcurio_helm "$@"
            ;;
        "status")
            check_status "$@"
            ;;
        "scale")
            scale_component "$@"
            ;;
        "logs")
            get_logs "$@"
            ;;
        *)
            print_error "Unknown command: $command"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"