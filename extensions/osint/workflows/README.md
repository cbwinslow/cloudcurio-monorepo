# Agentic Workflow Enhancements Summary

## Overview

This document summarizes the enhancements made to add agentic workflow capabilities to the OSINT platform using n8n and OpenWebUI.

## Components Added

### 1. n8n Workflows

#### Workflow Types
1. **Domain Research Workflow**
   - Searches for domain-related information
   - Validates domain registration
   - Stores findings in the database
   - Updates the knowledge graph

2. **Email Research Workflow**
   - Validates email addresses
   - Analyzes social engineering risks
   - Updates the knowledge graph with email information

3. **Person Research Workflow**
   - Searches social media for person information
   - Finds associated domains
   - Generates comprehensive profiles
   - Updates the knowledge graph

4. **Entity Linking Workflow**
   - Identifies relationships between entities
   - Analyzes connection nature
   - Creates relationships in the knowledge graph

5. **Master Workflow**
   - Orchestrates all other workflows
   - Generates comprehensive reports

#### Integration Points
- **SearxNG**: For web searches
- **LocalAI**: For AI analysis and generation
- **Neo4j**: For knowledge graph storage
- **PostgreSQL**: For relational data storage
- **AI Agents**: For report generation

### 2. OpenWebUI Configurations

#### AI Assistant Presets
1. **OSINT Research Assistant**
   - Specialized in Open Source Intelligence research
   - Expert in people, organizations, domains, and IP addresses

2. **Threat Intelligence Analyst**
   - Specialized in cyber threat intelligence analysis
   - Focus on threat actors, malware, and vulnerabilities

3. **OSINT Report Generator**
   - Specialized in creating comprehensive OSINT reports
   - Expert in executive summaries and technical details

### 3. BeEF Integration

#### New Features
- **Workflow Dashboard**: UI for managing and executing workflows
- **Workflow API**: REST API for workflow management
- **Integrated Execution**: Direct workflow execution from the BeEF interface

#### Controllers
- **Main Controller**: Updated dashboard with workflow access
- **Workflow Controller**: Dedicated controller for workflow management

## File Structure

```
extensions/osint/workflows/
├── n8n/
│   ├── osint_domain_research.json
│   ├── osint_email_research.json
│   ├── osint_person_research.json
│   ├── osint_entity_linking.json
│   ├── osint_master_workflow.json
│   ├── import_workflows.sh
│   └── README.md
├── openwebui/
│   ├── osint_research_assistant.json
│   ├── threat_intel_analyst.json
│   ├── report_generator.json
│   └── README.md
└── README.md
```

## Usage

### n8n Workflows
1. Start the OSINT platform with Docker Compose
2. Access n8n at http://n8n.osint.local:5678
3. Import workflows using the import script:
   ```bash
   ./extensions/osint/workflows/n8n/import_workflows.sh
   ```
4. Execute workflows manually or via API

### OpenWebUI Presets
1. Start the OSINT platform with Docker Compose
2. Access OpenWebUI at http://openwebui.osint.local:3000
3. Import presets through the UI
4. Select appropriate assistants for tasks

### BeEF Integration
1. Access the OSINT extension in BeEF
2. Use the updated dashboard to access workflows
3. Execute workflows directly from the interface
4. Monitor workflow progress and results

## Benefits

1. **Automation**: Reduce manual OSINT research tasks
2. **Consistency**: Standardized research processes
3. **Integration**: Seamless connection between tools
4. **Scalability**: Handle multiple research targets simultaneously
5. **Extensibility**: Easy to add new workflows and capabilities

## Future Enhancements

1. **Advanced Workflows**: More sophisticated research workflows
2. **Custom Nodes**: Specialized n8n nodes for OSINT tasks
3. **Workflow Templates**: Pre-built templates for common research scenarios
4. **Scheduling**: Automated workflow execution based on triggers
5. **Monitoring**: Enhanced workflow monitoring and alerting