# CloudCurio MCP Server

The Model Context Protocol (MCP) server manages CrewAI crews for the CloudCurio platform. It provides an API for starting, monitoring, and managing AI-powered tasks.

## Features

- REST API for managing CrewAI crews
- Database logging for crew results and telemetry
- Support for multiple crew types (code review, documentation, vulnerability assessment)
- Async crew execution with status tracking
- Health checks and monitoring endpoints

## Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /crews/start` - Start a new crew
- `GET /crews/{crew_id}` - Get crew status
- `GET /crews` - List all crews
- `DELETE /crews/{crew_id}` - Delete a crew
- `POST /crews/stop/{crew_id}` - Stop a crew (not fully implemented)

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables (see `.env.example`)

3. Start the server:
   ```bash
   python start_server.py
   ```

## Configuration

The server can be configured using environment variables:

- `MCP_HOST` - Host to bind to (default: 0.0.0.0)
- `MCP_PORT` - Port to listen on (default: 8000)
- `MCP_DEBUG` - Enable debug mode (default: False)
- `DATABASE_URL` - Database connection string
- `SUPABASE_URL` - Supabase URL
- `SUPABASE_KEY` - Supabase API key
- `OPENAI_API_KEY` - OpenAI API key
- `DEFAULT_MODEL` - Default AI model to use
- `DEFAULT_CREW_TIMEOUT` - Default timeout for crews in seconds
- `MAX_CONCURRENT_CREWS` - Maximum number of concurrent crews
- `LOG_LEVEL` - Logging level (default: INFO)

## Database

The server logs crew runs to a database using SQLAlchemy. By default, it uses SQLite, but can be configured to use PostgreSQL or other databases.

## Crew Types

Currently supported crew types:
- `code_review` - Reviews code and generates documentation
- `documentation` - Creates documentation from codebase
- `vulnerability_assessment` - Performs security analysis