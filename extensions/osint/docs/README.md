# OSINT Analysis Extension for BeEF

## Overview

The OSINT Analysis Extension for BeEF provides comprehensive open source intelligence gathering and analysis capabilities. This extension enables security professionals to research and analyze publicly available information about people, IP addresses, domains, and email addresses, with powerful knowledge graph linking capabilities.

## Features

- Multi-agent AI framework using CrewAI and LangChain
- Knowledge graph implementation with Neo4j
- Integration with Ollama Dolphin models for uncensored AI analysis
- Comprehensive reporting capabilities
- Web-based user interface for research and analysis
- Data linking between entities (people, IPs, domains, emails)

## Installation

1. Install Neo4j database
2. Install Ollama and required models
3. Install CrewAI and LangChain dependencies
4. Configure the extension in `config.yaml`

## Configuration

The extension can be configured in `extensions/osint/config.yaml`:

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
      
      # CrewAI configuration
      crewai:
        enabled: true
```

## Usage

1. Start BeEF with the OSINT extension enabled
2. Access the OSINT dashboard through the BeEF web interface
3. Create new research targets
4. Monitor research progress
5. View knowledge graph visualizations
6. Generate and export reports

## Components

### Multi-Agent Framework

The extension includes two multi-agent frameworks:

1. **CrewAI Framework**: Pre-configured crews for research, analysis, and reporting
2. **LangChain Framework**: Dynamic agent creation with Ollama integration

### Knowledge Graph

The Neo4j-based knowledge graph supports linking between:

- People and their associated information
- Email addresses and their owners
- Domains and their registrants/hosting
- IP addresses and their associated domains
- Social media profiles and people

### Reporting

The extension provides multiple report types:

- Executive Summary
- Technical Report
- Investigative Report

All reports can be exported in HTML, JSON, and PDF formats.

## API Endpoints

- `/ui/osint` - Main OSINT dashboard
- `/api/osint/target/:target_type/:target_id` - Get target information
- `/api/osint/research/start` - Start research on a target
- `/api/osint/research/status/:research_id` - Get research status
- `/api/osint/graph/:target_id` - Get knowledge graph data

## Security Considerations

This extension is intended for authorized security testing only. Users are responsible for complying with all applicable laws and regulations when conducting OSINT research.