# OSINT Platform Architecture

## Overview

This document describes the architecture of a comprehensive OSINT platform that integrates multiple tools for intelligence gathering, analysis, and visualization. The platform is containerized using Docker Compose and includes tools for data collection, processing, storage, analysis, and visualization.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                    Internet                                         │
└─────────────────────────▲───────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────────────────────────┐
│                              Reverse Proxy (Traefik)                              │
│                              Ports: 80, 443                                       │
└─────────────────────────▲───────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────────────────────────┐
│                           API Gateway (Kong)                                      │
│                           Port: 8000/8001/8443/8444                               │
└─────────────────────────▲───────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────────────────────────┐
│                            Load Balancer/Routing                                  │
└─────────────────────────▲───────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────────────────────────┐
│                                                                                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Data          │  │   Processing    │  │   Storage       │  │   Monitoring    │ │
│  │   Collection    │  │   & Analysis    │  │   & Database    │  │   & Logging     │ │
│  │                 │  │                 │  │                 │  │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│           │                     │                     │                     │      │
│           ▼                     ▼                     ▼                     ▼      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ SearXNG         │  │ LocalAI         │  │ Supabase        │  │ Prometheus      │ │
│  │ Port: 8080      │  │ Port: 8081      │  │ Port: 5432      │  │ Port: 9090      │ │
│  │                 │  │                 │  │                 │  │                 │ │
│  │ Archon          │  │ OpenWebUI       │  │ Neo4j           │  │ Grafana         │ │
│  │                 │  │ Port: 3000      │  │ Port: 7474      │  │ Port: 3001      │ │
│  │ BeEF            │  │ LocalRecall     │  │                 │  │                 │ │
│  │ Port: 3002      │  │ Port: 8082      │  │                 │  │ Netdata         │ │
│  │                 │  │                 │  │                 │  │ Port: 19999     │ │
│  │ n8n             │  │ Flowise         │  │                 │  │                 │ │
│  │ Port: 5678      │  │ Port: 3002      │  │                 │  │ Loki            │ │
│  │                 │  │                 │  │                 │  │ Port: 3100      │ │
│  │                 │  │                 │  │                 │  │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│           │                     │                     │                     │      │
│           ▼                     ▼                     ▼                     ▼      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ RabbitMQ        │  │ MCP Server      │  │ Bitwarden       │  │ Fluentd         │ │
│  │ Port: 5672      │  │                 │  │ Port: 8083      │  │ Port: 24224     │ │
│  │ Port: 15672     │  │                 │  │                 │  │                 │ │
│  │                 │  │                 │  │                 │  │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

## Component Descriptions

### 1. Networking Layer

#### Traefik Reverse Proxy
- **Purpose**: Handles SSL termination, routing, and load balancing
- **Ports**: 80 (HTTP), 443 (HTTPS)
- **Configuration**: Automatic SSL with Let's Encrypt, dynamic service discovery

### 2. API Management Layer

#### Kong API Gateway
- **Purpose**: API management, rate limiting, authentication
- **Ports**: 8000 (proxy), 8001 (admin), 8443/8444 (HTTPS)
- **Integration**: Connects to all internal services

### 3. Data Collection Layer

#### SearXNG
- **Purpose**: Metasearch engine for anonymous information gathering
- **Ports**: 8080
- **Features**: 246+ search services, REST API, Tor support

#### Archon
- **Purpose**: OSINT resource directory
- **Integration**: Provides links to external resources

#### BeEF
- **Purpose**: Browser exploitation framework for authorized penetration testing
- **Ports**: 3002
- **Features**: Client-side exploitation, social engineering tools

#### n8n
- **Purpose**: Workflow automation for data collection
- **Ports**: 5678
- **Features**: 500+ integrations, visual workflow designer

### 4. Processing & Analysis Layer

#### LocalAI
- **Purpose**: Local AI models for NLP and analysis
- **Ports**: 8081
- **Features**: Drop-in OpenAI replacement, no cloud dependency

#### OpenWebUI
- **Purpose**: Interface for interacting with local AI models
- **Ports**: 3000
- **Features**: Chat interface, model management

#### LocalRecall
- **Purpose**: Semantic search and knowledge base management
- **Ports**: 8082
- **Features**: Vector database integration, REST API

#### Flowise
- **Purpose**: Visual AI workflow builder
- **Ports**: 3002
- **Features**: Node-based interface, 100+ integrations

#### MCP Server
- **Purpose**: Model Context Protocol server for AI integrations
- **Integration**: Connects AI models to external systems

### 5. Storage & Database Layer

#### Supabase
- **Purpose**: Firebase alternative with PostgreSQL backend
- **Ports**: 5432 (PostgreSQL)
- **Features**: Real-time subscriptions, authentication, storage

#### Neo4j
- **Purpose**: Graph database for relationship analysis
- **Ports**: 7474 (HTTP), 7473 (HTTPS)
- **Features**: Cypher query language, visualization tools

#### Bitwarden
- **Purpose**: Secrets management for credentials and API keys
- **Ports**: 8083
- **Features**: Self-hosted password manager, secure storage

### 6. Monitoring & Logging Layer

#### Prometheus
- **Purpose**: Time-series database for metrics collection
- **Ports**: 9090
- **Features**: Pull-based metrics, alerting

#### Grafana
- **Purpose**: Data visualization and dashboarding
- **Ports**: 3001
- **Features**: 100+ data source integrations, alerting

#### Netdata
- **Purpose**: Real-time system monitoring
- **Ports**: 19999
- **Features**: Per-second metrics, distributed monitoring

#### Loki
- **Purpose**: Log aggregation system
- **Ports**: 3100
- **Features**: Horizontal scalability, Prometheus integration

#### Fluentd
- **Purpose**: Unified logging layer
- **Ports**: 24224
- **Features**: 500+ plugins, data pipeline

#### Sentry
- **Purpose**: Error tracking and performance monitoring
- **Integration**: Application error reporting

#### LogFlare
- **Purpose**: Log management with BigQuery backend
- **Integration**: Cloud-based log storage and querying

### 7. Messaging Layer

#### RabbitMQ
- **Purpose**: Message broker for distributed task processing
- **Ports**: 5672 (AMQP), 15672 (management)
- **Features**: Clustering, high availability

## Data Flow

1. **Data Collection**: SearXNG, Archon, BeEF, and n8n collect data from various sources
2. **Queueing**: RabbitMQ handles task distribution and buffering
3. **Processing**: LocalAI, OpenWebUI, and Flowise process and analyze data
4. **Storage**: Supabase and Neo4j store processed data
5. **Indexing**: LocalRecall creates searchable knowledge bases
6. **Monitoring**: Prometheus, Grafana, Netdata, and Loki monitor system health
7. **Security**: Kong manages API access, Bitwarden handles secrets
8. **Access**: Traefik provides secure external access

## Security Considerations

1. **Network Isolation**: Services communicate through internal Docker network
2. **Secrets Management**: Bitwarden stores all credentials and API keys
3. **Access Control**: Kong handles authentication and authorization
4. **Encryption**: Traefik provides SSL termination
5. **Monitoring**: Comprehensive logging and alerting with Sentry, Loki, and Prometheus

## Scalability

1. **Horizontal Scaling**: Most services can be scaled horizontally
2. **Load Balancing**: Traefik and Kong handle load distribution
3. **Clustering**: RabbitMQ, Neo4j, and Supabase support clustering
4. **Caching**: Redis can be added for performance optimization

## Deployment

The platform is deployed using Docker Compose with the following structure:

```
osint-platform/
├── docker-compose.yml
├── traefik/
│   ├── traefik.yml
│   └── dynamic/
├── supabase/
│   └── config.toml
├── kong/
│   └── kong.yml
├── configs/
│   ├── localai/
│   ├── openwebui/
│   └── ...
├── data/
│   ├── postgres/
│   ├── neo4j/
│   └── ...
├── scripts/
│   ├── setup.sh
│   ├── backup.sh
│   └── ...
└── docs/
    └── ...
```

## Configuration Management

A centralized configuration system manages:
1. Environment variables
2. Service configurations
3. Secrets (via Bitwarden integration)
4. Network settings
5. Feature flags

## Backup and Recovery

1. **Database Backups**: Automated backups for Supabase and Neo4j
2. **Configuration Backups**: Version-controlled configuration files
3. **Log Archiving**: Long-term log storage with Loki and LogFlare
4. **Disaster Recovery**: Scripts for quick restoration

This architecture provides a comprehensive, scalable, and secure OSINT platform that can be deployed anywhere with Docker.