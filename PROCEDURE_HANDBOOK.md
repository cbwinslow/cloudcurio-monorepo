# CloudCurio Procedure Handbook

This handbook demonstrates how to use all CloudCurio tools with practical examples and proof of concept implementations.

## Table of Contents
1. [Quick Start Guide](#quick-start-guide)
2. [AI Provider Management](#ai-provider-management)
3. [System Monitoring (SysMon)](#system-monitoring-sysmon)
4. [Configuration Editor](#configuration-editor)
5. [MCP Server Usage](#mcp-server-usage)
6. [Docker Containerization](#docker-containerization)
7. [Task Management](#task-management)
8. [Troubleshooting](#troubleshooting)
9. [Examples Repository](#examples-repository)

## Quick Start Guide

### 1. Initial Setup
```bash
# Clone the repository
git clone https://github.com/cbwinslow/cloudcurio.git
cd cloudcurio

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r crew/requirements.txt
pip install -r config_editor/requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your API keys
```

### 2. Basic Usage Flow
1. Start the MCP server
2. Configure AI providers
3. Run system monitoring
4. Use web-based configuration editor
5. Create configuration snapshots

## AI Provider Management

### Example: Adding a New AI Provider
```python
# Example from our implementation
from ai_tools.ai_provider import ai_manager

# Test provider availability
if ai_manager.is_provider_available("openrouter"):
    print("OpenRouter is available")
    
    # Get available models
    models = ai_manager.get_provider_models("openrouter")
    print(f"Available models: {models[:5]}")
    
    # Generate with specific provider
    response = ai_manager.generate_with_provider(
        "Explain quantum computing", 
        provider_name="openrouter",
        model="google/gemini-pro"
    )
    print(response)
```

### Secure Credential Management
```bash
# Using the CLI tool
python -m ai_tools.cli add-credential openrouter
python -m ai_tools.cli list-providers
python -m ai_tools.cli set-default openrouter
```

## System Monitoring (SysMon)

### Example: Creating a Configuration Snapshot
```python
from sysmon.sysmon import SysMon

# Initialize the system monitor
sysmon = SysMon()

# Create a snapshot
snapshot_path = sysmon.create_configuration_snapshot("my-dev-setup")
print(f"Snapshot created at: {snapshot_path}")

# Generate reproduction script
script_path = sysmon.generate_reproduction_script("my-dev-setup", "reproduce_dev.sh")
print(f"Reproduction script at: {script_path}")
```

### Example: Monitoring System Changes
```bash
# Continuous monitoring
cloudcurio-sysmon monitor --continuous

# Check recent events
cloudcurio-sysmon events --limit 50

# View event types
cloudcurio-sysmon events --type package_install
```

## Configuration Editor

### Example: Recording Web Actions
```python
# In the configuration editor
from config_editor.config_editor import PuppeteerController

controller = PuppeteerController()
await controller.start_recording("api_key_creation_session")

# User performs actions in browser
# Actions are automatically recorded and classified

await controller.stop_recording()
```

### Example: Action Classification Output
```
Recorded action: Clicked on BUTTON element with class 'create-key-btn' containing 'Create API Key' (confidence: 0.87)
Classified as: API Key Creation
Grouped under: Google Cloud API Key Creation workflow
```

## MCP Server Usage

### Example: Starting a Crew via API
```bash
# Using curl to start a code review crew
curl -X POST http://localhost:8000/crews/start \
  -H "Content-Type: application/json" \
  -d '{
    "crew_type": "code_review",
    "config": {},
    "input_data": {
      "repository_path": "/path/to/codebase"
    }
  }'
```

### Example: API Response
```json
{
  "crew_id": "abc123-def456",
  "message": "Crew started successfully"
}
```

### Example: Checking Crew Status
```bash
curl http://localhost:8000/crews/abc123-def456
```

```json
{
  "crew_id": "abc123-def456",
  "crew_type": "code_review",
  "status": "running",
  "created_at": "2023-10-20T10:00:00Z",
  "started_at": "2023-10-20T10:01:00Z",
  "completed_at": null,
  "result": null,
  "error": null
}
```

## Docker Containerization

### Example: Building MCP Server Container
```bash
# Build the MCP server container
docker build -f Dockerfile.mcp -t cloudcurio-mcp .

# Run with environment variables
docker run -p 8000:8000 -e OPENROUTER_API_KEY=your_key_here cloudcurio-mcp
```

### Example: Docker Compose for Full Setup
```yaml
version: '3.8'

services:
  mcp-server:
    build:
      context: .
      dockerfile: Dockerfile.mcp
    ports:
      - "8000:8000"
    environment:
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - DEFAULT_AI_PROVIDER=openrouter

  config-editor:
    build:
      context: .
      dockerfile: Dockerfile.config-editor
    ports:
      - "8081:8081"
    depends_on:
      - mcp-server
```

## Task Management

### Example: Task Tracking Workflow
```
1. New feature request: "Add Azure OpenAI support"
2. Domain: AI
3. Priority: High (integrates with existing provider system)
4. Status: Not Started
5. Assigned: Primary Developer
6. Due: Next release (2 weeks)
7. Implementation:
   - Create AzureOpenAIProvider class
   - Add to provider manager
   - Create secure credential storage
   - Add to CLI tool
   - Update documentation
8. Testing: Verify with multiple Azure models
9. Completion: Update task list, archive task
```

## Troubleshooting

### Common Issues and Solutions

#### Issue: API Keys Not Working
**Symptoms**: Authentication errors when using AI providers
**Solution**: 
```bash
# Check if credentials are stored correctly
python -m ai_tools.cli list-providers

# Re-add the credential
python -m ai_tools.cli add-credential openrouter
```

#### Issue: MCP Server Won't Start
**Symptoms**: Server fails to start or crashes
**Solution**:
1. Check if required environment variables are set
2. Verify database connection
3. Check logs for specific error messages

#### Issue: SysMon High CPU Usage
**Symptoms**: System monitoring consuming too many resources
**Solution**: 
- Reduce monitoring frequency
- Filter out non-essential events
- Optimize log aggregation

## Examples Repository

### Example 1: Complete MCP Server Integration
```python
# Example from crew/mcp_server/server.py
@app.post("/crews/start")
async def start_crew(crew_request: CrewRequest, db: Session = Depends(get_db)):
    """Start a new crew with the specified configuration"""
    crew_id = generate_crew_id()
    
    # Validate crew_type
    if crew_request.crew_type not in ["code_review", "documentation", "vulnerability_assessment"]:
        raise HTTPException(status_code=400, detail="Invalid crew type")
    
    # Create crew record in database
    crew_run = CrewRun(
        crew_id=crew_id,
        crew_type=crew_request.crew_type,
        status="pending",
        config=crew_request.config,
        input_data=crew_request.input_data,
        created_at=datetime.utcnow()
    )
    
    db.add(crew_run)
    db.commit()
    db.refresh(crew_run)
    
    # Run the crew in the background
    asyncio.create_task(run_crew_async(crew_id, crew_request, crew_run.created_at))
    
    return {"crew_id": crew_id, "message": "Crew started successfully"}
```

### Example 2: AI Provider Integration
```python
# Example from ai_tools/ai_provider.py
class OpenRouterProvider(BaseAIProvider):
    def generate(self, prompt: str, **kwargs) -> str:
        if not self.is_available():
            raise ValueError("OpenRouter API key not configured")
        
        import requests
        
        model = kwargs.get("model", self.default_model)
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
        }
        data.update({k: v for k, v in kwargs.items() if k != "model"})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(f"{self.base_url}/chat/completions", json=data, headers=headers)
        response.raise_for_status()
        
        return response.json()["choices"][0]["message"]["content"]
```

### Example 3: Action Recording and Classification
```python
# Example from config_editor/config_editor.py
async def _on_click(self, element):
    """Handle click events"""
    if not self.is_recording:
        return
    
    try:
        # Get element information
        tag_name = await element.getProperty('tagName')
        class_name = await element.getProperty('className')
        text_content = await element.getProperty('textContent')
        
        tag_name_val = await tag_name.jsonValue()
        class_name_val = await class_name.jsonValue() if class_name else ""
        text_content_val = await text_content.jsonValue() if text_content else ""
        
        # Create action description
        description = f"Clicked on {tag_name_val} element"
        if class_name_val:
            description += f" with class '{class_name_val}'"
        if text_content_val.strip():
            description += f" containing '{text_content_val.strip()[:50]}...'"
        
        # Determine action type based on context
        url = await self.current_page.url()
        action_type = self._determine_action_type(description, url)
        
        # Classify the action
        category, confidence = self.action_classifier.classify_action(description)
        
        # Record the action
        action = RecordedAction(
            id=None,
            action_type=action_type,
            timestamp=datetime.now(),
            description=description,
            url=url,
            selector=None,
            data={
                "tag_name": tag_name_val,
                "class_name": class_name_val,
                "text_content": text_content_val
            },
            session_id=self.session_id,
            step_group=category if confidence > 0.5 else None,
            confidence=confidence
        )
        
        action_id = self.action_db.insert_action(action)
        action.id = action_id
        
        self.recorded_actions.append(action)
        logger.info(f"Recorded action: {description} (confidence: {confidence:.2f})")
    except Exception as e:
        logger.error(f"Error recording click action: {e}")
```

## Proof of Concept Demonstrations

### POC 1: Automated API Key Creation
**Scenario**: User needs to create a Google Cloud API key
**Process**:
1. User starts recording in config editor
2. User navigates to Google Cloud Console
3. User follows standard process to create API key
4. System records each step and classifies as "API Key Creation"
5. System identifies this as a common task and creates a reusable workflow
6. Future API key creation can be automated using this workflow

### POC 2: System Reproduction
**Scenario**: Need to reproduce development environment on a new machine
**Process**:
1. Use SysMon to create a snapshot of the current system
2. Generate reproduction script
3. Run script on new machine to recreate the exact environment
4. Includes packages, services, configurations, and user settings

### POC 3: Multi-Provider AI Requests
**Scenario**: Need to compare responses across different AI providers
**Process**:
1. Send identical request to multiple providers simultaneously
2. Collect and compare responses
3. Rate responses based on quality, speed, and cost
4. Store results for future reference
5. Automatically select best provider for similar requests

## Best Practices

1. **Security First**: Always store credentials securely using GPG encryption
2. **Modular Design**: Keep components independent for easy testing and maintenance
3. **Documentation**: Document everything with examples
4. **Testing**: Write tests for all critical functionality
5. **Monitoring**: Implement comprehensive logging and monitoring
6. **Version Control**: Use proper branching and tagging strategies
7. **Configuration Management**: Keep configuration separate from code
8. **Error Handling**: Implement comprehensive error handling and recovery