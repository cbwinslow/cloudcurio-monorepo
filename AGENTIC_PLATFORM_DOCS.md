# CloudCurio Agentic Platform - Developer Documentation

## Overview

The CloudCurio Agentic Platform is a sophisticated multi-agent system designed to automate complex development tasks using AI agents and CrewAI orchestration. It provides a framework for creating, configuring, and managing teams of AI agents that can work together on various tasks.

## Architecture

### Core Components

#### 1. CloudCurioAgenticPlatform Class
The main platform class that manages all agentic operations:

```python
class CloudCurioAgenticPlatform:
    def __init__(self):
        self.agents = {}           # Agent registry
        self.tasks = {}            # Task registry  
        self.crews = {}            # Crew registry
        self.sysmon = SysMon()     # System monitoring integration
        self.active_sessions = []  # Active sessions
        
    def create_custom_agent(...) -> Agent
    def create_crew_from_config(...) -> Tuple[str, Crew]
    def create_agentic_task(...) -> str
    def execute_task(...) -> AgenticTask
    def run_crew(...) -> Any
    def create_custom_crew(...) -> Tuple[str, Crew]
```

#### 2. AgenticTask Data Class
Structure for tracking individual tasks:

```python
@dataclass
class AgenticTask:
    id: str
    name: str
    description: str
    assigned_agent: str
    priority: str  # low, medium, high, critical
    status: str    # pending, running, completed, failed
    created_at: datetime
    completed_at: Optional[datetime] = None
    result: Optional[str] = None
    error: Optional[str] = None
```

#### 3. AgenticCLI Class
Command-line interface for platform management:

```python
class AgenticCLI:
    def __init__(self):
        self.platform = CloudCurioAgenticPlatform()
        
    def run(self)  # Main CLI loop
    def list_agents(self) -> List[str]
    def list_crews(self) -> List[str]
    def create_crew(self, crew_type: str)
    def run_crew(self, crew_id: str)
    # ... other commands
```

## Agent System

### Default Agents

#### Code Analyst Agent
- **Role**: Analyze codebases to understand structure and functionality
- **Goal**: Examine codebases in detail, identifying components and interactions
- **Backstory**: Expert software engineer with extensive code analysis experience
- **Tools**: File reading, code searching, system info

#### Documentation Specialist Agent  
- **Role**: Create comprehensive documentation from codebase analysis
- **Goal**: Transform code analysis into clear, comprehensive documentation
- **Backstory**: Technical writer with deep expertise in developer documentation
- **Tools**: None (documentation generation)

#### QA Engineer Agent
- **Role**: Review generated documentation for accuracy and completeness
- **Goal**: Ensure documentation accurately reflects codebase and procedures
- **Backstory**: QA engineer with experience in code review and documentation
- **Tools**: None (review and validation)

#### System Monitor Agent
- **Role**: Monitor system changes and configuration updates
- **Goal**: Maintain accurate view of system state and changes
- **Backstory**: System monitoring expert tracking package installations, service modifications
- **Tools**: System info, package checker

### Creating Custom Agents

```python
# Using the platform's built-in method
agent = platform.create_custom_agent(
    name="my_custom_agent",
    role="Custom Role",
    goal="Perform specific task",
    backstory="Agent background and expertise",
    llm_provider="openrouter",
    model="mistralai/mistral-7b-instruct"
)

# Using CrewAI directly with tracking
from feature_tracking.feature_tracker import track_feature, FeatureCategory

@track_feature("custom_agent_creation", FeatureCategory.AGENT_PLATFORM)
def create_specialized_agent():
    agent = Agent(
        role="Specialized Role",
        goal="Specific goal for this agent",
        backstory="Detailed background for the agent",
        verbose=True,
        allow_delegation=False,
        llm=ChatOpenAI(model="gpt-4")
    )
    return agent
```

## Crew System

### Configuration-Based Crews

Crews can be defined using JSON configuration files:

```json
{
  "name": "Code Review Crew",
  "description": "Reviews codebases and generates documentation",
  "agents": ["code_analyst", "documentation_specialist", "qa_engineer"],
  "tasks": [
    {
      "name": "code_analysis",
      "description": "Analyze the codebase structure and components",
      "expected_output": "Detailed analysis of the codebase",
      "agent": "code_analyst"
    },
    {
      "name": "documentation_creation", 
      "description": "Create comprehensive documentation based on code analysis",
      "expected_output": "Complete documentation files",
      "agent": "documentation_specialist",
      "context": ["code_analysis"]
    },
    {
      "name": "quality_assurance",
      "description": "Review the created documentation for accuracy", 
      "expected_output": "Review with feedback",
      "agent": "qa_engineer",
      "context": ["code_analysis", "documentation_creation"]
    }
  ],
  "process": "sequential",
  "verbose": 2
}
```

### Creating and Running Crews

```python
# Create crew from configuration
crew_id, crew = platform.create_crew_from_config("code_review_crew")

# Run the crew
result = platform.run_crew(crew_id)

# Create custom crew programmatically
crew_id, crew = platform.create_custom_crew(
    name="custom_crew",
    agents=["code_analyst", "documentation_specialist"],
    tasks=[
        {
            "description": "Perform custom analysis",
            "expected_output": "Analysis results",
            "agent": "code_analyst"
        },
        {
            "description": "Create custom documentation", 
            "expected_output": "Documentation files",
            "agent": "documentation_specialist"
        }
    ]
)
```

## Task Management System

### Creating Tasks

```python
# Create a new task for the agentic system
task_id = platform.create_agentic_task(
    name="analyze_project_structure",
    description="Analyze the CloudCurio project structure and dependencies", 
    agent_name="code_analyst",
    priority="high"
)

# Execute a specific task
task = await platform.execute_task(task_id)
```

### Task Lifecycle

Tasks go through the following states:
1. **Pending**: Task created but not started
2. **Running**: Task is currently executing
3. **Completed**: Task finished successfully  
4. **Failed**: Task encountered an error

## Local AI Integration

### Ollama Support

The platform includes support for local AI models via Ollama:

```python
class LocalAIAgent:
    def __init__(self, model: str = "llama3"):
        self.model = model
        self.api_base = "http://localhost:11434/api/generate"
    
    def generate(self, prompt: str) -> str:
        # Generate response using local AI
        # Falls back to API-based model if Ollama unavailable
        pass
```

### Multi-Provider Support

The platform supports multiple AI providers:

- **OpenRouter**: Access to multiple models
- **OpenAI**: GPT models
- **Google Gemini**: Gemini models  
- **Ollama**: Local open-source models
- **LocalAI**: OpenAI-compatible local API
- **Alibaba Qwen**: Qwen series models
- **Anthropic**: Claude models
- And 10+ more providers

## Integration with Feature Tracking

### Tracked Operations

The agentic platform is fully integrated with the feature tracking system:

```python
@track_feature("agent_execution", FeatureCategory.AGENT_PLATFORM)
def execute_agent_task(agent_name: str, task_description: str):
    # Agent execution logic
    return result

@track_feature("crew_coordination", FeatureCategory.AGENT_PLATFORM) 
def coordinate_crew_agents(crew_id: str, tasks: list):
    # Crew coordination logic
    return result
```

### Metrics Tracked

For each agentic operation, the system tracks:
- Execution time and success status
- Number of agents involved
- Total tokens used (estimated)
- Input/output sizes
- Efficiency scores
- Error information
- User context and session data

## CLI Interface

### Available Commands

#### Agent Management
```
list-agents - List all available agents
create-agent <name> <role> <goal> <backstory> - Create a custom agent
```

#### Crew Management  
```
list-crews - List all available crews
create-crew <crew_type> - Create a crew from configuration
run-crew <crew_id> - Run a specific crew
```

#### Task Management
```
list-tasks - List all tasks
create-task <name> <description> <agent> - Create a new task
execute-task <task_id> - Execute a specific task
```

### CLI Usage Example

```bash
python agentic_platform.py

CloudCurio Agentic Platform
=========================

Available commands:
1. list-agents - List all available agents
2. list-crews - List all available crews  
3. create-crew <crew_type> - Create a crew from configuration
4. run-crew <crew_id> - Run a specific crew
5. create-task <name> <description> <agent> - Create a new task
6. list-tasks - List all tasks
7. execute-task <task_id> - Execute a specific task
8. create-agent <name> <role> <goal> <backstory> - Create a custom agent
9. exit - Exit the platform

Enter command: list-agents
Available agents: code_analyst, documentation_specialist, qa_engineer, sys_monitor
```

## Configuration Management

### Agent Configuration Files

Agents can be configured using JSON files in `agentic_configs/`:

```json
{
    "role": "Code Analyst",
    "goal": "Analyze codebases to understand structure, components, and functionality",
    "backstory": "Expert software engineer with extensive experience in code analysis",
    "tools": ["list_files", "read_file", "search_codebase"],
    "max_iter": 15,
    "max_rpm": 100
}
```

### Crew Configuration Files

Crews are defined in configuration files that specify:
- Agent composition
- Task sequences and dependencies
- Execution process (sequential, hierarchical)
- Verbosity level

## Performance Considerations

### Resource Management
- Agents are created on-demand to minimize memory usage
- Crew execution is asynchronous where possible
- API call rates are managed with rate limiting
- Local models reduce external dependencies

### Caching
- API responses can be cached to reduce costs
- Agent configurations are cached after loading
- Task results can be cached for repeated operations

### Error Handling
- Graceful fallbacks for API failures
- Local model fallback when cloud services unavailable
- Comprehensive error logging and reporting
- Automatic retry with exponential backoff

## Security Features

### Credential Management
- Secure credential storage with GPG encryption
- Environment variable isolation
- API key rotation support
- Secure credential access patterns

### Data Privacy
- Local processing where possible
- No data transmission by default
- Configurable privacy settings
- Anonymization options

## Extensibility

### Adding New Agents
1. Define agent configuration in JSON
2. Register with the platform
3. Add to relevant crews
4. Test with sample tasks

### Adding New Crews
1. Create crew configuration file
2. Define agent-task relationships
3. Specify execution process
4. Test with various inputs

### Adding New Tools
1. Implement tool function with proper annotations
2. Add to agent configuration
3. Test tool functionality
4. Update documentation

## Testing Strategy

### Unit Tests
```python
def test_agent_creation():
    platform = CloudCurioAgenticPlatform()
    agent = platform.create_custom_agent(
        "test_agent", "Test Role", "Test Goal", "Test Backstory"
    )
    assert agent.role == "Test Role"
    
def test_crew_execution():
    platform = CloudCurioAgenticPlatform() 
    crew_id, crew = platform.create_crew_from_config("code_review_crew")
    result = platform.run_crew(crew_id)
    assert result is not None
```

### Integration Tests
- End-to-end crew operations
- Multi-agent coordination scenarios
- API integration tests
- Local AI model integration tests

### Performance Tests
- Agent creation overhead
- Crew execution time
- Memory usage under load
- API rate limiting behavior

## Troubleshooting

### Common Issues

#### Agent Not Found
```
Error: Agent 'unknown_agent' not found
Solution: Check if agent is registered in platform.agents dictionary
```

#### API Key Issues  
```
Error: API key not configured
Solution: Add API key via CLI or environment variable
```

#### Local Model Unavailable
```
Error: Ollama service not available
Solution: Start Ollama service: ollama serve
```

### Debugging Commands
```
# Enable verbose logging
export LOG_LEVEL=DEBUG

# Check agent status
python agentic_platform.py --check-agents

# List available models
curl http://localhost:11434/api/tags
```

## Best Practices

### Agent Design
1. **Clear Roles**: Define specific, non-overlapping roles
2. **Descriptive Goals**: State specific, measurable objectives
3. **Detailed Backstories**: Provide comprehensive context
4. **Appropriate Tools**: Assign only necessary tools

### Crew Design
1. **Logical Task Flow**: Arrange tasks in sensible sequence
2. **Clear Dependencies**: Define task relationships explicitly
3. **Balanced Workload**: Distribute work appropriately
4. **Error Handling**: Plan for failure scenarios

### Security
1. **Credential Management**: Use secure storage for API keys
2. **Rate Limiting**: Respect API limits
3. **Data Privacy**: Process sensitive data locally when possible
4. **Access Control**: Implement appropriate access controls

### Performance
1. **Efficient Tool Usage**: Minimize unnecessary API calls
2. **Caching**: Cache results when appropriate
3. **Resource Management**: Monitor memory and CPU usage
4. **Asynchronous Execution**: Use async where possible

## Future Enhancements

### Planned Features
- Advanced agent memory systems
- Dynamic crew composition
- Multi-modal AI support
- Advanced planning and reasoning
- Distributed agent networks
- Real-time collaboration
- Advanced analytics and insights

### Scalability Improvements
- Container orchestration
- Microservice architecture
- Distributed task queues
- Horizontal scaling support

This documentation provides comprehensive guidance for developing, maintaining, and extending the CloudCurio Agentic Platform.