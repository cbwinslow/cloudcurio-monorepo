# OSINT Platform

A comprehensive, containerized OSINT (Open Source Intelligence) platform that integrates multiple tools for intelligence gathering, analysis, and visualization.

## Overview

This platform combines 20+ OSINT tools in a single, easy-to-deploy Docker environment. It includes tools for data collection, processing, storage, analysis, and visualization, all connected through a reverse proxy and API gateway.

## Features

- **Data Collection**: SearXNG, Archon, BeEF, n8n
- **Processing & Analysis**: LocalAI, OpenWebUI, LocalRecall, Flowise, MCP Server
- **Storage & Database**: Supabase, Neo4j, Bitwarden
- **Monitoring & Logging**: Prometheus, Grafana, Netdata, Loki, Fluentd, Sentry
- **Messaging**: RabbitMQ
- **Security**: Kong API Gateway, Traefik Reverse Proxy
- **AI Agents**: Pydantic AI agents with tools
- **Web Interface**: Next.js configuration interface

## Architecture

The platform follows a microservices architecture with the following layers:

1. **Networking Layer**: Traefik Reverse Proxy for SSL termination and routing
2. **API Management Layer**: Kong API Gateway for API management
3. **Data Collection Layer**: Tools for gathering intelligence from various sources
4. **Processing & Analysis Layer**: AI and workflow tools for data processing
5. **Storage & Database Layer**: Databases for storing collected intelligence
6. **Monitoring & Logging Layer**: Tools for monitoring and logging
7. **Messaging Layer**: RabbitMQ for distributed task processing

## Prerequisites

- Docker
- Docker Compose
- Git (optional, for updates)

## Quick Start

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd osint-platform
   ```

2. **Run the setup script**:
   ```bash
   ./scripts/setup-platform.sh
   ```

3. **Start the platform**:
   ```bash
   ./scripts/manage-platform.sh start
   ```

4. **Access the platform**:
   - Main interface: http://localhost
   - Traefik Dashboard: http://localhost:8080
   - Individual services through their respective subdomains

## Services Included

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

## Management Commands

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

## Configuration

The main configuration file is located at `config/osint-platform-config.yaml`. This file contains all settings and secrets for the platform.

## Security Considerations

1. **Change default passwords** in the configuration file
2. **Enable SSL** by setting up proper domain names and certificates
3. **Restrict access** to sensitive services
4. **Regular updates** of all services
5. **Monitor logs** for suspicious activity

## Backup and Recovery

The platform includes automated backup scripts that can backup:
- Database dumps (Supabase, Neo4j)
- Configuration files
- Service data

Backups are stored in the `backups/` directory by default.

## Customization

You can customize the platform by:
1. Modifying the `docker-compose.yml` file
2. Updating service configurations in their respective directories
3. Adding new services to the stack
4. Modifying the management scripts

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue on the GitHub repository.