# CloudCurio: AI-Powered Development Platform (Monorepo)

CloudCurio is an AI-powered platform designed to automate code review, documentation generation, and vulnerability assessment for software projects. The system leverages CrewAI to orchestrate teams of AI agents that can analyze codebases, generate documentation, and identify security vulnerabilities.

## 🏗️ Monorepo Structure

```
cloudcurio/
├── crew/                    # AI crew management (CrewAI-based)
├── ai_tools/               # Multi-provider AI integration
├── sysmon/                 # System monitoring and configuration tracking
├── config_editor/          # Web-based configuration editor
├── container/              # Docker configurations
├── docs/                   # Documentation
├── examples/               # Example configurations and use cases
├── tests/                  # Test suites
├── scripts/                # Utility scripts
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

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/cbwinslow/cloudcurio.git
   cd cloudcurio
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r crew/requirements.txt
   pip install -r config_editor/requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

4. Setup complete environment:
   ```bash
   ./complete_setup.sh
   ```

## 📚 Available Tools

### 1. Multi-Provider AI System (`ai_tools/`)
Supports multiple AI providers with secure credential storage:
- OpenRouter: Access to multiple models from Mistral, Google, OpenAI, and others
- OpenAI: GPT models (GPT-3.5, GPT-4, GPT-4 Turbo)
- Google Gemini: Gemini Pro, Gemini 1.5 models
- Ollama: Local open-source models (Llama, Mistral, etc.)
- LocalAI: OpenAI-compatible local API
- Alibaba Qwen: Qwen series models
- Groq: High-speed inference with Llama and Mixtral
- xAI Grok: Grok models from xAI
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
- Runs as systemd service

### 4. Configuration Editor (`config_editor/`)
Web-based configuration management with AI-powered automation:
- Visual service and program management
- Port scanning to identify running services
- AI-powered action recording and categorization
- Puppeteer integration for web automation
- Step grouping for common tasks

### 5. Terminal Integration (`terminal_tools/`)
Tabby terminal with CloudCurio configuration:
- Pre-configured SSH connections
- AI-assisted coding features
- Optimized settings for development

### 6. Web Interface Integration (`open_webui/`)
Open WebUI for graphical interaction with models:
- Support for local models (Ollama)
- Multiple AI provider integration (LiteLLM)
- RAG capabilities with web search
- Chat interface for interacting with AI models

## 🛠️ Usage Examples

### MCP Server API
```bash
# Start a code review crew
curl -X POST http://localhost:8000/crews/start \
  -H "Content-Type: application/json" \
  -d '{
    "crew_type": "code_review",
    "input_data": {"repository_path": "/path/to/codebase"}
  }'

# Check crew status
curl http://localhost:8000/crews/{crew_id}
```

### AI Provider Management
```bash
# Add API key securely
python -m ai_tools.cli add-credential openrouter

# List available providers
python -m ai_tools.cli list-providers

# Set default provider
python -m ai_tools.cli set-default openrouter
```

### System Monitoring
```bash
# Create configuration snapshot
cloudcurio-sysmon snapshot my-setup

# Monitor continuously
cloudcurio-sysmon monitor --continuous

# View recent events
cloudcurio-sysmon events --limit 20
```

## 📋 Master Task Management

CloudCurio includes a comprehensive task management system organized by:
- **Domain**: AI, SysMon, ConfigEditor, MCP, etc.
- **Priority**: Critical, High, Medium, Low
- **Status**: Not Started, In Progress, Blocked, Completed
- **Assigned To**: Team members

See [TASK_LIST.md](TASK_LIST.md) for the complete master task list.

## 📖 Documentation

- [PROCEDURE_HANDBOOK.md](PROCEDURE_HANDBOOK.md) - Complete usage guide with examples
- [MONOREPO_STRUCTURE.md](MONOREPO_STRUCTURE.md) - Monorepo organization
- [Examples Repository](examples/EXAMPLES_REPOSITORY.md) - Practical examples
- Domain-specific documentation in each component directory

## 🤝 Contributing

We welcome contributions to CloudCurio! Please see our [contributing guidelines](CONTRIBUTING.md) for more information.

## 🏷️ Branching and Tagging Strategy

- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: Individual feature branches
- `release/*`: Release preparation branches
- `hotfix/*`: Urgent fixes for main branch

Tags follow semantic versioning: `v{MAJOR}.{MINOR}.{PATCH}`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.