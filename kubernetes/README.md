# CloudCurio Kubernetes Deployment Manifests

This directory contains all Kubernetes manifests for deploying CloudCurio on a Kubernetes cluster.

## Structure

```
kubernetes/
├── manifests/           # Raw Kubernetes manifests
├── helm/               # Helm charts for CloudCurio
├── configs/            # Configuration files for Kubernetes deployments
└── scripts/            # Utility scripts for Kubernetes operations
```

## Deployment Options

### 1. Raw Kubernetes Manifests
Deploy using kubectl with the manifests in the `manifests/` directory:

```bash
kubectl apply -f kubernetes/manifests/
```

### 2. Helm Charts
Deploy using Helm with the charts in the `helm/` directory:

```bash
helm install cloudcurio kubernetes/helm/cloudcurio
```

## Components

The Kubernetes deployment includes:

1. **MCP Server** - Main API for managing AI crews
2. **Config Editor** - Web interface for managing configurations
3. **Ollama** - Local AI models for offline operation
4. **LiteLLM** - AI provider abstraction layer
5. **Open WebUI** - Graphical interface for AI interaction
6. **Database** - PostgreSQL for storing crew results and telemetry
7. **Redis** - In-memory data structure store for caching
8. **Monitoring** - Prometheus, Grafana, and Loki for observability

## Prerequisites

- Kubernetes cluster (v1.20+)
- kubectl CLI
- Helm CLI (for Helm deployments)
- Access to container registry (Docker Hub by default)

## Configuration

All components can be configured through:

1. **Environment Variables** - Set in the manifests
2. **ConfigMaps** - For non-sensitive configuration
3. **Secrets** - For sensitive data like API keys
4. **Helm Values** - For Helm-based deployments

## Scaling

Components can be scaled independently:

- MCP Server: Horizontal pod autoscaler
- Config Editor: Horizontal pod autoscaler
- Ollama: Stateful set for model persistence
- LiteLLM: Horizontal pod autoscaler
- Open WebUI: Horizontal pod autoscaler
- Database: Stateful set with persistent volumes
- Redis: Stateful set with persistent volumes
- Monitoring: Horizontal pod autoscaler

## Security

Security features include:

- Network policies for inter-service communication
- Role-based access control (RBAC)
- Pod security policies
- Secrets management
- TLS encryption for inter-service communication
- Ingress controller with TLS termination

## Monitoring

Monitoring is provided by:

- Prometheus for metrics collection
- Grafana for visualization
- Loki for log aggregation
- Alertmanager for alerting

## Backup and Recovery

Backup and recovery strategies:

- Database backups with Velero or similar tools
- Persistent volume snapshots
- Configuration backups
- Disaster recovery procedures

## Updates and Upgrades

Update procedures:

- Rolling updates for stateless services
- Blue-green deployments for zero-downtime updates
- Canary deployments for gradual rollouts
- Automated updates with ArgoCD or Flux

## Troubleshooting

Common troubleshooting steps:

- Check pod status: `kubectl get pods`
- Check logs: `kubectl logs <pod-name>`
- Check events: `kubectl get events`
- Check services: `kubectl get services`
- Check ingress: `kubectl get ingress`
- Describe resources: `kubectl describe <resource> <name>`

## Contributing

See the CONTRIBUTING.md file for guidelines on how to contribute to the Kubernetes deployment manifests.