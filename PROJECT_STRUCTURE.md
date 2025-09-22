# OSINT Platform - Project Structure

This document provides an overview of the OSINT Platform project structure.

## Root Directory

```
osint-platform/
├── README.md                      # Main project README
├── GETTING_STARTED.md            # Quick start guide
├── OSINT_PLATFORM_DOCUMENTATION.md # Comprehensive documentation
├── OSINT_PLATFORM_SUMMARY.md     # Project summary
├── OSINT_PLATFORM_DIAGRAM.md     # Architecture diagrams
├── PLUGIN_ARCHITECTURE.md        # Plugin system architecture
├── LINK_SHORTENER_INTEGRATION.md # Link shortener integration guide
├── docker-compose.yml            # Main Docker Compose configuration
├── Dockerfile.beef               # BeEF Dockerfile
├── start-osint-platform.sh       # Main starter script
├── .gitignore                    # Git ignore file
├── .github/                      # GitHub configuration
│   └── workflows/                # GitHub Actions workflows
│       ├── docker-build.yml     # Docker image building
│       ├── test.yml             # Testing workflow
│       ├── deploy.yml           # Deployment workflow
│       ├── security-scan.yml     # Security scanning
│       ├── docs.yml             # Documentation generation
│       └── backup.yml           # Automated backup
├── config/                      # Configuration files
│   ├── master-config.yaml        # Master configuration
│   └── services/                # Service-specific configurations
│       ├── traefik/             # Traefik configuration
│       ├── kong/                # Kong configuration
│       ├── supabase/            # Supabase configuration
│       ├── neo4j/               # Neo4j configuration
│       ├── bitwarden/           # Bitwarden configuration
│       ├── searxng/             # SearXNG configuration
│       ├── beef/                # BeEF configuration
│       ├── n8n/                # n8n configuration
│       ├── localai/             # LocalAI configuration
│       ├── ollama/              # Ollama configuration
│       ├── openwebui/           # OpenWebUI configuration
│       ├── localrecall/        # LocalRecall configuration
│       ├── flowise/             # Flowise configuration
│       ├── mcp-server/          # MCP Server configuration
│       ├── rabbitmq/            # RabbitMQ configuration
│       ├── prometheus/         # Prometheus configuration
│       ├── grafana/             # Grafana configuration
│       ├── netdata/             # Netdata configuration
│       ├── loki/                # Loki configuration
│       ├── fluentd/             # Fluentd configuration
│       ├── sentry/              # Sentry configuration
│       ├── archon/              # Archon configuration
│       ├── portainer/           # Portainer configuration
│       ├── podman/             # Podman configuration
│       ├── kali-osint/          # Kali OSINT configuration
│       ├── blackarch-osint/     # BlackArch OSINT configuration
│       └── blackarch-mcp/       # BlackArch MCP configuration
├── data/                        # Persistent data storage
│   ├── supabase/                # Supabase database files
│   ├── neo4j/                   # Neo4j database files
│   ├── bitwarden/               # Bitwarden data files
│   ├── n8n/                     # n8n data files
│   ├── localai/                 # LocalAI model files
│   ├── openwebui/               # OpenWebUI data files
│   ├── localrecall/             # LocalRecall data files
│   ├── flowise/                 # Flowise data files
│   ├── rabbitmq/                # RabbitMQ data files
│   ├── prometheus/              # Prometheus data files
│   ├── grafana/                 # Grafana data files
│   ├── netdata/                 # Netdata data files
│   ├── sentry/                  # Sentry data files
│   ├── portainer/               # Portainer data files
│   ├── ollama/                  # Ollama model files
│   ├── kali/                    # Kali OSINT data files
│   ├── blackarch/              # BlackArch OSINT data files
│   └── mcp/                     # MCP server data files
├── traefik/                     # Traefik configuration
│   ├── letsencrypt/             # SSL certificates
│   │   └── acme.json            # ACME certificate storage
│   ├── traefik.yml              # Main Traefik configuration
│   └── dynamic.yml              # Dynamic Traefik configuration
├── kong/                        # Kong configuration
│   └── kong.yml                 # Kong declarative configuration
├── searxng/                     # SearXNG configuration
│   └── settings.yml             # SearXNG settings
├── prometheus/                  # Prometheus configuration
│   └── prometheus.yml           # Prometheus configuration
├── fluentd/                     # Fluentd configuration
│   └── conf/                     # Fluentd configuration files
├── backups/                     # Backup storage
├── plugins/                     # Plugin system
│   ├── framework/               # Plugin framework
│   │   ├── base.py              # Base plugin classes
│   │   └── types.py             # Plugin type definitions
│   ├── samples/                 # Sample plugins
│   │   ├── web-collector/       # Web data collector plugin
│   │   ├── sentiment-analyzer/   # Sentiment analysis plugin
│   │   └── slack-integration/  # Slack integration plugin
│   └── config/                  # Plugin configuration
├── deployment/                  # Deployment scripts and configurations
│   ├── local/                   # Local deployment scripts
│   │   └── deploy-local.sh     # Local deployment script
│   ├── remote/                   # Remote deployment scripts
│   │   └── deploy-remote.sh    # Remote deployment script
│   ├── ansible/                  # Ansible playbooks
│   │   ├── inventory.ini         # Ansible inventory
│   │   ├── deploy.yml           # Main deployment playbook
│   │   ├── vars/                # Ansible variables
│   │   ├── tasks/               # Ansible tasks
│   │   ├── templates/            # Ansible templates
│   │   ├── files/               # Ansible files
│   │   └── roles/                # Ansible roles
│   ├── docker/                  # Docker configurations for deployment
│   │   ├── kali-osint/          # Kali OSINT container
│   │   │   └── Dockerfile       # Kali OSINT Dockerfile
│   │   ├── blackarch-osint/     # BlackArch OSINT container
│   │   │   └── Dockerfile       # BlackArch OSINT Dockerfile
│   │   └── mcp-blackarch/       # BlackArch MCP server
│   │       └── Dockerfile      # BlackArch MCP Dockerfile
│   ├── scripts/                 # Deployment scripts
│   │   ├── cloudflare-integration.sh  # Cloudflare integration
│   │   ├── gitlab-integration.sh      # GitLab integration
│   │   ├── podman-configuration.sh     # Podman configuration
│   │   ├── podman-compose-compat.sh   # Podman Compose compatibility
│   │   ├── kali-tools-init.sh         # Kali tools initialization
│   │   └── blackarch-tools-init.sh    # BlackArch tools initialization
│   └── config/                  # Deployment configurations
│       └── cloudflare.yml       # Cloudflare configuration
├── scripts/                     # Management scripts
│   ├── manage-platform.sh       # Main platform management script
│   ├── setup-platform.sh        # Platform setup script
│   ├── init-ollama.sh           # Ollama initialization script
│   └── backup-platform.sh      # Platform backup script
├── web-interface/               # Next.js web interface
│   ├── package.json             # Node.js dependencies
│   ├── Dockerfile               # Web interface Dockerfile
│   ├── pages/                   # Next.js pages
│   ├── components/              # React components
│   ├── styles/                  # CSS styles
│   ├── lib/                    # Library code
│   └── public/                 # Static assets
├── ai-agents/                   # Pydantic AI agents
│   ├── requirements.txt         # Python dependencies
│   ├── Dockerfile               # AI agents Dockerfile
│   ├── main.py                  # Main AI agents script
│   ├── agents/                  # AI agent implementations
│   │   ├── base.py              # Base agent classes
│   │   └── impl.py              # Specific agent implementations
│   ├── tools/                   # AI agent tools
│   │   └── impl.py              # Tool implementations
│   └── config/                  # AI agent configuration
│       └── agents.yaml         # Agent configuration
├── beef-config/                 # BeEF configuration files
├── neo4j/                       # Neo4j configuration
│   └── plugins/                # Neo4j plugins
├── docs/                        # Documentation files
│   ├── architecture.png         # Architecture diagram
│   └── api/                     # API documentation
└── LICENSE                      # License file
```

## Key Directories Explained

### config/
Contains all configuration files for the platform and individual services. This is the central location for managing platform settings.

### data/
Stores persistent data for all services. Each service has its own subdirectory to ensure data isolation and persistence across container restarts.

### deployment/
Contains scripts and configurations for deploying the platform in different environments (local, remote, Ansible, etc.).

### plugins/
Implements the plugin system for extending platform functionality. Contains the framework, sample plugins, and configuration files.

### scripts/
Management scripts for common platform operations like starting, stopping, backing up, and updating the platform.

### services/
Each service runs in its own container with specific configuration files stored in subdirectories under this directory.

## File Naming Conventions

- **Configuration files**: Use `.yml` or `.yaml` extensions for YAML files, `.conf` for configuration files, and `.env` for environment variables
- **Script files**: Use `.sh` extension for shell scripts
- **Documentation files**: Use `.md` extension for Markdown files
- **Docker files**: Use `Dockerfile` or `Dockerfile.<service>` for Docker configuration
- **Workflow files**: Use `.yml` extension and descriptive names for GitHub Actions workflows

## Important Files

1. **docker-compose.yml**: Main orchestration file for all services
2. **config/master-config.yaml**: Central configuration file for the entire platform
3. **start-osint-platform.sh**: Main entry point for users to interact with the platform
4. **README.md**: Primary documentation for the project
5. **GETTING_STARTED.md**: Quick start guide for new users

## Data Persistence

All important data is stored in the `data/` directory to ensure persistence across container restarts and updates. Each service has its own subdirectory to maintain data isolation.

## Configuration Management

The platform uses a hierarchical configuration system:
1. **Master Configuration**: `config/master-config.yaml` contains global settings
2. **Service Configuration**: Individual service configurations in `config/services/`
3. **Environment Variables**: Sensitive data stored as environment variables
4. **Runtime Configuration**: Some services support runtime configuration through APIs

## Backup Strategy

The platform implements a comprehensive backup strategy:
1. **Database Backups**: Regular backups of Supabase and Neo4j databases
2. **Configuration Backups**: Periodic backups of all configuration files
3. **Data Backups**: Regular backups of important data files
4. **Automated Backups**: Scheduled backups using cron jobs
5. **Scripted Backups**: Manual backup creation using management scripts

This structure ensures that the OSINT Platform is organized, maintainable, and scalable while providing clear separation of concerns between different components.