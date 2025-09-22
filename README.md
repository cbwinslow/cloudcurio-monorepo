# OSINT Platform

A comprehensive, containerized OSINT (Open Source Intelligence) platform that integrates 20+ tools for intelligence gathering, analysis, and visualization.

## Overview

The OSINT Platform is a powerful solution that combines multiple OSINT tools into a single, easy-to-deploy platform. Built with Docker and Docker Compose, it provides a modular architecture that allows for easy deployment and scaling.

![OSINT Platform Architecture](docs/architecture.png)

## Features

- **20+ Integrated Tools**: Combines popular OSINT tools in a single platform
- **Containerized Architecture**: Uses Docker for isolation and portability
- **Microservices Design**: Each service runs in its own container
- **Centralized Management**: Single interface for managing all services
- **Extensible Plugin System**: Allows for custom functionality
- **AI Integration**: Includes LLMs for advanced analysis
- **Security Focused**: Built-in authentication, encryption, and monitoring
- **DevOps Ready**: CI/CD pipelines and automated deployment

## Tools Included

### Data Collection
- **SearXNG**: Metasearch engine for anonymous reconnaissance
- **Archon**: OSINT resource directory
- **BeEF**: Browser exploitation framework
- **n8n**: Workflow automation platform

### Processing & Analysis
- **LocalAI**: Local AI models for NLP and analysis
- **Ollama**: LLM inference engine
- **OpenWebUI**: Interface for interacting with local AI models
- **LocalRecall**: Semantic search and knowledge base management
- **Flowise**: Visual AI workflow builder
- **MCP Server**: Model Context Protocol server

### Storage & Databases
- **Supabase**: PostgreSQL-based database with real-time capabilities
- **Neo4j**: Graph database for relationship analysis
- **Bitwarden**: Secrets management system

### Monitoring & Logging
- **Prometheus**: Time-series database for metrics collection
- **Grafana**: Data visualization and dashboarding
- **Netdata**: Real-time system monitoring
- **Loki**: Log aggregation system
- **Fluentd**: Unified logging layer
- **Sentry**: Error tracking and performance monitoring

### Messaging
- **RabbitMQ**: Message broker for distributed task processing

### Web Interface
- **Next.js Frontend**: Modern web interface for platform management
- **Pydantic AI Agents**: Intelligent agents with access to all platform tools

### Container Management
- **Portainer**: Container management UI
- **Podman**: Container engine

### OSINT Tools
- **Kali OSINT Container**: Container with Kali Linux OSINT tools
- **BlackArch OSINT Container**: Container with BlackArch Linux OSINT tools
- **BlackArch MCP Server**: MCP server with BlackArch Linux tools

## Architecture

The platform follows a layered microservices architecture with the following components:

1. **Reverse Proxy Layer**: Traefik for SSL termination and routing
2. **API Gateway Layer**: Kong for API management and security
3. **Data Collection Layer**: Tools for gathering intelligence from various sources
4. **Processing & Analysis Layer**: AI and workflow tools for data processing
5. **Storage & Database Layer**: Databases for storing collected intelligence
6. **Monitoring & Logging Layer**: Tools for monitoring and logging
7. **Messaging Layer**: RabbitMQ for distributed task processing
8. **Web Interface Layer**: Next.js interface for configuration and management
9. **AI Agents Layer**: Pydantic AI agents with tools for automation
10. **Container Management Layer**: Portainer and Podman for container management
11. **OSINT Tools Layer**: Specialized containers with Kali Linux and BlackArch tools

## Installation

### Prerequisites

- Docker
- Docker Compose
- Git (optional, for updates)

### Quick Start

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd osint-platform
   ```

2. Run the setup script:
   ```bash
   ./start-osint-platform.sh
   ```

3. Select option 1 to install the platform

4. Select option 2 to start the platform

5. Access the platform at http://localhost

### Manual Installation

1. Create directory structure:
   ```bash
   mkdir -p data/{supabase,neo4j,bitwarden,n8n,localai,openwebui,localrecall,flowise,rabbitmq,prometheus,grafana,netdata,sentry,portainer,ollama,kali,blackarch,mcp}
   ```

2. Start the platform:
   ```bash
   docker-compose up -d
   ```

3. Access the platform at http://localhost

## Usage

### Starting the Platform

```bash
./start-osint-platform.sh
# Select option 2: Start OSINT Platform
```

### Stopping the Platform

```bash
./start-osint-platform.sh
# Select option 3: Stop OSINT Platform
```

### Viewing Logs

```bash
./start-osint-platform.sh
# Select option 5: View Platform Logs
```

### Creating Backups

```bash
./start-osint-platform.sh
# Select option 7: Backup OSINT Platform
```

### Restoring from Backup

```bash
./start-osint-platform.sh
# Select option 8: Restore OSINT Platform
```

## Configuration

### Master Configuration

The platform uses a master configuration file at `config/master-config.yaml` that contains all settings for all services.

### Service-Specific Configuration

Each service has its own configuration directory under `config/services/<service-name>/`.

### Environment Variables

Sensitive information should be stored as environment variables rather than in configuration files.

### Secrets Management

The platform uses Bitwarden for secrets management. Configure Bitwarden with your credentials and API keys.

## Security

### Authentication

The platform uses Bitwarden for secrets management and authentication.

### Encryption

All communications are encrypted using SSL/TLS with Let's Encrypt certificates.

### Network Security

The platform uses Docker networks for isolation and Traefik for access control.

### Monitoring

The platform includes comprehensive monitoring with Prometheus, Grafana, Netdata, and Loki.

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

## Documentation

For detailed documentation, see:
- [Architecture Documentation](OSINT_PLATFORM_DOCUMENTATION.md)
- [Configuration Guide](config/master-config.yaml)
- [Service Configuration](config/services/)
- [Deployment Guide](deployment/)
- [API Documentation](docs/api/)