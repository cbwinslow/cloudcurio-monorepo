# CloudCurio Feature Tracking System

The CloudCurio Feature Tracking System provides comprehensive monitoring, measurement, and analysis of feature usage across the entire CloudCurio platform. It tracks performance metrics, success rates, efficiency scores, and usage patterns for all platform features.

## 📊 Features

- **Comprehensive Tracking**: Monitor usage, performance, and effectiveness of all features
- **Performance Metrics**: Measure execution time, efficiency, success rates, and resource usage
- **Category-Based Organization**: Organize features by functional categories
- **Real-time Dashboard**: Visualize metrics through an interactive web dashboard
- **Command-Line Interface**: Query and analyze tracking data from the terminal
- **Decorator-Based Integration**: Easy integration with existing code using decorators
- **Manual Tracking Support**: Track complex operations with custom parameters
- **Privacy-Focused**: Options to anonymize user data and exclude sensitive features

## 🏗️ Architecture

```
feature_tracking/
├── feature_tracker.py     # Core tracking library
├── config.py             # Configuration system
├── cli.py                # Command-line interface
├── dashboard.py          # Web dashboard server
├── integration_examples.py # Integration examples
├── setup_integration.py   # Integration setup script
└── README.md             # This documentation
```

## 🚀 Quick Start

### Installation
The feature tracking system is included with CloudCurio:

```bash
# If using from source
pip install -e .

# The tracking system is available by default
```

### Basic Usage

#### 1. Decorator-Based Tracking

```python
from feature_tracking.feature_tracker import track_feature, FeatureCategory

@track_feature("my_feature", FeatureCategory.AI_PROVIDER)
def my_function(param1, param2):
    # Your function logic here
    return "result"
```

#### 2. Manual Tracking for Complex Operations

```python
from feature_tracking.feature_tracker import feature_tracker, FeatureStatus

# Start tracking
record_id = feature_tracker.start_custom_tracking(
    "complex_operation", 
    FeatureCategory.SYSMON,
    user_id="user123",
    metadata={"operation_type": "data_analysis"}
)

try:
    # Perform complex operation
    result = perform_operation()
    
    # Complete tracking with success
    feature_tracker.complete_custom_tracking(
        record_id,
        status=FeatureStatus.SUCCESS,
        input_size=len(str(input_data)),
        output_size=len(str(result)),
        efficiency_score=0.95
    )
except Exception as e:
    # Complete tracking with failure
    feature_tracker.complete_custom_tracking(
        record_id,
        status=FeatureStatus.FAILED,
        error_message=str(e),
        efficiency_score=0.0
    )
```

## 📈 Dashboard

Start the web dashboard to visualize tracking data:

```bash
# Start the dashboard server
python -m feature_tracking.dashboard

# Access at: http://localhost:8081
```

The dashboard shows:

- Overall usage statistics
- Feature usage by category
- Top features by usage count
- Recent feature calls
- Performance metrics and efficiency scores

## 🖥️ Command-Line Interface

Query tracking data from the command line:

```bash
# List top features by usage
python -m feature_tracking.cli list-features --limit 10

# Get statistics for a specific feature
python -m feature_tracking.cli feature-stats my_feature --category ai_provider

# List recent feature calls
python -m feature_tracking.cli list-records --limit 20

# Filter by category
python -m feature_tracking.cli list-records --category ai_provider --limit 10
```

## 🔧 Integration Examples

### AI Provider Tracking

```python
from feature_tracking.feature_tracker import track_feature, FeatureCategory

@track_feature("openrouter_query", FeatureCategory.AI_PROVIDER)
def query_openrouter(prompt: str, model: str = "mistralai/mistral-7b-instruct"):
    # AI query logic here
    return ai_response
```

### MCP Server Tracking

```python
from feature_tracking.feature_tracker import track_feature, FeatureCategory

@track_feature("crew_execution", FeatureCategory.MCP_SERVER)
def execute_crew(crew_type: str, config: dict):
    # Crew execution logic here
    return crew_result
```

### SysMon Tracking

```python
from feature_tracking.feature_tracker import track_feature, FeatureCategory

@track_feature("config_snapshot", FeatureCategory.SYSMON)
def create_configuration_snapshot(name: str = None):
    # Configuration snapshot logic here
    return snapshot_path
```

## ⚙️ Configuration

The feature tracking system can be configured through environment variables:

```bash
# Enable/disable tracking
FEATURE_TRACKING_ENABLED=true

# Track only failures
FEATURE_TRACKING_FAILURES_ONLY=false

# Minimum duration threshold (in seconds)
FEATURE_TRACKING_MIN_DURATION=0.0

# Maximum metadata size (in bytes)
FEATURE_TRACKING_MAX_METADATA_SIZE=10240

# Anonymize user data
FEATURE_TRACKING_ANONYMIZE=true

# Features to exclude from tracking (comma-separated)
FEATURE_TRACKING_EXCLUDE=api_keys,passwords

# Flush interval (batch records)
FEATURE_TRACKING_FLUSH_INTERVAL=100

# Maximum batch size
FEATURE_TRACKING_MAX_BATCH_SIZE=50
```

## 📊 Metrics Tracked

For each feature execution, the system captures:

- **Execution Time**: Duration of the feature execution
- **Success Status**: Success, failure, partial, or timeout
- **Input/Output Size**: Size of input and output data
- **Efficiency Score**: Calculated efficiency based on time, output, and iterations
- **Metadata**: Function parameters, thread ID, and custom metadata
- **User Context**: User ID and session ID (configurable)
- **Error Information**: Error messages for failed executions
- **Iteration Count**: Number of iterations for complex operations

## 🏷️ Feature Categories

Features are organized into categories:

- `AI_PROVIDER`: AI model interactions
- `MCP_SERVER`: Model Context Protocol server operations
- `SYSMON`: System monitoring and tracking
- `CONFIG_EDITOR`: Configuration management
- `AGENT_PLATFORM`: Multi-agent operations
- `WEB_INTERFACE`: Web interface interactions
- `TERMINAL_TOOL`: Terminal tool operations
- `FILE_OPERATION`: File system operations
- `DATABASE_OPERATION`: Database operations
- `OTHER`: Uncategorized features

## 📊 Available Statistics

The system provides various statistics:

- **Total Calls**: Number of times a feature was called
- **Success Rate**: Percentage of successful executions
- **Average Duration**: Average execution time
- **Average Efficiency**: Average calculated efficiency score
- **Failure Count**: Number of failed executions
- **Top Features**: Features with highest usage

## 🛡️ Privacy & Security

- **Anonymization**: User IDs can be hashed to protect privacy
- **Exclusion List**: Sensitive features can be excluded from tracking
- **Local Storage**: All tracking data stored locally by default
- **Configurable**: Extensive configuration options for privacy requirements

## 🤖 Agentic Platform Integration

For the agentic platform, tracking is especially valuable:

```python
from feature_tracking.feature_tracker import track_feature, FeatureCategory

@track_feature("agent_execution", FeatureCategory.AGENT_PLATFORM)
def execute_agent_task(agent_name: str, task_description: str):
    # Agent task execution
    return result

@track_feature("crew_coordination", FeatureCategory.AGENT_PLATFORM) 
def coordinate_crew_agents(crew_id: str, tasks: list):
    # Crew coordination logic
    return result
```

## 🚀 Deployment

The feature tracking system is designed to work in all deployment environments:

- **Development**: Full tracking with detailed metrics
- **Staging**: Tracking with sampling for performance
- **Production**: Optimized tracking with privacy controls

## 📄 License

This feature tracking system is part of the CloudCurio platform and is licensed under the MIT License.