# CloudCurio MCP Server Technical Documentation

## Overview

The Model Context Protocol (MCP) server is the core service that manages CrewAI crews for the CloudCurio platform. It provides an API for starting, monitoring, and managing AI-powered tasks like code review, documentation generation, and vulnerability assessment.

## Architecture

The MCP server follows a RESTful API architecture built with FastAPI. It includes:

- API endpoints for crew management
- Database integration for logging results and telemetry
- Asynchronous task execution for crew runs
- Configuration management for different crew types
- AI provider abstraction layer

## Installation and Deployment

### Prerequisites

- Python 3.10+
- pip package manager
- Virtual environment (recommended)

### Local Installation

1. Install dependencies:
   ```bash
   pip install -r crew/mcp_server/requirements.txt
   ```

2. Set environment variables (see `.env.example`)

3. Start the server:
   ```bash
   python crew/mcp_server/start_server.py
   ```

### Docker Deployment

To deploy using Docker:

1. Build the image:
   ```bash
   docker build -f Dockerfile.mcp -t cloudcurio-mcp .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 -e OPENAI_API_KEY=your_key_here cloudcurio-mcp
   ```

## API Endpoints

### Health Check
- **GET /** - Server status
- **GET /health** - Health check

### Crew Management
- **POST /crews/start** - Start a new crew
- **GET /crews/{crew_id}** - Get crew status and results
- **GET /crews** - List all crews
- **DELETE /crews/{crew_id}** - Delete a crew
- **POST /crews/stop/{crew_id}** - Stop a running crew

### Request/Response Examples

Starting a crew:
```json
POST /crews/start
{
  "crew_type": "code_review",
  "config": {},
  "input_data": {
    "repository_path": "/path/to/repository"
  }
}
```

Response:
```json
{
  "crew_id": "uuid-string",
  "message": "Crew started successfully"
}
```

Crew status response:
```json
{
  "crew_id": "uuid-string",
  "crew_type": "code_review",
  "status": "running",
  "created_at": "2023-01-01T00:00:00Z",
  "started_at": "2023-01-01T00:00:00Z",
  "completed_at": null,
  "result": null,
  "error": null
}
```

## Configuration

### Environment Variables

- `MCP_HOST`: Server host (default: 0.0.0.0)
- `MCP_PORT`: Server port (default: 8000)
- `MCP_DEBUG`: Enable debug mode (default: false)
- `DATABASE_URL`: Database connection string
- `SUPABASE_URL`: Supabase instance URL
- `SUPABASE_KEY`: Supabase service role key
- `OPENAI_API_KEY`: OpenAI API key
- `DEFAULT_MODEL`: Default LLM model (default: gpt-4)
- `DEFAULT_CREW_TIMEOUT`: Timeout in seconds (default: 3600)
- `MAX_CONCURRENT_CREWS`: Max concurrent crews (default: 5)
- `LOG_LEVEL`: Logging level (default: INFO)

### Crew Configuration Files

Crew-specific configurations are stored in JSON files in the `crew/config/` directory. Each crew type has its own configuration file that defines:

- Agent roles and backstories
- Available tools for each agent
- Task definitions and expected outputs
- Execution process (sequential, hierarchical, etc.)

## Database Schema

The server uses SQLAlchemy ORM to store crew execution data. The main table is:

### crew_runs
- `id`: Integer, primary key
- `crew_id`: String, unique identifier for the crew run
- `crew_type`: String, type of crew (code_review, documentation, etc.)
- `status`: String, current status (pending, running, completed, failed)
- `config`: JSON, configuration parameters for the crew
- `input_data`: JSON, input data provided to the crew
- `result`: Text, output from the crew execution
- `error`: Text, error message if crew failed
- `created_at`: DateTime, when the crew was created
- `started_at`: DateTime, when the crew started execution
- `completed_at`: DateTime, when the crew finished execution

## Crew Types

### Code Review Crew
- Analyzes codebase structure and components
- Generates documentation about architecture and components
- Reviews code for quality and best practices

### Documentation Crew
- Creates comprehensive documentation from codebase analysis
- Maps all major components and their relationships
- Generates developer guides and API documentation

### Vulnerability Assessment Crew
- Scans codebase for security vulnerabilities
- Analyzes dependencies for known security issues
- Generates security reports with risk assessment and recommendations

## AI Tools Integration

The system supports multiple AI providers through an abstraction layer:

- **OpenAI**: Cloud-based GPT models
- **Ollama**: Local open-source models
- **Google Gemini**: Google's Gemini models
- **Qwen**: Alibaba's Qwen models

## Monitoring and Logging

The server provides basic monitoring capabilities:

- Request logging with configurable log levels
- Crew execution status tracking
- Error logging for failed crew executions
- Performance metrics (in future versions)

## Extending the Server

### Adding New Crew Types

To add a new crew type:

1. Create a configuration file in `crew/config/`
2. Implement the crew logic in a new module in the `crew/` directory
3. Update the server's execution logic to handle the new crew type
4. Update the validation logic to accept the new crew type

### Adding New AI Providers

New AI providers can be added by extending the `BaseAIProvider` class in `ai_tools/ai_provider.py`.

## Security Considerations

- Validate all input data before processing
- Use environment variables for sensitive configuration
- Implement proper authentication for production deployments
- Sanitize all outputs before returning to clients

## Troubleshooting

### Common Issues

- **Missing API Keys**: Ensure all required environment variables are set
- **Database Connection**: Verify DATABASE_URL is properly configured
- **Crew Execution Failures**: Check logs for specific error messages

### Logging

The server logs to stdout by default. In production, consider using a log management system to capture and analyze logs.

## Future Enhancements

- Authentication and authorization
- Real-time crew status updates via WebSocket
- Advanced orchestration and scheduling
- Integration with CI/CD pipelines
- Extended AI tool support
- Performance optimization and caching