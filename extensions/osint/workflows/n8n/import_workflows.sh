#!/bin/bash

# Script to import n8n workflows

# Check if n8n is running
if ! curl -s http://localhost:5678/rest/health > /dev/null; then
    echo "n8n is not running. Please start n8n first."
    exit 1
fi

# Import workflows
echo "Importing OSINT workflows into n8n..."

# Import domain research workflow
curl -X POST http://localhost:5678/rest/workflows \
  -H "Content-Type: application/json" \
  -d @extensions/osint/workflows/n8n/osint_domain_research.json

# Import email research workflow
curl -X POST http://localhost:5678/rest/workflows \
  -H "Content-Type: application/json" \
  -d @extensions/osint/workflows/n8n/osint_email_research.json

# Import person research workflow
curl -X POST http://localhost:5678/rest/workflows \
  -H "Content-Type: application/json" \
  -d @extensions/osint/workflows/n8n/osint_person_research.json

# Import entity linking workflow
curl -X POST http://localhost:5678/rest/workflows \
  -H "Content-Type: application/json" \
  -d @extensions/osint/workflows/n8n/osint_entity_linking.json

# Import master workflow
curl -X POST http://localhost:5678/rest/workflows \
  -H "Content-Type: application/json" \
  -d @extensions/osint/workflows/n8n/osint_master_workflow.json

echo "Workflows imported successfully!"