# CloudCurio: AI-Powered Development Platform (Monorepo) v2.1.0

[![CI/CD](https://github.com/cbwinslow/cloudcurio-monorepo/actions/workflows/cicd.yaml/badge.svg)](https://github.com/cbwinslow/cloudcurio-monorepo/actions/workflows/cicd.yaml)
[![Security](https://github.com/cbwinslow/cloudcurio-monorepo/actions/workflows/security-scan.yaml/badge.svg)](https://github.com/cbwinslow/cloudcurio-monorepo/actions/workflows/security-scan.yaml)
[![Tests](https://github.com/cbwinslow/cloudcurio-monorepo/actions/workflows/testing.yaml/badge.svg)](https://github.com/cbwinslow/cloudcurio-monorepo/actions/workflows/testing.yaml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11-blue)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue)](https://www.docker.com/)
[![PyPI](https://img.shields.io/pypi/v/cloudcurio)](https://pypi.org/project/cloudcurio/)

CloudCurio is an AI-powered platform designed to automate code review, documentation generation, and vulnerability assessment for software projects. The system leverages CrewAI to orchestrate teams of AI agents that can analyze codebases, generate documentation, and identify security vulnerabilities.

## 🌟 What's New in v2.1.0

### 🤖 Agentic Platform
- Advanced multi-agent system with configurable agents and crews
- Crew orchestration with sequential/hierarchical processes
- Local AI support with Ollama integration
- Custom agent and crew creation APIs
- Task management system with status tracking

### 📊 Feature Tracking System
- Real-time feature usage tracking and visualization
- SQLite database backend for persistent tracking
- Decorator-based integration (@track_feature)
- Manual tracking for complex operations
- Web dashboard for real-time monitoring
- CLI for querying tracking data
- Category-based organization (AI, MCP, SysMon, etc.)

### 🚀 CI/CD & Release Management
- Complete GitHub Actions workflows for automated testing
- Security scanning with Bandit and Safety
- Performance monitoring and benchmarking
- Automated release management with PyPI and Docker Hub publishing
- Branch management with automated cleanup
- Dependency update automation
- AI code review with local Ollama models

## 🏗️ Architecture

```
cloudcurio/
├── crew/                    # AI crew management (CrewAI-based)
├── ai_tools/               # Multi-provider AI integration
├── sysmon/                 # System monitoring and configuration tracking
├── config_editor/          # Web-based configuration editor
├── feature_tracking/       # Feature usage tracking system
├── agentic_platform.py     # Multi-agent system
├── container/              # Docker configurations
├── docs/                   # Documentation
├── examples/               # Example configurations and use cases
├── tests/                  # Test suites
├── scripts/                # Utility scripts
├── domains/                # Domain-specific projects
├── infrastructure/          # Infrastructure as code
├── tools/                  # Development tools
├── .github/
│   └── workflows/          # GitHub Actions workflows
└── ...
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Docker (for containerized deployment)
- API keys for AI providers (if using cloud models)
- GPG (for secure credential storage)

### Installation Options

#### Option 1: Pip Installation
```bash
pip install cloudcurio
```

#### Option 2: Docker Installation
```bash
# Pull the latest Docker image
docker pull cbwinslow/cloudcurio-mcp:latest

# Run the MCP server
docker run -p 8000:8000 -e OPENROUTER_API_KEY=your_key_here cbwinslow/cloudcurio-mcp:latest
```

#### Option 3: Source Installation
```bash
git clone https://github.com/cbwinslow/cloudcurio-monorepo.git
cd cloudcurio-monorepo

# Run the installation script
./scripts/installers/install.sh

# Or install from source
pip install -e .
```

#### Option 4: Docker Compose (Complete Platform)
```bash
# Start the complete CloudCurio platform
docker-compose up -d

# Access the services:
# - MCP Server: http://localhost:8000
# - Config Editor: http://localhost:8081
# - Open WebUI: http://localhost:3000
# - Ollama: http://localhost:11434
```

## 🛠️ Build & Development

```bash
# Setup development environment
make setup

# Install development dependencies
make install-dev

# Run tests
make test

# Build all packages
make build

# Build specific packages
make build-pip        # Python package
make build-docker     # Docker images

# Run services
make run-mcp          # MCP Server
make run-config-editor # Configuration Editor
make run-sysmon       # System Monitor
```

## 🤖 Agentic Platform Usage

### Setup Agentic Environment
```bash
# Setup complete agentic environment
python scripts/setup_agentic.py

# Or quick setup for local AI only
python scripts/setup_agentic.py --quick
```

### Using the Agentic CLI
```bash
python agentic_platform.py
```

Available commands:
- `list-agents` - List all available agents
- `list-crews` - List all available crews
- `create-crew <crew_type>` - Create a crew from configuration
- `run-crew <crew_id>` - Run a specific crew
- `create-task <name> <description> <agent>` - Create a new task
- `list-tasks` - List all tasks
- `execute-task <task_id>` - Execute a specific task
- `create-agent <name> <role> <goal> <backstory>` - Create a custom agent

## 📊 Feature Tracking System

### Quick Start with Feature Tracking

#### Enable Tracking
Feature tracking is enabled by default. To start tracking your own features:

```python
from feature_tracking.feature_tracker import track_feature, FeatureCategory

@track_feature("my_custom_feature", FeatureCategory.AGENT_PLATFORM)
def my_function(param):
    # Your function logic
    return result
```

#### View Tracking Dashboard
```bash
# Start the tracking dashboard
python -m feature_tracking.dashboard
# Access at: http://localhost:8081
```

#### Use the CLI
```bash
# List top features by usage
python -m feature_tracking.cli list-features --limit 10

# Get statistics for a specific feature
python -m feature_tracking.cli feature-stats my_feature

# List recent feature calls
python -m feature_tracking.cli list-records --limit 20
```

## 🔄 CI/CD Workflows

### Automated Testing
All code changes trigger comprehensive automated testing:

- Unit tests across multiple Python versions (3.10, 3.11)
- Integration tests with PostgreSQL and Redis
- End-to-end tests for user flows
- Security scanning with Bandit and Safety
- Code quality checks with Black, Flake8, and MyPy
- Performance benchmarking

### Automated Deployment
Merging to `main` triggers:

- Automated package building (PyPI and Docker Hub)
- GitHub release creation with assets
- Documentation updates to GitHub Pages
- Security scanning and reporting
- Performance benchmarking and reporting

### Branch Management
- Automated cleanup of merged feature branches
- Branch protection rule enforcement
- Stale branch detection and notification
- Automated synchronization between branches

## 🔧 Advanced Configuration Management

### Multi-Provider AI System
Supports 20+ AI providers with secure credential storage:
- OpenRouter, OpenAI, Google Gemini, Ollama, LocalAI
- Alibaba Qwen, Groq, xAI Grok, Anthropic, Cohere
- And 10+ more providers

### MCP Server
Model Context Protocol server for managing AI crews:
- REST API for crew management
- Support for multiple crew types
- Database logging for results and telemetry
- Async crew execution

### System Monitor (SysMon)
Comprehensive system monitoring and configuration tracking:
- Tracks package installations/removals
- Monitors service changes
- Aggregates system logs
- Creates configuration snapshots
- Generates reproduction scripts

### Configuration Editor
Web-based configuration management with AI-powered automation:
- Visual service and program management
- Port scanning to identify running services
- AI-powered action recording and categorization
- Puppeteer integration for web automation
- Step grouping for common tasks

## 📋 Master Task Management

CloudCurio includes a comprehensive task management system organized by:
- **Domain**: AI, SysMon, ConfigEditor, MCP, etc.
- **Priority**: Critical, High, Medium, Low
- **Status**: Not Started, In Progress, Blocked, Completed
- **Assigned To**: Team members

See [TASK_LIST.md](TASK_LIST.md) for the complete master task list.

## 🏷️ Versioning & Tagging

The project follows semantic versioning (MAJOR.MINOR.PATCH) with automated release management:

- Git tags: `v1.2.3`
- Docker images: `cbwinslow/cloudcurio-mcp:1.2.3`
- PyPI packages: `cloudcurio==1.2.3`

## 🚀 Deployment Options

### Single Service Deployment
```bash
# MCP Server only
docker run -p 8000:8000 -e OPENROUTER_API_KEY=your_key cbwinslow/cloudcurio-mcp:latest
```

### Complete Platform Deployment
```bash
# Using Docker Compose
docker-compose up -d
```

### Kubernetes Deployment (Coming Soon)
Kubernetes manifests are planned for future releases.

## 🤝 Contributing

We welcome contributions to CloudCurio! Please see our [contributing guidelines](CONTRIBUTING.md) for more information.

### Getting Started
1. Fork the repository
2. Create a feature branch from `develop`
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/cloudcurio-monorepo.git
cd cloudcurio-monorepo

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
make install-dev

# Run tests
make test
```

### Code Standards
- Follow PEP 8 style guidelines
- Use type hints for all functions
- Write tests for new functionality
- Update documentation with changes
- Use conventional commit messages

## 🛡️ Security

We take security seriously. Please see our [security policy](SECURITY.md) for information on how to report vulnerabilities.

### Security Features
- Secure credential storage with GPG encryption
- Regular security scanning with Bandit and Safety
- Dependency vulnerability monitoring
- Automated security updates
- Penetration testing for major releases

### Reporting Vulnerabilities
To report a security vulnerability, please email our security team at:
security@cloudcurio.dev

Please do NOT report security vulnerabilities through public GitHub issues.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewAI) for the AI crew orchestration framework
- [LangChain](https://github.com/langchain-ai/langchain) for language model integration
- The open-source community for continuous inspiration and collaboration

## 📞 Support

For support, please:

1. Check the [documentation](docs/)
2. Review existing [issues](https://github.com/cbwinslow/cloudcurio-monorepo/issues)
3. Open a [new issue](https://github.com/cbwinslow/cloudcurio-monorepo/issues/new) if needed

## 🌐 Links

- [Documentation](docs/)
- [API Reference](docs/api/)
- [Examples](examples/)
- [Changelog](CHANGELOG.md)
- [Security Policy](SECURITY.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Branching Strategy](BRANCHING_STRATEGY.md)
- [Release Management](RELEASE_MANAGEMENT.md)
- [Feature Tracking Docs](feature_tracking/README.md)
- [Agentic Platform Docs](AGENTIC_PLATFORM_DOCS.md)