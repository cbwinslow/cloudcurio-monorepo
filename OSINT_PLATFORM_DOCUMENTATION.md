# OSINT Platform - Comprehensive Documentation

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Services](#services)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Usage](#usage)
7. [Security](#security)
8. [Monitoring](#monitoring)
9. [Troubleshooting](#troubleshooting)
10. [Contributing](#contributing)

## Overview

The OSINT Platform is a comprehensive, containerized solution that integrates 20+ OSINT tools for intelligence gathering, analysis, and visualization. Built with Docker and Docker Compose, it provides a modular architecture that allows for easy deployment and scaling.

### Key Features

- **20+ Integrated Tools**: Combines popular OSINT tools in a single platform
- **Containerized Architecture**: Uses Docker for isolation and portability
- **Microservices Design**: Each service runs in its own container
- **Centralized Management**: Single interface for managing all services
- **Extensible Plugin System**: Allows for custom functionality
- **AI Integration**: Includes LLMs for advanced analysis
- **Security Focused**: Built-in authentication, encryption, and monitoring
- **DevOps Ready**: CI/CD pipelines and automated deployment

## Architecture

The platform follows a layered microservices architecture:

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Internet/Web Browsers                        │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────────┐
│                         Reverse Proxy (Traefik)                     │
│                        SSL Termination & Routing                    │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────────┐
│                         API Gateway (Kong)                          │
│                       API Management & Security                     │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────────┐
│                            Load Balancer                            │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────────┐
│                                                                     │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐   │
│  │   Data     │  │Processing &│  │  Storage   │  │ Monitoring │   │
│  │Collection  │  │ Analysis   │  │  & DB      │  │  & Logging │   │
│  │            │  │            │  │            │  │            │   │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘   │
│        │                │               │               │         │
│        ▼                ▼               ▼               ▼         │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐   │
│  │ SearXNG    │  │ LocalAI    │  │ Supabase   │  │ Prometheus │   │
│  │ Archon     │  │ OpenWebUI  │  │ Neo4j      │  │ Grafana    │   │
│  │ BeEF       │  │ LocalRecall│  │ Bitwarden  │  │ Netdata    │   │
│  │ n8n        │  │ Flowise    │  │            │  │ Loki       │   │
│  │            │  │ MCP Server │  │            │  │ Fluentd    │   │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘   │
│        │                │               │               │         │
│        ▼                ▼               ▼               ▼         │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐   │
│  │ Messaging  │  │ Web UI     │  │ AI Agents  │  │ Additional │   │
│  │ (RabbitMQ) │  │            │  │            │  │ OSINT      │   │
│  └────────────┘  └────────────┘  └────────────┘  │ Tools      │   │
│                                                   │ (Kali,     │   │
│                                                   │ BlackArch) │   │
│                                                   └────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Services

### Core Infrastructure

1. **Traefik** - Reverse proxy with SSL termination and routing
2. **Kong** - API gateway for management and security
3. **RabbitMQ** - Message broker for distributed task processing
4. **Redis** - In-memory data structure store
5. **Sentry** - Error tracking and performance monitoring

### Database Layer

1. **Supabase** - PostgreSQL-based database with real-time capabilities
2. **Neo4j** - Graph database for relationship analysis
3. **Bitwarden** - Secrets management system

### Data Collection Layer

1. **SearXNG** - Metasearch engine for anonymous reconnaissance
2. **Archon** - OSINT resource directory
3. **BeEF** - Browser exploitation framework
4. **n8n** - Workflow automation platform

### Processing & Analysis Layer

1. **LocalAI** - Local AI models for NLP and analysis
2. **Ollama** - LLM inference engine
3. **OpenWebUI** - Interface for interacting with local AI models
4. **LocalRecall** - Semantic search and knowledge base management
5. **Flowise** - Visual AI workflow builder
6. **MCP Server** - Model Context Protocol server

### Monitoring & Logging Layer

1. **Prometheus** - Time-series database for metrics collection
2. **Grafana** - Data visualization and dashboarding
3. **Netdata** - Real-time system monitoring
4. **Loki** - Log aggregation system
5. **Fluentd** - Unified logging layer

### Web Interface Layer

1. **Web Interface** - Next.js frontend for platform management
2. **AI Agents** - Pydantic AI agents with tools for automation

### Container Management

1. **Portainer** - Container management UI
2. **Podman** - Container engine

### OSINT Tools

1. **Kali OSINT** - Container with Kali Linux OSINT tools
2. **BlackArch OSINT** - Container with BlackArch Linux OSINT tools
3. **BlackArch MCP** - MCP server with BlackArch Linux tools

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

### Local Deployment

For local deployment, use the provided deployment script:

```bash
cd deployment/local
./deploy-local.sh
```

### Remote Deployment

For remote deployment, use the remote deployment script:

```bash
cd deployment/remote
./deploy-remote.sh -h <host> -u <user> -k <ssh_key>
```

### Ansible Deployment

For automated deployment using Ansible:

```bash
cd deployment/ansible
ansible-playbook -i inventory.ini deploy.yml
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

## Usage

### Starting the Platform

```bash
./scripts/manage-platform.sh start
```

### Stopping the Platform

```bash
./scripts/manage-platform.sh stop
```

### Viewing Logs

```bash
./scripts/manage-platform.sh logs
```

### Creating Backups

```bash
./scripts/manage-platform.sh backup
```

### Restoring from Backup

```bash
./scripts/manage-platform.sh restore <backup_file>
```

### Updating the Platform

```bash
./scripts/manage-platform.sh update
```

## Security

### Authentication

The platform uses Bitwarden for secrets management and authentication.

### Encryption

All communications are encrypted using SSL/TLS with Let's Encrypt certificates.

### Network Security

The platform uses Docker networks for isolation and Traefik for access control.

### Monitoring

The platform includes comprehensive monitoring with Prometheus, Grafana, Netdata, and Loki.

## Monitoring

### Metrics Collection

Prometheus collects metrics from all services at regular intervals.

### Log Aggregation

Fluentd collects logs from all services and forwards them to Loki for aggregation.

### Visualization

Grafana provides dashboards for visualizing metrics and logs.

### Real-Time Monitoring

Netdata provides real-time system monitoring.

### Alerting

Alerts can be configured in Prometheus and Grafana for critical events.

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

### Debugging

Enable debug mode in the master configuration file for more verbose logging.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Guidelines

1. Follow the existing code style
2. Write tests for new functionality
3. Update documentation when making changes
4. Keep pull requests focused on a single feature or bug fix

### Code of Conduct

Please follow our code of conduct when contributing to the project.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue on the GitHub repository.