# AI Agents System for BeEF

## Overview

The AI Agents System for BeEF provides intelligent automation capabilities for OSINT (Open Source Intelligence) gathering, analysis, and reporting. This system uses multiple AI agents working together to collect data, analyze findings, generate reports, send alerts, and create dashboards.

## Features

- **Multi-Agent Architecture**: Specialized agents for different tasks
- **RAG (Retrieval-Augmented Generation)**: Enhanced AI responses using vector databases
- **Dashboard Management**: Automatic creation of Grafana and OpenSearch dashboards
- **Environment Configuration**: Secure configuration management with .env files
- **Container Integration**: Docker-ready deployment
- **Extensible Design**: Easy to add new agents and tools

## Agents

1. **Data Collector Agent**: Gathers information from various sources
2. **Analyzer Agent**: Identifies patterns and extracts insights
3. **Reporter Agent**: Generates comprehensive reports and visualizations
4. **Alerter Agent**: Sends notifications through multiple channels
5. **Dashboard Agent**: Creates and manages monitoring dashboards

## Technologies

- **Python 3.13** with uv package manager
- **LangChain** for AI orchestration
- **OpenAI** for natural language processing
- **ChromaDB** for vector storage
- **Grafana** for dashboard visualization
- **OpenSearch** for log analytics
- **Neo4j** for knowledge graph storage
- **Docker** for containerization

## Installation

1. Ensure you have Python 3.13 installed
2. Install uv package manager: `pip install uv`
3. Create virtual environment: `uv venv`
4. Activate virtual environment: `source .venv/bin/activate`
5. Install dependencies: `uv pip install -r requirements.txt`
6. Configure environment variables in `.env` file
7. Run the system: `python main.py`

## Configuration

Create a `.env` file with the following variables:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_neo4j_password

# ChromaDB Configuration
CHROMA_HOST=localhost
CHROMA_PORT=8000

# Grafana Configuration
GRAFANA_HOST=localhost
GRAFANA_PORT=3000
GRAFANA_API_KEY=your_grafana_api_key

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/database
```

## Usage

Run the main script to see example agent operations:

```bash
python main.py
```

## Dashboard Templates

The system includes pre-built dashboard templates for:
- OSINT Monitoring
- Threat Intelligence
- Network Security
- Data Visualization

## Contributing

Contributions are welcome! Please submit pull requests with improvements to the code, documentation, or features.

## License

This project is licensed under the MIT License.