# CloudCurio: AI-Powered Code Review and Documentation Platform

## Overview

CloudCurio is an AI-powered platform designed to automate code review, documentation generation, and vulnerability assessment for software projects. The system leverages CrewAI to orchestrate teams of AI agents that can analyze codebases, generate documentation, and identify security vulnerabilities.

## Architecture

The CloudCurio platform consists of several key components:

1. **MCP Server**: The Model Context Protocol server that manages AI crews
2. **CrewAI Framework**: Orchestrates teams of AI agents for various tasks
3. **AI Tools Integration**: Support for multiple AI models and providers
4. **Database Layer**: Stores crew execution results and telemetry
5. **Monitoring Stack**: Observability for the entire platform

### MCP Server

The MCP (Model Context Protocol) server is the core component that manages AI crews. It provides a REST API for starting, monitoring, and managing AI-powered tasks. The server supports multiple crew types including code review, documentation generation, and vulnerability assessment.

#### API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /crews/start` - Start a new crew
- `GET /crews/{crew_id}` - Get crew status
- `GET /crews` - List all crews
- `DELETE /crews/{crew_id}` - Delete a crew
- `POST /crews/stop/{crew_id}` - Stop a crew (not fully implemented)

### Crew Types

CloudCurio supports several types of AI crews:

#### Code Review Crew
- Analyzes codebase structure and components
- Generates architectural documentation
- Performs quality assessment

#### Documentation Crew
- Creates comprehensive documentation from codebase analysis
- Maps all major components and relationships
- Generates developer guides and API documentation

#### Vulnerability Assessment Crew
- Scans codebase for security vulnerabilities
- Analyzes dependencies for known issues
- Generates security reports with recommendations

## AI Tools Integration

CloudCurio supports multiple AI providers and tools:

- **OpenRouter**: Access to multiple models from Mistral, Google, OpenAI, and others
- **OpenAI**: API-based access to GPT models
- **Google Gemini**: Integration with Gemini models
- **Ollama**: Local access to open-source models like Llama
- **LocalAI**: OpenAI-compatible local API
- **Alibaba Qwen**: Qwen series models
- **Groq**: High-speed inference with Llama and Mixtral
- **xAI Grok**: Grok models from xAI
- **LM Studio**: Local models via LM Studio API
- **SambaNova**: Enterprise-grade Llama models
- **DeepInfra**: Access to open-source models
- **Models.dev**: Open-source model hosting
- **LiteLLM**: Proxy for multiple LLM providers
- **Open WebUI**: Web interface for interacting with local and remote models
- **Tabby Terminal**: AI-powered terminal with SSH management

## Setup and Installation

### Prerequisites

- Python 3.10+
- Docker (optional, for containerized deployment)
- API keys for AI providers (if using cloud models)

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
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

4. Start the MCP server:
   ```bash
   python crew/mcp_server/start_server.py
   ```

### Docker Deployment

To run CloudCurio using Docker:

```bash
docker build -f Dockerfile.mcp -t cloudcurio-mcp .
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key_here cloudcurio-mcp
```

## Configuration

### Environment Variables

- `MCP_HOST`: Host to bind to (default: 0.0.0.0)
- `MCP_PORT`: Port to listen on (default: 8000)
- `MCP_DEBUG`: Enable debug mode (default: False)
- `DATABASE_URL`: Database connection string
- `SUPABASE_URL`: Supabase URL
- `SUPABASE_KEY`: Supabase API key
- `OPENAI_API_KEY`: OpenAI API key
- `DEFAULT_MODEL`: Default AI model to use
- `DEFAULT_CREW_TIMEOUT`: Default timeout for crews in seconds
- `MAX_CONCURRENT_CREWS`: Maximum number of concurrent crews
- `LOG_LEVEL`: Logging level (default: INFO)

### Crew Configuration

Each crew type has its own configuration file in the `crew/config/` directory. These files define the agents, tasks, and workflow for each crew type.

## Usage Examples

### Starting a Code Review Crew

```bash
curl -X POST http://localhost:8000/crews/start \
  -H "Content-Type: application/json" \
  -d '{
    "crew_type": "code_review",
    "config": {},
    "input_data": {"repository_path": "/path/to/codebase"}
  }'
```

### Checking Crew Status

```bash
curl http://localhost:8000/crews/{crew_id}
```

## Development

### Adding New Crew Types

To add a new crew type:

1. Create a configuration file in `crew/config/`
2. Implement the crew logic in a new module in the `crew/` directory
3. Update the MCP server to handle the new crew type
4. Add the crew type to the validation list in the server

### Extending AI Tools

New AI providers can be added by extending the `BaseAIProvider` class in `ai_tools/ai_provider.py`.

## Monitoring and Telemetry

The platform includes a monitoring stack with:

- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **Loki**: Log aggregation
- **Netdata**: System monitoring
- **RabbitMQ**: Message queuing for distributed processing

## Security Considerations

- API keys should be stored securely and not committed to version control
- Use environment variables or secure vaults for sensitive configuration
- Validate and sanitize all inputs to prevent injection attacks
- Regularly update dependencies to address security vulnerabilities

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

## Contributing

See the CONTRIBUTING.md file for guidelines on how to contribute to the project.

## License

This project is licensed under the MIT License - see the LICENSE file for details.