# CloudCurio Helm Chart

This Helm chart deploys the complete CloudCurio AI-Powered Development Platform to Kubernetes.

## Prerequisites

- Kubernetes 1.20+
- Helm 3.0+
- Access to a container registry (Docker Hub by default)
- NVidia GPU drivers (for Ollama with GPU acceleration)

## Installing the Chart

To install the chart with the release name `cloudcurio`:

```bash
helm repo add cloudcurio https://cbwinslow.github.io/cloudcurio-helm-charts/
helm install cloudcurio cloudcurio/cloudcurio
```

Or to install from the local chart:

```bash
helm install cloudcurio ./kubernetes/helm/cloudcurio
```

## Configuration

The following table lists the configurable parameters of the CloudCurio chart and their default values.

### Global Configuration

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `global.imageRegistry` | Global Docker image registry | `""` |
| `global.imageTag` | Global Docker image tag | `"2.2.0"` |
| `global.imagePullSecrets` | Global Docker registry secret names as an array | `[]` |
| `global.storageClass` | Global storage class for dynamic provisioning | `""` |
| `global.namespace` | Namespace to deploy CloudCurio to | `"cloudcurio"` |

### MCP Server Configuration

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `mcpServer.enabled` | Enable MCP Server deployment | `true` |
| `mcpServer.replicaCount` | Number of MCP Server replicas | `1` |
| `mcpServer.image.repository` | MCP Server image repository | `"cbwinslow/cloudcurio-mcp"` |
| `mcpServer.image.tag` | MCP Server image tag | `""` |
| `mcpServer.image.pullPolicy` | MCP Server image pull policy | `"IfNotPresent"` |
| `mcpServer.service.type` | MCP Server service type | `"ClusterIP"` |
| `mcpServer.service.port` | MCP Server service port | `8000` |
| `mcpServer.resources.limits.cpu` | MCP Server CPU limit | `"1000m"` |
| `mcpServer.resources.limits.memory` | MCP Server memory limit | `"1Gi"` |
| `mcpServer.resources.requests.cpu` | MCP Server CPU request | `"500m"` |
| `mcpServer.resources.requests.memory` | MCP Server memory request | `"512Mi"` |
| `mcpServer.autoscaling.enabled` | Enable MCP Server autoscaling | `true` |
| `mcpServer.autoscaling.minReplicas` | Minimum MCP Server replicas | `1` |
| `mcpServer.autoscaling.maxReplicas` | Maximum MCP Server replicas | `10` |
| `mcpServer.autoscaling.targetCPUUtilizationPercentage` | Target CPU utilization percentage | `70` |
| `mcpServer.autoscaling.targetMemoryUtilizationPercentage` | Target memory utilization percentage | `80` |

### Configuration Editor Configuration

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `configEditor.enabled` | Enable Configuration Editor deployment | `true` |
| `configEditor.replicaCount` | Number of Configuration Editor replicas | `1` |
| `configEditor.image.repository` | Configuration Editor image repository | `"cbwinslow/cloudcurio-config-editor"` |
| `configEditor.image.tag` | Configuration Editor image tag | `""` |
| `configEditor.image.pullPolicy` | Configuration Editor image pull policy | `"IfNotPresent"` |
| `configEditor.service.type` | Configuration Editor service type | `"ClusterIP"` |
| `configEditor.service.port` | Configuration Editor service port | `8081` |
| `configEditor.resources.limits.cpu` | Configuration Editor CPU limit | `"500m"` |
| `configEditor.resources.limits.memory` | Configuration Editor memory limit | `"512Mi"` |
| `configEditor.resources.requests.cpu` | Configuration Editor CPU request | `"250m"` |
| `configEditor.resources.requests.memory` | Configuration Editor memory request | `"256Mi"` |
| `configEditor.autoscaling.enabled` | Enable Configuration Editor autoscaling | `true` |
| `configEditor.autoscaling.minReplicas` | Minimum Configuration Editor replicas | `1` |
| `configEditor.autoscaling.maxReplicas` | Maximum Configuration Editor replicas | `5` |
| `configEditor.autoscaling.targetCPUUtilizationPercentage` | Target CPU utilization percentage | `70` |
| `configEditor.autoscaling.targetMemoryUtilizationPercentage` | Target memory utilization percentage | `80` |

### Ollama Configuration

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `ollama.enabled` | Enable Ollama deployment | `true` |
| `ollama.replicaCount` | Number of Ollama replicas | `1` |
| `ollama.image.repository` | Ollama image repository | `"ollama/ollama"` |
| `ollama.image.tag` | Ollama image tag | `"latest"` |
| `ollama.image.pullPolicy` | Ollama image pull policy | `"IfNotPresent"` |
| `ollama.service.type` | Ollama service type | `"ClusterIP"` |
| `ollama.service.port` | Ollama service port | `11434` |
| `ollama.resources.limits.cpu` | Ollama CPU limit | `"2000m"` |
| `ollama.resources.limits.memory` | Ollama memory limit | `"4Gi"` |
| `ollama.resources.limits.nvidia.com/gpu` | Ollama GPU limit | `"1"` |
| `ollama.resources.requests.cpu` | Ollama CPU request | `"1000m"` |
| `ollama.resources.requests.memory` | Ollama memory request | `"2Gi"` |
| `ollama.resources.requests.nvidia.com/gpu` | Ollama GPU request | `"1"` |
| `ollama.nodeSelector.nvidia.com/gpu.present` | Node selector for GPU nodes | `"true"` |
| `ollama.persistence.enabled` | Enable Ollama persistence | `true` |
| `ollama.persistence.size` | Ollama persistence size | `"50Gi"` |
| `ollama.persistence.accessModes` | Ollama persistence access modes | `["ReadWriteOnce"]` |

### LiteLLM Configuration

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `litellm.enabled` | Enable LiteLLM deployment | `true` |
| `litellm.replicaCount` | Number of LiteLLM replicas | `1` |
| `litellm.image.repository` | LiteLLM image repository | `"ghcr.io/berriai/litellm"` |
| `litellm.image.tag` | LiteLLM image tag | `"main-latest"` |
| `litellm.image.pullPolicy` | LiteLLM image pull policy | `"IfNotPresent"` |
| `litellm.service.type` | LiteLLM service type | `"ClusterIP"` |
| `litellm.service.port` | LiteLLM service port | `4000` |
| `litellm.resources.limits.cpu` | LiteLLM CPU limit | `"1000m"` |
| `litellm.resources.limits.memory` | LiteLLM memory limit | `"1Gi"` |
| `litellm.resources.requests.cpu` | LiteLLM CPU request | `"500m"` |
| `litellm.resources.requests.memory` | LiteLLM memory request | `"512Mi"` |
| `litellm.autoscaling.enabled` | Enable LiteLLM autoscaling | `true` |
| `litellm.autoscaling.minReplicas` | Minimum LiteLLM replicas | `1` |
| `litellm.autoscaling.maxReplicas` | Maximum LiteLLM replicas | `5` |
| `litellm.autoscaling.targetCPUUtilizationPercentage` | Target CPU utilization percentage | `70` |
| `litellm.autoscaling.targetMemoryUtilizationPercentage` | Target memory utilization percentage | `80` |

### Open WebUI Configuration

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `openWebUI.enabled` | Enable Open WebUI deployment | `true` |
| `openWebUI.replicaCount` | Number of Open WebUI replicas | `1` |
| `openWebUI.image.repository` | Open WebUI image repository | `"ghcr.io/open-webui/open-webui"` |
| `openWebUI.image.tag` | Open WebUI image tag | `"main"` |
| `openWebUI.image.pullPolicy` | Open WebUI image pull policy | `"IfNotPresent"` |
| `openWebUI.service.type` | Open WebUI service type | `"ClusterIP"` |
| `openWebUI.service.port` | Open WebUI service port | `3000` |
| `openWebUI.resources.limits.cpu` | Open WebUI CPU limit | `"1000m"` |
| `openWebUI.resources.limits.memory` | Open WebUI memory limit | `"1Gi"` |
| `openWebUI.resources.requests.cpu` | Open WebUI CPU request | `"500m"` |
| `openWebUI.resources.requests.memory` | Open WebUI memory request | `"512Mi"` |
| `openWebUI.autoscaling.enabled` | Enable Open WebUI autoscaling | `true` |
| `openWebUI.autoscaling.minReplicas` | Minimum Open WebUI replicas | `1` |
| `openWebUI.autoscaling.maxReplicas` | Maximum Open WebUI replicas | `3` |
| `openWebUI.autoscaling.targetCPUUtilizationPercentage` | Target CPU utilization percentage | `70` |
| `openWebUI.autoscaling.targetMemoryUtilizationPercentage` | Target memory utilization percentage | `80` |
| `openWebUI.persistence.enabled` | Enable Open WebUI persistence | `true` |
| `openWebUI.persistence.size` | Open WebUI persistence size | `"10Gi"` |
| `openWebUI.persistence.accessModes` | Open WebUI persistence access modes | `["ReadWriteOnce"]` |

### PostgreSQL Configuration

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `postgresql.enabled` | Enable PostgreSQL deployment | `true` |
| `postgresql.replicaCount` | Number of PostgreSQL replicas | `1` |
| `postgresql.image.repository` | PostgreSQL image repository | `"postgres"` |
| `postgresql.image.tag` | PostgreSQL image tag | `"15"` |
| `postgresql.image.pullPolicy` | PostgreSQL image pull policy | `"IfNotPresent"` |
| `postgresql.service.type` | PostgreSQL service type | `"ClusterIP"` |
| `postgresql.service.port` | PostgreSQL service port | `5432` |
| `postgresql.auth.username` | PostgreSQL username | `"postgres"` |
| `postgresql.auth.password` | PostgreSQL password | `"password"` |
| `postgresql.auth.database` | PostgreSQL database name | `"cloudcurio"` |
| `postgresql.resources.limits.cpu` | PostgreSQL CPU limit | `"1000m"` |
| `postgresql.resources.limits.memory` | PostgreSQL memory limit | `"1Gi"` |
| `postgresql.resources.requests.cpu` | PostgreSQL CPU request | `"500m"` |
| `postgresql.resources.requests.memory` | PostgreSQL memory request | `"512Mi"` |
| `postgresql.primary.persistence.enabled` | Enable PostgreSQL persistence | `true` |
| `postgresql.primary.persistence.size` | PostgreSQL persistence size | `"20Gi"` |
| `postgresql.primary.persistence.accessModes` | PostgreSQL persistence access modes | `["ReadWriteOnce"]` |

### Redis Configuration

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `redis.enabled` | Enable Redis deployment | `true` |
| `redis.replicaCount` | Number of Redis replicas | `1` |
| `redis.image.repository` | Redis image repository | `"redis"` |
| `redis.image.tag` | Redis image tag | `"7-alpine"` |
| `redis.image.pullPolicy` | Redis image pull policy | `"IfNotPresent"` |
| `redis.service.type` | Redis service type | `"ClusterIP"` |
| `redis.service.port` | Redis service port | `6379` |
| `redis.resources.limits.cpu` | Redis CPU limit | `"500m"` |
| `redis.resources.limits.memory` | Redis memory limit | `"512Mi"` |
| `redis.resources.requests.cpu` | Redis CPU request | `"250m"` |
| `redis.resources.requests.memory` | Redis memory request | `"256Mi"` |
| `redis.master.persistence.enabled` | Enable Redis persistence | `true` |
| `redis.master.persistence.size` | Redis persistence size | `"10Gi"` |
| `redis.master.persistence.accessModes` | Redis persistence access modes | `["ReadWriteOnce"]` |

### Monitoring Configuration

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `monitoring.enabled` | Enable monitoring stack deployment | `true` |
| `monitoring.prometheus.enabled` | Enable Prometheus deployment | `true` |
| `monitoring.grafana.enabled` | Enable Grafana deployment | `true` |
| `monitoring.loki.enabled` | Enable Loki deployment | `true` |

## Customizing the Chart

### Override Values

You can override the default values by creating a `values.yaml` file:

```yaml
# custom-values.yaml
mcpServer:
  replicaCount: 3
  resources:
    limits:
      cpu: 2000m
      memory: 2Gi
    requests:
      cpu: 1000m
      memory: 1Gi

configEditor:
  replicaCount: 2
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

Then install with your custom values:

```bash
helm install cloudcurio ./kubernetes/helm/cloudcurio -f custom-values.yaml
```

### Environment-Specific Values

You can create environment-specific values files:

```bash
# Development environment
helm install cloudcurio-dev ./kubernetes/helm/cloudcurio -f values-dev.yaml

# Staging environment
helm install cloudcurio-staging ./kubernetes/helm/cloudcurio -f values-staging.yaml

# Production environment
helm install cloudcurio-prod ./kubernetes/helm/cloudcurio -f values-prod.yaml
```

## Upgrading the Chart

To upgrade the chart:

```bash
helm upgrade cloudcurio ./kubernetes/helm/cloudcurio
```

To upgrade with new values:

```bash
helm upgrade cloudcurio ./kubernetes/helm/cloudcurio -f custom-values.yaml
```

## Uninstalling the Chart

To uninstall/delete the release:

```bash
helm uninstall cloudcurio
```

## Accessing Services

After deploying, you can access the services using port forwarding:

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

To expose services externally, you can enable ingress:

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

## Persistence

The chart uses PersistentVolumes for data persistence. Make sure your cluster has a default StorageClass configured, or specify a StorageClass in your values.

## GPU Acceleration

For Ollama with GPU acceleration, ensure your cluster has NVidia GPU drivers installed and the appropriate device plugin running.

## Monitoring and Observability

The chart includes monitoring stack deployment with:
- Prometheus for metrics collection
- Grafana for visualization
- Loki for log aggregation

## Security Considerations

- Use Kubernetes secrets for sensitive data
- Enable RBAC for access control
- Use network policies for service communication
- Regularly update container images
- Scan images for vulnerabilities
- Use secure container registries
- Implement pod security policies
- Enable audit logging

## Troubleshooting

### Common Issues

1. **Insufficient Resources**: Increase resource limits in values.yaml
2. **GPU Not Available**: Check NVidia drivers and device plugin
3. **Persistence Issues**: Ensure StorageClass is properly configured
4. **Network Connectivity**: Check service selectors and network policies
5. **Authentication Failures**: Verify secrets and credentials

### Debugging Commands

```bash
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

## Contributing

See the [CONTRIBUTING.md](../../../CONTRIBUTING.md) file for guidelines on how to contribute to this Helm chart.

## License

This Helm chart is licensed under the MIT License - see the [LICENSE](../../../LICENSE) file for details.