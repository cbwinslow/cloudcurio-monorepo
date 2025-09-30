# CloudCurio: AI-Powered Development Platform (Monorepo)

> **Note**: This is the main repository for the CloudCurio platform. For the latest version and complete documentation, see [MONOREPO_README.md](MONOREPO_README.md)

CloudCurio is an AI-powered platform designed to automate code review, documentation generation, and vulnerability assessment for software projects. The system leverages CrewAI to orchestrate teams of AI agents that can analyze codebases, generate documentation, and identify security vulnerabilities.

This repository has been restructured as a monorepo to better organize the various components of the CloudCurio platform. For complete information about the project structure, components, and usage, please refer to the [Monorepo README](MONOREPO_README.md).

## Features

- Automated code review with AI agents
- Documentation generation from codebase analysis
- Vulnerability assessment and security scanning
- REST API for crew management
- Support for multiple AI providers (OpenRouter, OpenAI, Google Gemini, Ollama, LocalAI, Qwen, Groq, Grok, LM Studio, SambaNova, DeepInfra, Models.dev, LiteLLM, and more)
- Secure credential storage using GPG encryption
- Portable configuration system with persistent agent configurations
- Database logging for crew results and telemetry
- Configurable crew types and workflows

## Architecture

- **MCP Server**: Model Context Protocol server managing AI crews
- **CrewAI Framework**: Orchestrates teams of AI agents
- **AI Tools Integration**: Multiple AI model support
- **Database Layer**: Stores execution results and telemetry
- **Monitoring Stack**: Observability for platform health

## Prerequisites

- Python 3.10+
- Docker (for containerized deployment)
- API keys for AI providers (if using cloud models)
- GPG (for secure credential storage, optional but recommended)

## Installation

### Local Installation

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
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

4. [Optional] Setup GPG for secure credential storage:
   ```bash
   # On Ubuntu/Debian
   sudo apt-get install gnupg
   
   # On macOS
   brew install gnupg
   ```

5. Configure AI providers using the CLI:
   ```bash
   # Setup configuration directory
   python -m ai_tools.cli setup
   
   # Add API keys for providers you want to use
   python -m ai_tools.cli add-credential openai
   python -m ai_tools.cli add-credential gemini
   python -m ai_tools.cli add-credential openrouter
   # ... etc for other providers
   
   # Set default provider
   python -m ai_tools.cli set-default openrouter
   ```

6. Start the MCP server:
   ```bash
   python crew/mcp_server/start_server.py
   ```

### Docker Installation

To run CloudCurio using Docker:

```bash
docker build -f Dockerfile.mcp -t cloudcurio-mcp .
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key_here cloudcurio-mcp
```

## AI Provider Support

CloudCurio supports multiple AI providers:

- **OpenRouter**: Access to multiple models from Mistral, Google, OpenAI, and others
- **OpenAI**: GPT models (GPT-3.5, GPT-4, GPT-4 Turbo)
- **Google Gemini**: Gemini Pro, Gemini 1.5 models
- **Ollama**: Local open-source models (Llama, Mistral, etc.)
- **LocalAI**: OpenAI-compatible local API
- **Alibaba Qwen**: Qwen series models
- **Groq**: High-speed inference with Llama and Mixtral
- **xAI Grok**: Grok models from xAI
- **LM Studio**: Local models via LM Studio API
- **SambaNova**: Enterprise-grade Llama models
- **DeepInfra**: Access to open-source models
- **Models.dev**: Open-source model hosting
- **LiteLLM**: Proxy for multiple LLM providers

## Secure Credential Storage

CloudCurio uses GPG encryption to securely store API keys locally:

1. Credentials are encrypted using a passphrase (by default using an environment variable)
2. Stored in `~/.cloudcurio/credentials.json.gpg`
3. Can fallback to environment variables if GPG is not available
4. Supports multiple provider credentials simultaneously

## Agent Configuration

CloudCurio allows persistent configuration of AI agents:

```bash
# List available agents
python -m ai_tools.cli list-agents

# Configure an agent with specific provider/model
python -m ai_tools.cli configure-agent code-analyst --provider openrouter --model mistralai/mistral-7b-instruct
```

## Terminal Tools Integration

CloudCurio includes integration with Tabby terminal for enhanced development workflows:

1. Setup Tabby terminal with CloudCurio configuration:
   ```bash
   ./setup_tabby.sh
   ```

2. Install Tabby from https://eugeny.github.io/tabby/

3. Launch with CloudCurio configuration:
   ```bash
   cloudcurio-terminal
   ```

The Tabby configuration includes:
- Pre-configured SSH connections
- AI-assisted coding features
- Optimized settings for development

## Configuration Management and Automation

CloudCurio includes several tools for managing and automating your system configuration:

### System Monitoring (SysMon)

A comprehensive system monitoring tool that tracks all system changes:

1. Setup the system monitor:
   ```bash
   ./setup_sysmon.sh
   ```

2. Create your first configuration snapshot:
   ```bash
   cloudcurio-sysmon setup
   ```

3. Monitor system changes:
   ```bash
   cloudcurio-sysmon monitor --continuous
   ```

4. Create configuration snapshots:
   ```bash
   cloudcurio-sysmon snapshot my-system-config
   ```

5. Generate reproduction scripts:
   ```bash
   cloudcurio-sysmon reproduce my-system-config reproduce.sh
   ```

Features of SysMon:
- Tracks package installations, removals, and updates
- Monitors service changes
- Aggregates system logs
- Captures user configuration files
- Generates bash scripts to reproduce your system configuration
- Provides bash completion for all commands
- Runs as a systemd service for continuous monitoring

### Web-Based Configuration Editor

A web interface for managing system configurations with AI-powered action recording:

1. Setup the configuration editor:
   ```bash
   ./setup_config_editor.sh
   ```

2. Start the web interface:
   ```bash
   python config_editor/launcher.py
   ```

3. Access the web interface at: `http://localhost:8081`

Features of the Configuration Editor:
- Visual management of services and programs
- Port scanning to identify running services
- AI-powered action recording and categorization
- Puppeteer integration for web automation recording
- Step grouping for common tasks (like API key creation)
- Download tracking for installed software

1. Setup the system monitor:
   ```bash
   ./setup_sysmon.sh
   ```

2. Create your first configuration snapshot:
   ```bash
   cloudcurio-sysmon setup
   ```

3. Monitor system changes:
   ```bash
   cloudcurio-sysmon monitor --continuous
   ```

4. Create configuration snapshots:
   ```bash
   cloudcurio-sysmon snapshot my-system-config
   ```

5. Generate reproduction scripts:
   ```bash
   cloudcurio-sysmon reproduce my-system-config reproduce.sh
   ```

Features of SysMon:
- Tracks package installations, removals, and updates
- Monitors service changes
- Aggregates system logs
- Captures user configuration files
- Generates bash scripts to reproduce your system configuration
- Provides bash completion for all commands
- Runs as a systemd service for continuous monitoring

## Web Interface with Open WebUI

CloudCurio provides integration with Open WebUI for a graphical interface:

1. Setup Open WebUI with Docker:
   ```bash
   ./setup_open_webui.sh
   ```

2. Start the Open WebUI stack:
   ```bash
   ./start_open_webui.sh
   ```

3. Access Open WebUI at http://localhost:3000

The Open WebUI integration includes:
- Support for local models (Ollama)
- Multiple AI provider integration (LiteLLM)
- RAG capabilities with web search
- Chat interface for interacting with AI models

## Usage

The MCP server provides a REST API to manage AI crews:

- Start a crew: `POST /crews/start`
- Check status: `GET /crews/{crew_id}`
- List crews: `GET /crews`

See the [API documentation](MCP_SERVER_DOCS.md) for complete details.

## Contributing

We welcome contributions to CloudCurio! Please see our [contributing guidelines](CONTRIBUTING.md) for more information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.