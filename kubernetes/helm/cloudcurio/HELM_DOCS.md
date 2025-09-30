# CloudCurio Helm Chart Documentation

This documentation explains how to use the CloudCurio Helm chart to deploy the complete platform to Kubernetes.

## Prerequisites

Before deploying CloudCurio using Helm, ensure you have:

1. **Kubernetes Cluster**: Access to a Kubernetes cluster (v1.20+)
2. **Helm CLI**: Helm 3.0+ installed locally
3. **kubectl**: kubectl configured to access your cluster
4. **NVidia GPU Drivers**: If using Ollama with GPU acceleration
5. **Storage Class**: Default StorageClass configured for dynamic provisioning
6. **Ingress Controller**: If exposing services externally (optional)

## Installing Helm

If you don't have Helm installed, follow these steps:

### On Linux/macOS:
```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

### On Windows (using Chocolatey):
```powershell
choco install kubernetes-helm
```

### On Windows (using Scoop):
```powershell
scoop install helm
```

## Adding the CloudCurio Helm Repository

To use the CloudCurio Helm chart, add the repository:

```bash
helm repo add cloudcurio https://cbwinslow.github.io/cloudcurio-helm-charts/
helm repo update
```

## Installing CloudCurio

### Quick Installation (Development)
For a quick development installation:

```bash
helm install cloudcurio cloudcurio/cloudcurio --values kubernetes/helm/cloudcurio/values-dev.yaml
```

### Production Installation
For a production installation:

```bash
helm install cloudcurio cloudcurio/cloudcurio --values kubernetes/helm/cloudcurio/values-prod.yaml
```

### Custom Installation
To customize the installation, create a custom values file:

```bash
# Create a custom values file
cp kubernetes/helm/cloudcurio/values.yaml.template my-values.yaml

# Edit the values file to match your requirements
nano my-values.yaml

# Install with custom values
helm install cloudcurio cloudcurio/cloudcurio --values my-values.yaml
```

## Configuration Options

### Global Configuration
| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `global.imageRegistry` | Global Docker image registry | `""` |
| `global.imageTag` | Global Docker image tag | `"2.2.0"` |
| `global.namespace` | Namespace to deploy CloudCurio to | `"cloudcurio"` |

### MCP Server Configuration
| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `mcpServer.enabled` | Enable MCP Server deployment | `true` |
| `mcpServer.replicaCount` | Number of MCP Server replicas | `1` |
| `mcpServer.service.port` | MCP Server service port | `8000` |
| `mcpServer.resources.limits.cpu` | MCP Server CPU limit | `"1000m"` |
| `mcpServer.resources.limits.memory` | MCP Server memory limit | `"1Gi"` |

### Configuration Editor Configuration
| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `configEditor.enabled` | Enable Configuration Editor deployment | `true` |
| `configEditor.replicaCount` | Number of Configuration Editor replicas | `1` |
| `configEditor.service.port` | Configuration Editor service port | `8081` |
| `configEditor.resources.limits.cpu` | Configuration Editor CPU limit | `"500m"` |
| `configEditor.resources.limits.memory` | Configuration Editor memory limit | `"512Mi"` |

### Ollama Configuration
| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `ollama.enabled` | Enable Ollama deployment | `true` |
| `ollama.replicaCount` | Number of Ollama replicas | `1` |
| `ollama.service.port` | Ollama service port | `11434` |
| `ollama.resources.limits.cpu` | Ollama CPU limit | `"2000m"` |
| `ollama.resources.limits.memory` | Ollama memory limit | `"4Gi"` |
| `ollama.resources.limits.nvidia.com/gpu` | Ollama GPU limit | `"1"` |

### LiteLLM Configuration
| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `litellm.enabled` | Enable LiteLLM deployment | `true` |
| `litellm.replicaCount` | Number of LiteLLM replicas | `1` |
| `litellm.service.port` | LiteLLM service port | `4000` |
| `litellm.resources.limits.cpu` | LiteLLM CPU limit | `"1000m"` |
| `litellm.resources.limits.memory` | LiteLLM memory limit | `"1Gi"` |

### Open WebUI Configuration
| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `openWebUI.enabled` | Enable Open WebUI deployment | `true` |
| `openWebUI.replicaCount` | Number of Open WebUI replicas | `1` |
| `openWebUI.service.port` | Open WebUI service port | `3000` |
| `openWebUI.resources.limits.cpu` | Open WebUI CPU limit | `"1000m"` |
| `openWebUI.resources.limits.memory` | Open WebUI memory limit | `"1Gi"` |

### PostgreSQL Configuration
| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `postgresql.enabled` | Enable PostgreSQL deployment | `true` |
| `postgresql.replicaCount` | Number of PostgreSQL replicas | `1` |
| `postgresql.service.port` | PostgreSQL service port | `5432` |
| `postgresql.auth.username` | PostgreSQL username | `"postgres"` |
| `postgresql.auth.password` | PostgreSQL password | `"password"` |
| `postgresql.auth.database` | PostgreSQL database | `"cloudcurio"` |
| `postgresql.resources.limits.cpu` | PostgreSQL CPU limit | `"1000m"` |
| `postgresql.resources.limits.memory` | PostgreSQL memory limit | `"1Gi"` |

### Redis Configuration
| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `redis.enabled` | Enable Redis deployment | `true` |
| `redis.replicaCount` | Number of Redis replicas | `1` |
| `redis.service.port` | Redis service port | `6379` |
| `redis.resources.limits.cpu` | Redis CPU limit | `"500m"` |
| `redis.resources.limits.memory` | Redis memory limit | `"512Mi"` |

### Monitoring Configuration
| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `monitoring.enabled` | Enable monitoring stack deployment | `true` |
| `monitoring.prometheus.enabled` | Enable Prometheus deployment | `true` |
| `monitoring.grafana.enabled` | Enable Grafana deployment | `true` |
| `monitoring.loki.enabled` | Enable Loki deployment | `true` |

## Accessing Services

After deployment, you can access the services using port forwarding:

```bash
# Access MCP Server
kubectl port-forward svc/cloudcurio-mcp-server 8000:8000

# Access Configuration Editor
kubectl port-forward svc/cloudcurio-config-editor 8081:8081

# Access Ollama
kubectl port-forward svc/ollama-service 11434:11434

# Access LiteLLM
kubectl port-forward svc/litellm-service 4000:4000

# Access Open WebUI
kubectl port-forward svc/open-webui-service 3000:3000

# Access PostgreSQL
kubectl port-forward svc/postgres-service 5432:5432

# Access Redis
kubectl port-forward svc/redis-service 6379:6379

# Access Prometheus
kubectl port-forward svc/prometheus-service -n cloudcurio-monitoring 9090:9090

# Access Grafana
kubectl port-forward svc/grafana-service -n cloudcurio-monitoring 3001:3000

# Access Loki
kubectl port-forward svc/loki-service -n cloudcurio-monitoring 3100:3100
```

## Ingress Configuration

To expose services externally, enable ingress in your values file:

```yaml
ingress:
  enabled: true
  className: "nginx"
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
  hosts:
    - host: cloudcurio.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: cloudcurio-tls
      hosts:
        - cloudcurio.example.com
```

## Scaling Components

To scale components, modify the replica counts in your values file or use Helm upgrade:

```bash
# Scale MCP Server to 3 replicas
helm upgrade cloudcurio cloudcurio/cloudcurio --set mcpServer.replicaCount=3

# Scale Configuration Editor to 2 replicas
helm upgrade cloudcurio cloudcurio/cloudcurio --set configEditor.replicaCount=2

# Scale Ollama to 2 replicas
helm upgrade cloudcurio cloudcurio/cloudcurio --set ollama.replicaCount=2
```

## Updating CloudCurio

To update CloudCurio to a new version:

```bash
# Update Helm repositories
helm repo update

# Upgrade the release
helm upgrade cloudcurio cloudcurio/cloudcurio --version 2.3.0
```

To upgrade with new values:

```bash
helm upgrade cloudcurio cloudcurio/cloudcurio --values my-values.yaml
```

## Uninstalling CloudCurio

To uninstall/delete the release:

```bash
helm uninstall cloudcurio
```

To completely remove all resources including the namespace:

```bash
helm uninstall cloudcurio
kubectl delete namespace cloudcurio
kubectl delete namespace cloudcurio-monitoring
```

## Troubleshooting

### Common Issues

1. **Insufficient Resources**: Increase resource limits in values.yaml
2. **GPU Not Available**: Check NVidia drivers and device plugin
3. **Persistence Issues**: Ensure StorageClass is properly configured
4. **Network Connectivity**: Check service selectors and network policies
5. **Authentication Failures**: Verify secrets and credentials

### Debugging Commands

```bash
# Check Helm release status
helm status cloudcurio

# Check pod status
kubectl get pods -n cloudcurio

# Check service status
kubectl get services -n cloudcurio

# Check logs
kubectl logs -n cloudcurio deployment/cloudcurio-mcp-server

# Describe resources
kubectl describe -n cloudcurio deployment/cloudcurio-mcp-server

# Check events
kubectl get events -n cloudcurio

# Check configmaps
kubectl get configmaps -n cloudcurio

# Check secrets
kubectl get secrets -n cloudcurio
```

## Customization Examples

### Example 1: Custom Resource Allocation
```yaml
# custom-resources.yaml
mcpServer:
  resources:
    limits:
      cpu: 2000m
      memory: 2Gi
    requests:
      cpu: 1000m
      memory: 1Gi

configEditor:
  resources:
    limits:
      cpu: 1000m
      memory: 1Gi
    requests:
      cpu: 500m
      memory: 512Mi

ollama:
  resources:
    limits:
      cpu: 4000m
      memory: 8Gi
      nvidia.com/gpu: 2
    requests:
      cpu: 2000m
      memory: 4Gi
      nvidia.com/gpu: 1
```

### Example 2: Custom Ingress Configuration
```yaml
# custom-ingress.yaml
ingress:
  enabled: true
  className: "traefik"
  annotations:
    traefik.ingress.kubernetes.io/router.entrypoints: websecure
    traefik.ingress.kubernetes.io/router.tls: "true"
  hosts:
    - host: cloudcurio.mydomain.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: cloudcurio-tls
      hosts:
        - cloudcurio.mydomain.com
```

### Example 3: Custom Storage Configuration
```yaml
# custom-storage.yaml
postgresql:
  primary:
    persistence:
      enabled: true
      size: 100Gi
      storageClass: fast-ssd

ollama:
  persistence:
    enabled: true
    size: 200Gi
    storageClass: fast-ssd

openWebUI:
  persistence:
    enabled: true
    size: 50Gi
    storageClass: standard
```

## Security Considerations

### Credential Management
- Use Kubernetes secrets for sensitive data
- Enable RBAC for access control
- Use network policies for service communication
- Regularly update container images
- Scan images for vulnerabilities
- Use secure container registries

### Network Security
- Implement pod security policies
- Enable audit logging
- Use mutual TLS for service communication
- Restrict ingress/egress traffic
- Implement service mesh for advanced security

### Data Protection
- Encrypt data at rest
- Use secure backup procedures
- Implement disaster recovery plans
- Regularly rotate credentials
- Monitor for unauthorized access

## Monitoring and Observability

The Helm chart includes monitoring stack deployment with:
- Prometheus for metrics collection
- Grafana for visualization
- Loki for log aggregation

### Accessing Monitoring Tools
```bash
# Access Prometheus
kubectl port-forward svc/prometheus-service -n cloudcurio-monitoring 9090:9090

# Access Grafana
kubectl port-forward svc/grafana-service -n cloudcurio-monitoring 3001:3000

# Access Loki
kubectl port-forward svc/loki-service -n cloudcurio-monitoring 3100:3100
```

### Default Monitoring Configuration
- 15-day data retention for Prometheus
- 30-day data retention for Loki
- Default dashboards for all CloudCurio components
- Alerting rules for critical metrics

## Contributing

See the [CONTRIBUTING.md](../../../CONTRIBUTING.md) file for guidelines on how to contribute to this Helm chart.

## License

This Helm chart is licensed under the MIT License - see the [LICENSE](../../../LICENSE) file for details.