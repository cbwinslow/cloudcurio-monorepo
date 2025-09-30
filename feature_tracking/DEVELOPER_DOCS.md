# CloudCurio Feature Tracking System - Developer Documentation

## Overview

The CloudCurio Feature Tracking System provides comprehensive monitoring and analysis capabilities for all platform features. It enables data-driven insights into feature usage, performance, and effectiveness across the entire CloudCurio ecosystem.

## Architecture

### Core Components

#### 1. FeatureTracker Class
The main class that manages all tracking operations:

```python
class FeatureTracker:
    def __init__(self, db_path: str = "~/.cloudcurio/feature_tracking.db")
    def track_feature(...) -> Callable  # Decorator factory
    def start_custom_tracking(...) -> str  # Manual tracking start
    def complete_custom_tracking(...)  # Manual tracking completion
    def get_feature_stats(...) -> Dict  # Statistics retrieval
    def get_all_records(...) -> List[FeatureUsageRecord]  # Record retrieval
```

#### 2. FeatureUsageRecord Data Class
Data structure for storing feature usage information:

```python
@dataclass
class FeatureUsageRecord:
    record_id: str
    feature_name: str
    category: FeatureCategory
    status: FeatureStatus
    duration: float
    start_time: datetime
    end_time: datetime
    input_size: int
    output_size: int
    metadata: Dict[str, Any]
    user_id: Optional[str]
    session_id: str
    error_message: Optional[str] = None
    efficiency_score: Optional[float] = None
    iterations: int = 1
```

#### 3. FeatureTrackerDB Class
Database manager for persistent storage:

```python
class FeatureTrackerDB:
    def __init__(self, db_path: str)
    def insert_record(self, record: FeatureUsageRecord)
    def get_records(self, ...) -> List[FeatureUsageRecord]
    def get_usage_stats(self, ...) -> Dict[str, Any]
```

### Enums

#### FeatureCategory
Categorizes features for better organization:
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

#### FeatureStatus
Tracks execution status:
- `SUCCESS`: Successful completion
- `FAILED`: Execution failure
- `PARTIAL`: Partial completion
- `TIMEOUT`: Operation timed out

## Decorator-Based Integration

### Basic Usage
```python
from feature_tracking.feature_tracker import track_feature, FeatureCategory

@track_feature("my_feature", FeatureCategory.AI_PROVIDER)
def my_function(param1, param2):
    return "result"
```

### Advanced Usage with Parameters
```python
@track_feature(
    feature_name="complex_operation", 
    category=FeatureCategory.AGENT_PLATFORM,
    user_id="user123"
)
def complex_function(data):
    return process(data)
```

## Manual Tracking for Complex Operations

For operations that require more control:

```python
from feature_tracking.feature_tracker import feature_tracker, FeatureStatus

def complex_operation():
    record_id = feature_tracker.start_custom_tracking(
        feature_name="my_complex_operation",
        category=FeatureCategory.SYSMON,
        user_id="user123",
        metadata={"operation_type": "data_processing", "data_size": "large"}
    )
    
    try:
        # Perform the operation
        result = perform_operation()
        
        feature_tracker.complete_custom_tracking(
            record_id=record_id,
            status=FeatureStatus.SUCCESS,
            input_size=len(str(input_data)),
            output_size=len(str(result)),
            efficiency_score=0.95,
            iterations=1
        )
        
        return result
    except Exception as e:
        feature_tracker.complete_custom_tracking(
            record_id=record_id,
            status=FeatureStatus.FAILED,
            error_message=str(e),
            efficiency_score=0.0
        )
        raise
```

## Efficiency Calculation

The system calculates efficiency using a weighted formula:
```
efficiency = (duration_factor * 0.5) + (output_factor * 0.3) + (iteration_factor * 0.2)
```

Where:
- `duration_factor`: Inversely proportional to execution time (faster = higher efficiency)
- `output_factor`: Proportional to output size (larger meaningful output = higher efficiency)  
- `iteration_factor`: Inversely proportional to iteration count (fewer iterations = higher efficiency)

## Configuration Options

The system is configurable via environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `FEATURE_TRACKING_DB_PATH` | Path to tracking database | `~/.cloudcurio/feature_tracking.db` |
| `FEATURE_TRACKING_ENABLED` | Enable/disable tracking | `true` |
| `FEATURE_TRACKING_FAILURES_ONLY` | Track only failures | `false` |
| `FEATURE_TRACKING_MIN_DURATION` | Minimum duration to track (seconds) | `0.0` |
| `FEATURE_TRACKING_MAX_METADATA_SIZE` | Max metadata size in bytes | `10240` |
| `FEATURE_TRACKING_ANONYMIZE` | Anonymize user data | `true` |
| `FEATURE_TRACKING_EXCLUDE` | Comma-separated features to exclude | `` (empty) |
| `FEATURE_TRACKING_FLUSH_INTERVAL` | Batch records and flush every N records | `100` |
| `FEATURE_TRACKING_MAX_BATCH_SIZE` | Max records per batch | `50` |

## API Endpoints

### Dashboard Endpoints
- `GET /` - Main dashboard page
- `GET /api/stats` - Overall statistics
- `GET /api/chart-data` - Chart data for visualization
- `GET /api/recent-calls` - Recent feature calls
- `GET /api/feature/{feature_name}` - Specific feature details

### CLI Commands
- `list-features` - Top features by usage
- `feature-stats <feature_name>` - Statistics for a feature
- `list-records` - Recent feature calls with filters

## Integration Examples

### AI Tools Integration
```python
# In ai_provider.py
@track_feature('ai_generation', FeatureCategory.AI_PROVIDER)
def generate_with_provider(self, prompt: str, provider_name: Optional[str] = None, **kwargs) -> str:
    # Original function logic
    return result
```

### MCP Server Integration
```python
# In server.py
@track_feature('crew_execution', FeatureCategory.MCP_SERVER)
def run_crew_endpoint(crew_id: str):
    # Original function logic
    return result
```

### SysMon Integration
```python
# In sysmon.py
@track_feature('create_config_snapshot', FeatureCategory.SYSMON)
def create_configuration_snapshot(self, name: str = None) -> str:
    # Original function logic
    return result
```

## Database Schema

The tracking system uses SQLite with the following schema:

```sql
CREATE TABLE feature_usage (
    id TEXT PRIMARY KEY,
    feature_name TEXT NOT NULL,
    category TEXT NOT NULL,
    status TEXT NOT NULL,
    duration REAL NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    input_size INTEGER DEFAULT 0,
    output_size INTEGER DEFAULT 0,
    metadata TEXT,  -- JSON string
    user_id TEXT,
    session_id TEXT NOT NULL,
    error_message TEXT,
    efficiency_score REAL,
    iterations INTEGER DEFAULT 1
);

-- Indexes for performance
CREATE INDEX idx_feature_name ON feature_usage(feature_name);
CREATE INDEX idx_category ON feature_usage(category);
CREATE INDEX idx_start_time ON feature_usage(start_time);
CREATE INDEX idx_user_id ON feature_usage(user_id);
```

## Performance Considerations

### Threading Safety
- All database operations use thread-local locks
- Concurrent access is properly synchronized
- No race conditions in record creation

### Batch Operations
- Records can be batched for performance
- Configurable batch sizes via environment variables
- Periodic flushing to database

### Memory Usage
- Minimal memory overhead per tracked operation
- Metadata size can be limited to prevent memory bloat
- Efficient data structures for record storage

## Privacy and Security

### User Data Protection
- Optional anonymization of user IDs
- Exclusion list for sensitive features
- Local storage by default (no external transmission)

### Data Retention
- Records stored locally in user's home directory
- No automatic data sharing or transmission
- Users control their tracking data completely

## Error Handling

### Failed Operations
- Errors during tracked operations are captured and stored
- Tracking operations themselves don't interfere with main functions
- Failed tracking doesn't break the main application

### Database Errors
- Graceful fallback if database is unavailable
- Operations continue even if tracking fails
- Error logging for debugging tracking issues

## Testing

### Unit Tests
```python
def test_feature_tracking():
    @track_feature("test_feature", FeatureCategory.OTHER)
    def test_func():
        return "result"
    
    result = test_func()
    assert result == "result"
    
    # Verify record was created
    records = feature_tracker.get_all_records(feature_name="test_feature")
    assert len(records) == 1
    assert records[0].status == FeatureStatus.SUCCESS
```

### Integration Tests
- Test decorator integration with various function types
- Verify database operations work correctly
- Test error handling scenarios
- Validate efficiency calculations

## Maintenance

### Database Cleanup
- Manual cleanup procedures available
- Automatic archiving possible in future versions
- Backup and restore capabilities

### Migration
- Version-aware schema migrations
- Backward compatibility maintained
- Upgrade procedures documented

## Future Enhancements

### Planned Features
- Real-time alerts for performance degradation
- Advanced analytics and machine learning insights
- Distributed tracking across multiple instances
- Export capabilities for external analysis
- Custom dashboard widgets
- Alerting and notification system

### Scalability
- Support for PostgreSQL for enterprise deployments
- Distributed tracking architecture
- Sharding for high-volume usage

## Troubleshooting

### Common Issues
1. **Database Locking**: Ensure only one process accesses the database
2. **Performance Impact**: Adjust batch sizes and flush intervals
3. **Memory Usage**: Limit metadata size and batch operations
4. **Integration Problems**: Check decorator placement and parameters

### Debugging
- Enable detailed logging for tracking operations  
- Use CLI to query and verify tracking data
- Check dashboard for real-time monitoring
- Review configuration settings

## Best Practices

1. **Use Appropriate Categories**: Categorize features correctly for better analysis
2. **Limit Metadata**: Keep metadata size reasonable
3. **Handle Errors Gracefully**: Don't let tracking errors break main functionality
4. **Configure Sensibly**: Adjust settings based on usage patterns
5. **Regular Monitoring**: Use dashboard to monitor feature performance
6. **Privacy First**: Always consider user privacy in tracking