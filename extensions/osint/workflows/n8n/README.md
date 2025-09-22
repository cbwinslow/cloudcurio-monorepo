# OSINT Workflows

This directory contains n8n workflows for automating OSINT research tasks.

## Workflow Types

### 1. Domain Research Workflow
- Searches for domain-related information
- Validates domain registration
- Stores findings in the database
- Updates the knowledge graph

### 2. Email Research Workflow
- Validates email addresses
- Analyzes social engineering risks
- Updates the knowledge graph with email information

### 3. Person Research Workflow
- Searches social media for person information
- Finds associated domains
- Generates comprehensive profiles
- Updates the knowledge graph

### 4. Entity Linking Workflow
- Identifies relationships between entities
- Analyzes connection nature
- Creates relationships in the knowledge graph

### 5. Master Workflow
- Orchestrates all other workflows
- Generates comprehensive reports

## Usage

1. Import workflows into n8n
2. Configure API endpoints and database connections
3. Execute workflows manually or via API triggers
4. Monitor progress through the n8n interface

## Integration Points

- **SearxNG**: For web searches
- **LocalAI**: For AI analysis and generation
- **Neo4j**: For knowledge graph storage
- **PostgreSQL**: For relational data storage
- **AI Agents**: For report generation

## Customization

Workflows can be customized by:
- Adding new data sources
- Modifying AI analysis prompts
- Extending entity types
- Adding new relationship types