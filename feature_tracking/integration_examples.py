"""
CloudCurio Feature Tracking Integration Examples

Examples of how to integrate the feature tracking system with different
CloudCurio components.
"""

from feature_tracking.feature_tracker import track_feature, FeatureCategory, feature_tracker
from ai_tools.ai_provider import ai_manager
from crew.mcp_server.server import app  # Assuming FastAPI app
from sysmon.sysmon import SysMon


# Example 1: Track AI provider usage
@track_feature("openrouter_query", FeatureCategory.AI_PROVIDER)
def query_openrouter(prompt: str, model: str = "mistralai/mistral-7b-instruct"):
    """Query OpenRouter with feature tracking"""
    return ai_manager.generate_with_provider(prompt, provider_name="openrouter", model=model)


# Example 2: Track system monitoring operations
class TrackedSysMon(SysMon):
    """SysMon with feature tracking integration"""
    
    @track_feature("create_snapshot", FeatureCategory.SYSMON)
    def create_tracked_snapshot(self, name: str = None):
        """Create a configuration snapshot with tracking"""
        return self.create_configuration_snapshot(name)
    
    @track_feature("check_for_changes", FeatureCategory.SYSMON)
    def tracked_check_for_changes(self):
        """Check for system changes with tracking"""
        return self.command_tracker.check_for_changes()


# Example 3: Track MCP server endpoints
def setup_tracked_mcp_endpoints():
    """Setup MCP server endpoints with feature tracking"""
    
    # We'll use middleware approach for API endpoints
    @app.middleware("http")
    async def track_api_requests(request, call_next):
        start_time = time.time()
        
        # Identify the endpoint
        path = request.url.path
        method = request.method
        
        # Determine category based on endpoint
        if "/crews/" in path:
            category = FeatureCategory.MCP_SERVER
            feature_name = f"api_crew_{method.lower()}"
        elif "/health" in path:
            category = FeatureCategory.MCP_SERVER
            feature_name = "api_health_check"
        else:
            category = FeatureCategory.MCP_SERVER
            feature_name = f"api_{path.replace('/', '_').replace('-', '_')}"
        
        record_id = feature_tracker.start_custom_tracking(
            feature_name,
            category,
            metadata={
                "path": path,
                "method": method,
                "client_ip": request.client.host if request.client else None
            }
        )
        
        try:
            response = await call_next(request)
            
            # Calculate efficiency based on response time
            duration = time.time() - start_time
            
            feature_tracker.complete_custom_tracking(
                record_id,
                status=response.status_code < 400 and FeatureStatus.SUCCESS or FeatureStatus.FAILED,
                input_size=int(request.headers.get("content-length", 0)),
                output_size=int(response.headers.get("content-length", 0)),
                efficiency_score=1.0 / (1.0 + duration)  # Higher efficiency for faster responses
            )
            
            return response
        except Exception as e:
            duration = time.time() - start_time
            feature_tracker.complete_custom_tracking(
                record_id,
                FeatureStatus.FAILED,
                error_message=str(e),
                efficiency_score=0.0
            )
            raise


# Example 4: Track agentic platform operations
@track_feature("create_agent", FeatureCategory.AGENT_PLATFORM)
def create_tracked_agent(name: str, role: str, goal: str, backstory: str):
    """Create an agent with feature tracking"""
    platform = feature_tracker.get_agentic_platform()  # Assuming this method exists
    return platform.create_custom_agent(name, role, goal, backstory)


@track_feature("run_crew", FeatureCategory.AGENT_PLATFORM)
def run_tracked_crew(crew_id: str):
    """Run a crew with feature tracking"""
    platform = feature_tracker.get_agentic_platform()  # Assuming this method exists
    return platform.run_crew(crew_id)


# Example 5: Track configuration editor operations
@track_feature("record_action", FeatureCategory.CONFIG_EDITOR)
def record_tracked_action(action_type: str, description: str, session_id: str):
    """Record an action in the configuration editor with tracking"""
    from config_editor.config_editor import RecordedAction
    import json
    
    # Simulate creating and recording an action
    action = RecordedAction(
        id=None,
        action_type=action_type,
        timestamp=None,
        description=description,
        url=None,
        selector=None,
        data={},
        session_id=session_id,
        step_group=None,
        confidence=0.0
    )
    
    # This is just an example - actual implementation would depend on your system
    return action


# Example 6: Batch processing with tracking
def batch_process_with_tracking(items: list, processor_func):
    """Process a batch of items with tracking for each operation"""
    results = []
    
    for i, item in enumerate(items):
        # Create a unique feature name for this specific operation
        feature_name = f"batch_process_item_{i % 10}"  # Group by last digit to avoid too many unique names
        record_id = feature_tracker.start_custom_tracking(
            feature_name,
            FeatureCategory.OTHER,
            metadata={
                "item_index": i,
                "item_type": type(item).__name__,
                "batch_size": len(items)
            }
        )
        
        try:
            # Process the item
            result = processor_func(item)
            
            # Calculate input/output sizes (example)
            input_size = len(str(item))
            output_size = len(str(result))
            
            feature_tracker.complete_custom_tracking(
                record_id,
                FeatureStatus.SUCCESS,
                input_size=input_size,
                output_size=output_size
            )
            
            results.append(result)
            
        except Exception as e:
            feature_tracker.complete_custom_tracking(
                record_id,
                FeatureStatus.FAILED,
                error_message=str(e)
            )
            # Depending on your requirements, you might want to continue or stop
            results.append(None)  # or raise the exception
    
    return results


# Example 7: Context manager for complex operations
from contextlib import contextmanager

@contextmanager
def tracked_operation(feature_name: str, category: FeatureCategory, **metadata):
    """Context manager for tracking complex operations"""
    record_id = feature_tracker.start_custom_tracking(
        feature_name,
        category,
        metadata=metadata
    )
    
    start_time = time.time()
    try:
        yield
        duration = time.time() - start_time
        
        feature_tracker.complete_custom_tracking(
            record_id,
            FeatureStatus.SUCCESS,
            efficiency_score=1.0 / (1.0 + duration)  # Simple efficiency calculation
        )
    except Exception as e:
        duration = time.time() - start_time
        feature_tracker.complete_custom_tracking(
            record_id,
            FeatureStatus.FAILED,
            error_message=str(e),
            efficiency_score=0.0
        )
        raise


# Example usage of the context manager
def example_context_usage():
    """Example of using the tracked operation context manager"""
    
    # Example: Tracking a complex configuration update
    with tracked_operation(
        "complex_config_update",
        FeatureCategory.CONFIG_EDITOR,
        config_type="system_config",
        update_reason="security_patch"
    ):
        # Simulate complex operation
        time.sleep(1)  # Simulate work
        # Perform actual configuration update
        print("Performing complex configuration update...")


if __name__ == "__main__":
    print("CloudCurio Feature Tracking Integration Examples")
    print("=" * 50)
    
    # Run examples
    print("\n1. Example: Query OpenRouter with tracking")
    try:
        result = query_openrouter("What is the capital of France?")
        print(f"Result: {result[:50]}...")
    except Exception as e:
        print(f"Error (expected if no API key): {e}")
    
    print("\n2. Example: Context manager usage")
    example_context_usage()
    
    print("\n3. Example: Batch processing with tracking")
    items = ["item1", "item2", "item3"]
    results = batch_process_with_tracking(items, lambda x: f"processed_{x}")
    print(f"Processed {len([r for r in results if r is not None])} items successfully")
    
    print("\nFeature tracking is now integrated throughout the CloudCurio platform!")