# OSINT Analysis Extension for BeEF

## Overview

The OSINT Analysis Extension for BeEF provides comprehensive open source intelligence gathering and analysis capabilities. This extension enables security professionals to research and analyze publicly available information about people, IP addresses, domains, and email addresses, with powerful knowledge graph linking capabilities.

## Features

- **Multi-Agent AI Framework**: Integration with CrewAI and LangChain for coordinated research operations
- **Knowledge Graph**: Neo4j-based graph database for linking entities and visualizing relationships
- **AI Analysis**: Ollama Dolphin models for uncensored AI-powered analysis
- **Comprehensive Reporting**: Multiple report formats with automated generation
- **Web Interface**: User-friendly dashboard for research management and visualization
- **Entity Linking**: Advanced capabilities to connect people, IPs, domains, and emails

## Components

### 1. Multi-Agent Framework
- **CrewAI Integration**: Pre-configured crews for research, analysis, and reporting
- **LangChain Integration**: Dynamic agent creation with tool usage capabilities
- **Ollama Models**: Uncensored AI models for analysis (Dolphin-Llama3, Dolphin-Mistral)

### 2. Knowledge Graph
- **Neo4j Database**: Graph database for storing and linking OSINT data
- **Entity Types**: Person, Email, Domain, IPAddress, SocialProfile, PhoneNumber, Organization
- **Relationships**: 10+ relationship types for connecting entities
- **Visualization**: Graph visualization in the web interface

### 3. Research Tools
- **Web Research**: Automated web searching and scraping
- **Domain Analysis**: WHOIS, DNS, and hosting investigations
- **Social Media**: Profile discovery and analysis
- **Email Validation**: Verification and disposable email detection

### 4. Reporting
- **Executive Summary**: High-level overview for management
- **Technical Report**: Detailed findings for technical teams
- **Investigative Report**: Timeline and leads for investigators
- **Export Formats**: HTML, JSON, and PDF exports

## Installation

1. Run the installation script:
   ```bash
   cd extensions/osint
   ./install.sh
   ```

2. Configure the extension in `config.yaml`

3. Initialize the Neo4j database:
   ```bash
   cd extensions/osint
   ./scripts/setup_neo4j.rb
   ```

## Configuration

Edit `extensions/osint/config.yaml`:

```yaml
beef:
  extension:
    osint:
      name: 'OSINT Analysis'
      enable: true
      
      # Database configuration for Neo4j
      neo4j:
        host: 'localhost'
        port: 7687
        username: 'neo4j'
        password: 'password'
        database: 'osint'
      
      # Ollama configuration
      ollama:
        host: 'localhost'
        port: 11434
        model: 'dolphin-llama3'
```

## Usage

1. Start BeEF with the OSINT extension enabled
2. Access the OSINT dashboard through the BeEF web interface
3. Create new research targets using the "New Research" button
4. Monitor research progress in the targets table
5. View knowledge graph visualizations by clicking "Graph" for any target
6. Generate reports using the reporting interface
7. Export reports in your preferred format

## API Endpoints

- `/ui/osint` - Main OSINT dashboard
- `/api/osint/target/:target_type/:target_id` - Get target information
- `/api/osint/research/start` - Start research on a target
- `/api/osint/research/status/:research_id` - Get research status
- `/api/osint/graph/:target_id` - Get knowledge graph data

## Documentation

- [Main Documentation](docs/README.md)
- [API Reference](docs/api.md)
- [Neo4j Schema](docs/neo4j_schema.md)

## Security Considerations

This extension is intended for authorized security testing only. Users are responsible for complying with all applicable laws and regulations when conducting OSINT research.

## Contributing

Contributions are welcome! Please submit pull requests with improvements to the code, documentation, or features.

## License

This extension is released under the same license as BeEF - GNU General Public License v2.0.