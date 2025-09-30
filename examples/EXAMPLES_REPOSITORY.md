# CloudCurio Examples Repository

This directory contains practical examples for using CloudCurio tools.

## Table of Contents
1. [AI Provider Examples](#ai-provider-examples)
2. [MCP Server Examples](#mcp-server-examples)
3. [SysMon Examples](#sysmon-examples)
4. [Configuration Editor Examples](#configuration-editor-examples)
5. [Docker Examples](#docker-examples)
6. [Integration Examples](#integration-examples)

## AI Provider Examples

### Example 1: Multi-Provider Comparison
```python
# File: examples/ai/multi_provider_comparison.py
from ai_tools.ai_provider import ai_manager

def compare_responses(prompt):
    """Compare responses from different AI providers"""
    providers_to_test = ["openrouter", "openai", "gemini"]
    
    results = {}
    for provider in providers_to_test:
        try:
            if ai_manager.is_provider_available(provider):
                response = ai_manager.generate_with_provider(prompt, provider_name=provider)
                results[provider] = response
                print(f"{provider}: {len(response)} characters")
            else:
                results[provider] = "Not available"
                print(f"{provider}: Not available")
        except Exception as e:
            results[provider] = f"Error: {str(e)}"
            print(f"{provider}: Error - {str(e)}")
    
    return results

# Usage
prompt = "Explain the benefits of containerization in modern software development"
responses = compare_responses(prompt)

for provider, response in responses.items():
    print(f"\n{provider.upper()} RESPONSE:")
    print(response[:500] + "..." if len(response) > 500 else response)
```

### Example 2: Secure Credential Management
```python
# File: examples/ai/secure_credentials.py
from ai_tools.config_manager import global_config_manager

# Add a new API key securely
global_config_manager.add_api_key("openrouter", "your-api-key-here")

# Get a stored API key
api_key = global_config_manager.get_api_key("openrouter")
if api_key:
    print("API key retrieved successfully")
else:
    print("API key not found")

# List all configured providers
configured = global_config_manager.list_configured_providers()
print(f"Configured providers: {configured}")
```

## MCP Server Examples

### Example 1: Starting Different Crew Types
```bash
# File: examples/mcp/start_crews.sh

#!/bin/bash

MCP_SERVER="http://localhost:8000"

echo "Starting Code Review Crew..."
curl -X POST $MCP_SERVER/crews/start \
  -H "Content-Type: application/json" \
  -d '{
    "crew_type": "code_review",
    "input_data": {
      "repository_path": "/path/to/repository"
    }
  }' | jq

echo "Starting Documentation Crew..."
curl -X POST $MCP_SERVER/crews/start \
  -H "Content-Type: application/json" \
  -d '{
    "crew_type": "documentation", 
    "input_data": {
      "repository_path": "/path/to/repository"
    }
  }' | jq

echo "Starting Vulnerability Assessment Crew..."
curl -X POST $MCP_SERVER/crews/start \
  -H "Content-Type: application/json" \
  -d '{
    "crew_type": "vulnerability_assessment",
    "input_data": {
      "repository_path": "/path/to/repository"
    }
  }' | jq
```

### Example 2: Checking Crew Status
```python
# File: examples/mcp/check_status.py
import requests
import time

def monitor_crew(crew_id, mcp_server="http://localhost:8000"):
    """Monitor a crew until completion"""
    url = f"{mcp_server}/crews/{crew_id}"
    
    while True:
        response = requests.get(url)
        data = response.json()
        
        print(f"Status: {data['status']}")
        
        if data['status'] in ['completed', 'failed']:
            print("Final result:")
            print(f"Status: {data['status']}")
            if data['result']:
                print(f"Result: {data['result']}")
            if data['error']:
                print(f"Error: {data['error']}")
            break
        
        time.sleep(5)  # Check every 5 seconds

# Usage
# monitor_crew("your-crew-id-here")
```

## SysMon Examples

### Example 1: Creating Configuration Snapshots
```python
# File: examples/sysmon/create_snapshot.py
from sysmon.sysmon import SysMon

def create_dev_environment_snapshot():
    """Create a snapshot of the current development environment"""
    sysmon = SysMon()
    
    # Create a named snapshot
    snapshot_name = "dev_environment_20231020"
    snapshot_path = sysmon.create_configuration_snapshot(snapshot_name)
    
    print(f"Snapshot created: {snapshot_path}")
    
    # List installed packages
    import json
    packages_path = f"{snapshot_path}/packages.json"
    with open(packages_path) as f:
        packages = json.load(f)
        print(f"Python packages: {len(packages.get('pip', []))}")
        print(f"System packages: {len(packages.get('apt', [])) if packages.get('apt') else 0}")

# Usage
create_dev_environment_snapshot()
```

### Example 2: Generating Reproduction Scripts
```bash
# File: examples/sysmon/generate_reproduction.sh

#!/bin/bash

# Create a snapshot
SNAPSHOT_NAME="production_setup"
python -c "from sysmon.sysmon import SysMon; SysMon().create_configuration_snapshot('$SNAPSHOT_NAME')"

# Generate reproduction script
OUTPUT_SCRIPT="reproduce_${SNAPSHOT_NAME}.sh"
python -c "from sysmon.sysmon import SysMon, ReproductionEngine; e = ReproductionEngine(f'~/.cloudcurio/snapshots/{SNAPSHOT_NAME}'); e.generate_bash_script('$OUTPUT_SCRIPT')"

echo "Reproduction script generated: $OUTPUT_SCRIPT"
echo "Important: Review the script before running it!"
```

## Configuration Editor Examples

### Example 1: Web Automation Recording
```python
# File: examples/config_editor/record_automation.py
import asyncio
from config_editor.config_editor import PuppeteerController

async def record_api_key_creation():
    """Demonstrate how to record an API key creation process"""
    controller = PuppeteerController()
    
    # Start recording
    session_id = f"api_key_session_{int(time.time())}"
    await controller.start_recording(session_id)
    
    # User would now perform actions in the browser
    # These would be automatically recorded
    
    # Stop recording after user completes the task
    await controller.stop_recording()
    
    print(f"Recorded actions for session: {session_id}")

# Note: This is a conceptual example - actual implementation would
# require the user to interact with the Puppeteer-controlled browser
```

## Docker Examples

### Example 1: MCP Server Container
```dockerfile
# File: examples/docker/mcp_server.Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY crew/mcp_server/requirements.txt /app/crew/mcp_server/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r crew/mcp_server/requirements.txt

# Copy project
COPY . /app/

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "-m", "uvicorn", "crew.mcp_server.server:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Example 2: Multi-Service Deployment
```yaml
# File: examples/docker/docker-compose.yml
version: '3.8'

services:
  mcp-server:
    build:
      context: .
      dockerfile: Dockerfile.mcp
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/cloudcurio
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
    depends_on:
      - db

  config-editor:
    build:
      context: .
      dockerfile: Dockerfile.config-editor
    ports:
      - "8081:8081"
    depends_on:
      - mcp-server

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: cloudcurio
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

## Integration Examples

### Example 1: AI Tool Integration in MCP Server
```python
# Conceptual example showing how AI providers integrate with MCP
# File: examples/integration/ai_mcp_integration.py

from ai_tools.ai_provider import ai_manager
from crewai import Agent, Task, Crew

def create_dynamic_crew(provider_config):
    """Create a crew using a specific AI provider"""
    
    # Create an agent using the specified provider
    # In a real implementation, this would require creating 
    # LangChain-compatible wrappers for each provider
    llm = ai_manager.get_provider(provider_config['provider'])
    
    # Example agent creation (simplified)
    agent = Agent(
        role=provider_config['role'],
        goal=provider_config['goal'],
        backstory=provider_config['backstory'],
        verbose=True,
        allow_delegation=False,
        # Note: This is pseudocode - would need LangChain wrappers
        llm=llm  
    )
    
    # Create and run the crew
    task = Task(
        description=provider_config['task_description'],
        agent=agent,
        expected_output=provider_config['expected_output']
    )
    
    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=2
    )
    
    result = crew.kickoff()
    return result

# Usage example
config = {
    'provider': 'openrouter',
    'role': 'Code Reviewer',
    'goal': 'Analyze Python code quality',
    'backstory': 'You are an expert Python developer...',
    'task_description': 'Review the provided code for quality issues',
    'expected_output': 'List of code quality issues and suggestions'
}

# result = create_dynamic_crew(config)
```

### Example 2: Complete Workflow Example
```python
# File: examples/integration/complete_workflow.py
"""
Complete CloudCurio workflow example:
1. Monitor system for changes
2. Use AI to analyze and document changes
3. Create configuration snapshot
4. Generate reproduction script
"""

from sysmon.sysmon import SysMon
from ai_tools.ai_provider import ai_manager

def complete_documentation_workflow():
    """Complete workflow example"""
    
    print("Starting complete documentation workflow...")
    
    # 1. Initialize components
    sysmon = SysMon()
    print("✓ SysMon initialized")
    
    # 2. Check for recent changes
    sysmon.command_tracker.check_for_changes()
    print("✓ System changes detected")
    
    # 3. Get recent events
    events = sysmon.get_recent_events(limit=10)
    print(f"✓ Found {len(events)} recent events")
    
    if events:
        # 4. Use AI to analyze changes
        event_descriptions = [f"{e.event_type.value}: {e.details}" for e in events[:5]]
        prompt = f"Summarize these system changes: {', '.join(event_descriptions)}"
        
        try:
            ai_summary = ai_manager.generate(prompt)
            print(f"✓ AI summary generated: {ai_summary[:100]}...")
        except Exception as e:
            print(f"⚠ AI analysis failed: {e}")
    
    # 5. Create configuration snapshot
    snapshot_name = "workflow_snapshot"
    snapshot_path = sysmon.create_configuration_snapshot(snapshot_name)
    print(f"✓ Configuration snapshot created: {snapshot_path}")
    
    print("Complete workflow finished successfully!")

# Run the workflow
if __name__ == "__main__":
    complete_documentation_workflow()
```