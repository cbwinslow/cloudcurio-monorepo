# Getting Started with OSINT Platform

This guide will help you quickly get started with the OSINT Platform.

## Prerequisites

Before you begin, ensure you have the following installed:
- Docker
- Docker Compose
- Git (optional, for updates)

## Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd osint-platform
```

### 2. Run the Starter Script

```bash
./start-osint-platform.sh
```

You'll see a menu like this:

```
==========================================
     OSINT Platform - Starter Script      
==========================================

Main Menu:
  1. Install OSINT Platform
  2. Start OSINT Platform
  3. Stop OSINT Platform
  4. View Platform Status
  5. View Platform Logs
  6. Update OSINT Platform
  7. Backup OSINT Platform
  8. Restore OSINT Platform
  9. Show Platform Information
  10. Exit

Select an option (1-10): 
```

### 3. Install the Platform

Select option 1 to install the platform. This will:
- Check prerequisites
- Create directory structure
- Pull Docker images
- Initialize databases

### 4. Start the Platform

Select option 2 to start the platform. This will:
- Start all Docker containers
- Initialize services
- Display access information

Once started, you can access:
- Main interface: http://localhost
- Traefik Dashboard: http://localhost:8080
- Portainer: http://localhost:9001
- Grafana: http://localhost:3001
- Prometheus: http://localhost:9090

### 5. Explore the Platform

Navigate to http://localhost to access the main web interface. From here you can:
- Manage all integrated tools
- Configure platform settings
- View monitoring dashboards
- Access AI agents
- Manage containerized OSINT tools

## Key Services and Their URLs

| Service | URL | Description |
|---------|-----|-------------|
| Main Interface | http://localhost | Central management interface |
| Traefik Dashboard | http://localhost:8080 | Reverse proxy management |
| Portainer | http://localhost:9001 | Container management |
| Grafana | http://localhost:3001 | Monitoring dashboards |
| Prometheus | http://localhost:9090 | Metrics collection |
| Supabase | http://localhost:5432 | PostgreSQL database |
| Neo4j | http://localhost:7474 | Graph database |
| Bitwarden | http://localhost:8083 | Secrets management |
| SearXNG | http://localhost:8084 | Metasearch engine |
| BeEF | http://localhost:3002 | Browser exploitation |
| n8n | http://localhost:5678 | Workflow automation |
| LocalAI | http://localhost:8081 | Local AI models |
| Ollama | http://localhost:11434 | LLM inference |
| OpenWebUI | http://localhost:3000 | AI interface |
| LocalRecall | http://localhost:8082 | Semantic search |
| Flowise | http://localhost:3003 | AI workflow builder |
| MCP Server | http://localhost:3004 | Model Context Protocol |
| RabbitMQ | http://localhost:15672 | Message broker |
| Netdata | http://localhost:19999 | System monitoring |
| Loki | http://localhost:3100 | Log aggregation |
| Sentry | http://localhost:9000 | Error tracking |
| Archon | http://localhost:8085 | OSINT resource directory |
| Kali OSINT | http://localhost:8086 | Kali Linux tools |
| BlackArch OSINT | http://localhost:8087 | BlackArch Linux tools |
| BlackArch MCP | http://localhost:3006 | BlackArch MCP server |

## Basic Operations

### Managing the Platform

Use the starter script for common operations:

```bash
# Start the platform
./start-osint-platform.sh
# Select option 2

# Stop the platform
./start-osint-platform.sh
# Select option 3

# View logs
./start-osint-platform.sh
# Select option 5

# Update the platform
./start-osint-platform.sh
# Select option 6

# Backup the platform
./start-osint-platform.sh
# Select option 7

# Restore from backup
./start-osint-platform.sh
# Select option 8
```

### Using OSINT Tools

1. **SearXNG**: Access at http://localhost:8084 for anonymous web searches
2. **BeEF**: Access at http://localhost:3002 for browser exploitation testing
3. **Kali OSINT**: Access at http://localhost:8086 for Kali Linux tools
4. **BlackArch OSINT**: Access at http://localhost:8087 for BlackArch Linux tools
5. **LocalAI/Ollama**: Use through OpenWebUI at http://localhost:3000 or directly via API

### Working with AI Agents

The platform includes Pydantic AI agents with access to all tools:

1. Access the AI agents through the web interface
2. Configure agent tools and permissions
3. Run automated OSINT tasks
4. Monitor agent activities and results

### Monitoring and Logging

1. **Grafana**: Access at http://localhost:3001 for dashboards and metrics
2. **Prometheus**: Access at http://localhost:9090 for metrics collection
3. **Netdata**: Access at http://localhost:19999 for real-time system monitoring
4. **Loki**: Access logs through Grafana or directly via API

## Security Considerations

1. **Change Default Passwords**: Update default credentials in configuration files
2. **Enable SSL**: Configure SSL certificates for production use
3. **Restrict Access**: Limit access to sensitive services
4. **Regular Updates**: Keep all services updated with security patches
5. **Monitor Logs**: Regularly review logs for suspicious activity
6. **Use Bitwarden**: Store secrets securely with Bitwarden

## Troubleshooting

### Common Issues

1. **Port Conflicts**: Ensure no other services are using the same ports
2. **Docker Permissions**: Ensure the user has permission to run Docker commands
3. **Configuration Errors**: Check that all configuration files are properly formatted
4. **Network Issues**: Verify that services can communicate with each other

### Checking Service Status

```bash
# View all running services
docker-compose ps

# View logs for a specific service
docker-compose logs <service_name>

# Restart a specific service
docker-compose restart <service_name>
```

### Getting Help

For detailed documentation, see:
- [Full Documentation](OSINT_PLATFORM_DOCUMENTATION.md)
- [Configuration Guide](config/master-config.yaml)
- [Service Configuration](config/services/)

For support, please open an issue on the GitHub repository.