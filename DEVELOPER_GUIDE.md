# CloudCurio: AI-Powered Development Platform (Monorepo)

CloudCurio is an AI-powered platform designed to automate code review, documentation generation, and vulnerability assessment for software projects. The system leverages CrewAI to orchestrate teams of AI agents that can analyze codebases, generate documentation, and identify security vulnerabilities.

## 🌟 New Features

### 🤖 Agentic Platform
- Multi-agent system with configurable agents and tasks
- Crew management system for orchestrating agent teams
- Local AI support with Ollama integration
- Advanced task scheduling and execution

### 🚀 Comprehensive Release Management
- Automated versioning and tagging system
- Multi-platform Docker builds
- PyPI package distribution
- GitLab and GitHub CI/CD pipelines
- Automated release generation

### 📦 Complete Packaging & Installation
- PyPI package for easy installation
- Docker images for containerized deployment
- Comprehensive installer script
- Makefile for build automation
- Cross-platform compatibility

### 🔧 Advanced Configuration Management
- Web-based configuration editor
- System monitoring and change tracking (SysMon)
- AI-powered action classification
- Terminal integration (Tabby)
- Open WebUI for graphical interaction

## 🏗️ Monorepo Structure

```
cloudcurio/
├── crew/                    # AI crew management (CrewAI-based)
├── ai_tools/               # Multi-provider AI integration
├── sysmon/                 # System monitoring and configuration tracking
├── config_editor/          # Web-based configuration editor
├── agentic_platform/       # Advanced multi-agent platform
├── container/              # Docker configurations
├── docs/                   # Documentation
├── examples/               # Example configurations and use cases
├── tests/                  # Test suites
├── scripts/                # Utility scripts
├── releases/               # Release artifacts
├── packaging/              # Packaging configurations
├── domains/                # Domain-specific projects
├── infrastructure/         # Infrastructure as code
├── tools/                  # Development tools
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
git clone https://github.com/cbwinslow/cloudcurio.git
cd cloudcurio

# Run the installation script
./scripts/installers/install.sh

# Or install from source
./scripts/installers/install.sh --install-source
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

## 📊 Feature Tracking System

CloudCurio now includes a comprehensive feature tracking system that monitors usage, performance, and effectiveness of all platform features.

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

### Feature Tracking Capabilities

- **Comprehensive Monitoring**: Tracks usage, performance, success rates, and efficiency
- **Category-Based Organization**: Features organized by functionality (AI, MCP, SysMon, etc.)
- **Performance Metrics**: Execution time, input/output sizes, efficiency scores
- **Real-time Dashboard**: Visualize metrics through an interactive web interface
- **Privacy Controls**: Anonymize user data and exclude sensitive features
- **Configurable**: Environment variables to control tracking behavior

### Integration Examples

The tracking system is already integrated with core CloudCurio components:

- **AI Providers**: All AI model interactions tracked
- **MCP Server**: Crew execution and management operations
- **SysMon**: System monitoring and snapshot operations
- **Agentic Platform**: Agent execution and crew coordination
- **Configuration Editor**: Configuration changes and operations

### Data Collected

The system tracks:
- Execution duration and success status
- Input/output data sizes
- Efficiency scores
- Error information
- User and session context
- Custom metadata

All data is stored locally in SQLite by default, with privacy controls enabled.

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

### Example Agentic Workflow
```python
from agentic_platform import CloudCurioAgenticPlatform

# Initialize the platform
platform = CloudCurioAgenticPlatform()

# Create a custom crew from configuration
crew_id, crew = platform.create_crew_from_config("code_review_crew")

# Run the crew
result = platform.run_crew(crew_id)
print(result)
```

## 🔄 Release Management

### Create a New Release
```bash
# Check current version
python scripts/release_manager.py version

# Bump version (major, minor, or patch)
python scripts/release_manager.py bump --part minor

# Create a release
python scripts/release_manager.py release --version 1.2.0
```

### Version Management
- Automatic changelog generation
- Git tagging and pushing
- PyPI and Docker Hub publishing
- GitHub release creation

## 📋 Available Tools

### 1. Multi-Provider AI System (`ai_tools/`)
Supports multiple AI providers with secure credential storage:
- OpenRouter, OpenAI, Google Gemini, Ollama, LocalAI
- Alibaba Qwen, Groq, xAI Grok, Anthropic, Cohere
- And 10+ more providers

### 2. MCP Server (`crew/mcp_server/`)
Model Context Protocol server for managing AI crews:
- REST API for crew management
- Support for multiple crew types
- Database logging for results and telemetry
- Async crew execution

### 3. System Monitor (SysMon) (`sysmon/`)
Comprehensive system monitoring and configuration tracking:
- Tracks package installations/removals
- Monitors service changes
- Aggregates system logs
- Creates configuration snapshots
- Generates reproduction scripts

### 4. Configuration Editor (`config_editor/`)
Web-based configuration management with AI-powered automation:
- Visual service and program management
- Port scanning to identify running services
- AI-powered action recording and categorization
- Puppeteer integration for web automation
- Step grouping for common tasks

### 5. Agentic Platform (`agentic_platform/`)
Advanced multi-agent system:
- Configurable agents and tasks
- Crew orchestration system
- Local AI model support
- Task scheduling and execution
- Multi-agent collaboration

## 📊 Master Task Management

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

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.