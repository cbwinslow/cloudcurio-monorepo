# OSINT Platform - Complete Guide

## Overview

This document provides a comprehensive guide to using and extending the OSINT (Open Source Intelligence) Platform, a containerized solution that integrates 20+ tools for intelligence gathering, analysis, and visualization.

## Architecture Summary

The platform follows a microservices architecture with the following key components:

1. **Networking Layer**: Traefik Reverse Proxy for SSL termination and routing
2. **API Management Layer**: Kong API Gateway for API management
3. **Data Collection Layer**: Tools for gathering intelligence from various sources
4. **Processing & Analysis Layer**: AI and workflow tools for data processing
5. **Storage & Database Layer**: Databases for storing collected intelligence
6. **Monitoring & Logging Layer**: Tools for monitoring and logging
7. **Messaging Layer**: RabbitMQ for distributed task processing
8. **AI Agents Layer**: Pydantic AI agents with tools for automated tasks
9. **Web Interface Layer**: Next.js interface for configuration and management

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- Git (optional, for updates)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd osint-platform
   ```

2. Run the setup script:
   ```bash
   ./scripts/setup-platform.sh
   ```

3. Start the platform:
   ```bash
   ./scripts/manage-platform.sh start
   ```

4. Access the platform:
   - Main interface: http://localhost
   - Traefik Dashboard: http://localhost:8080
   - Individual services through their respective subdomains

## Services Overview

The platform includes the following services:

| Service | Port | Description |
|---------|------|-------------|
| Traefik | 80/443, 8080 | Reverse Proxy with SSL |
| Kong | 8000, 8001, 8443, 8444 | API Gateway |
| Supabase | 5432 | PostgreSQL database |
| Neo4j | 7474, 7687 | Graph database |
| Bitwarden | 8083 | Secrets management |
| SearXNG | 8084 | Metasearch engine |
| BeEF | 3002 | Browser exploitation framework |
| n8n | 5678 | Workflow automation |
| LocalAI | 8081 | Local AI models |
| OpenWebUI | 3000 | AI interface |
| LocalRecall | 8082 | Semantic search |
| Flowise | 3003 | AI workflow builder |
| MCP Server | 3004 | Model Context Protocol |
| RabbitMQ | 5672, 15672 | Message broker |
| Prometheus | 9090 | Metrics collection |
| Grafana | 3001 | Data visualization |
| Netdata | 19999 | System monitoring |
| Loki | 3100 | Log aggregation |
| Fluentd | 24224 | Log collection |
| Sentry | 9000 | Error tracking |
| Archon | 8085 | OSINT resource directory |
| Web Interface | 3005 | Configuration UI |
| AI Agents | N/A | Automated intelligence tasks |

## Configuration

### Centralized Configuration

The platform uses a centralized configuration system located at `config/osint-platform-config.yaml`. This file contains all settings and secrets for the platform.

### Environment Variables

Sensitive information should be stored as environment variables rather than in configuration files. The platform supports loading configuration from environment variables.

## Management Commands

The platform includes a management script (`scripts/manage-platform.sh`) with the following commands:

```bash
# Start the platform
./scripts/manage-platform.sh start

# Stop the platform
./scripts/manage-platform.sh stop

# Restart the platform
./scripts/manage-platform.sh restart

# View status
./scripts/manage-platform.sh status

# View logs (all or specific service)
./scripts/manage-platform.sh logs
./scripts/manage-platform.sh logs beef

# Create backup
./scripts/manage-platform.sh backup

# Restore from backup
./scripts/manage-platform.sh restore <backup_file>

# Update to latest versions
./scripts/manage-platform.sh update
```

## AI Agents

The platform includes Pydantic AI agents that can automate various OSINT tasks:

1. **Data Collector Agent**: Collects data from various sources
2. **Analyzer Agent**: Analyzes collected data for patterns
3. **Reporter Agent**: Generates reports from analyzed data
4. **Alerter Agent**: Sends alerts based on findings

### Customizing AI Agents

To customize AI agents:

1. Modify the configuration file at `ai-agents/config/agents.yaml`
2. Add new tools in `ai-agents/tools/impl.py`
3. Add new agent implementations in `ai-agents/agents/impl.py`

## Web Interface

The platform includes a Next.js web interface for configuration and management:

1. Access the interface at http://ui.osint.local or http://localhost:3005
2. Navigate between Dashboard, Configuration, and Services pages
3. Modify platform settings through the web interface

## Security Considerations

1. **Change default passwords** in the configuration file
2. **Enable SSL** by setting up proper domain names and certificates
3. **Restrict access** to sensitive services
4. **Regular updates** of all services
5. **Monitor logs** for suspicious activity
6. **Use Bitwarden** for secrets management

## Backup and Recovery

The platform includes automated backup scripts that can backup:
- Database dumps (Supabase, Neo4j)
- Configuration files
- Service data

Backups are stored in the `backups/` directory by default.

## Extending the Platform

### Adding New Services

To add new services to the platform:

1. Add the service definition to `docker-compose.yml`
2. Configure Traefik labels for routing
3. Add any necessary configuration files
4. Update the web interface to include the new service

### Adding New Tools to AI Agents

To add new tools to the AI agents:

1. Create a new tool class in `ai-agents/tools/impl.py`
2. Add the tool configuration to `ai-agents/config/agents.yaml`
3. Register the tool with the appropriate agents

### Adding New Agent Types

To add new agent types:

1. Create a new agent class in `ai-agents/agents/impl.py`
2. Add the agent configuration to `ai-agents/config/agents.yaml`
3. Register the agent in `ai-agents/main.py`

## CI/CD Pipeline

The platform includes GitHub Actions workflows for:

1. **Building and Pushing Docker Images**: Automatically builds and pushes Docker images to DockerHub
2. **Testing**: Runs tests for Python and Node.js components
3. **Deployment**: Deploys the platform to production environments

## Troubleshooting

### Common Issues

1. **Port Conflicts**: Ensure no other services are using the same ports
2. **Docker Permissions**: Ensure the user has permission to run Docker commands
3. **Configuration Errors**: Check that all configuration files are properly formatted
4. **Network Issues**: Verify that services can communicate with each other

### Logs

Check logs using the management script:
```bash
./scripts/manage-platform.sh logs
```

Or view logs for specific services:
```bash
./scripts/manage-platform.sh logs <service_name>
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue on the GitHub repository.