#!/usr/bin/env python3
"""
CloudCurio Feature Tracking Integration Setup

This script helps integrate feature tracking into the CloudCurio platform.
"""

import os
import sys
from pathlib import Path


def integrate_with_ai_tools():
    """Integrate feature tracking with AI tools"""
    ai_tools_path = Path("ai_tools")
    if ai_tools_path.exists():
        # Update ai_provider.py to include feature tracking
        ai_provider_path = ai_tools_path / "ai_provider.py"
        if ai_provider_path.exists():
            with open(ai_provider_path, "r") as f:
                content = f.read()
            
            # Add import
            if "feature_tracking" not in content:
                content = content.replace(
                    "from typing import Optional, Dict, Any, List",
                    "from typing import Optional, Dict, Any, List\nfrom feature_tracking.feature_tracker import track_feature, FeatureCategory"
                )
                
                # Add tracking to generate methods
                content = content.replace(
                    "def generate_with_provider(self, prompt: str, provider_name: Optional[str] = None, **kwargs) -> str:",
                    "@track_feature('ai_generation', FeatureCategory.AI_PROVIDER)\ndef generate_with_provider(self, prompt: str, provider_name: Optional[str] = None, **kwargs) -> str:"
                )
            
            with open(ai_provider_path, "w") as f:
                f.write(content)
            print("✓ Integrated feature tracking with AI tools")


def integrate_with_mcp_server():
    """Integrate feature tracking with MCP server"""
    mcp_path = Path("crew") / "mcp_server"
    if mcp_path.exists():
        server_path = mcp_path / "server.py"
        if server_path.exists():
            with open(server_path, "r") as f:
                content = f.read()
            
            # Add import for feature tracking
            if "feature_tracking" not in content:
                content = content.replace(
                    "from crewai import Crew, Process",
                    "from crewai import Crew, Process\nfrom feature_tracking.feature_tracker import track_feature, FeatureCategory"
                )
                
                # Add tracking to crew execution
                content = content.replace(
                    "result = code_review_crew.kickoff()",
                    "# Track the crew execution\nresult = track_feature('code_review_crew_execution', FeatureCategory.MCP_SERVER)(lambda: code_review_crew.kickoff)()"
                )
            
            with open(server_path, "w") as f:
                f.write(content)
            print("✓ Integrated feature tracking with MCP server")


def integrate_with_sysmon():
    """Integrate feature tracking with SysMon"""
    sysmon_path = Path("sysmon")
    if sysmon_path.exists():
        sysmon_py = sysmon_path / "sysmon.py"
        if sysmon_py.exists():
            with open(sysmon_py, "r") as f:
                content = f.read()
            
            # Add import for feature tracking
            if "feature_tracking" not in content:
                content = content.replace(
                    "from datetime import datetime",
                    "from datetime import datetime\nfrom feature_tracking.feature_tracker import track_feature, FeatureCategory"
                )
                
                # Add tracking to create_snapshot method
                if "create_configuration_snapshot" in content and "@track_feature" not in content:
                    content = content.replace(
                        "def create_configuration_snapshot(self, name: str = None) -> str:",
                        "@track_feature('create_config_snapshot', FeatureCategory.SYSMON)\ndef create_configuration_snapshot(self, name: str = None) -> str:"
                    )
                
                # Add tracking to check_for_changes method
                if "check_for_changes" in content and "@track_feature" not in content:
                    content = content.replace(
                        "def check_for_changes(self):",
                        "@track_feature('check_system_changes', FeatureCategory.SYSMON)\ndef check_for_changes(self):"
                    )
            
            with open(sysmon_py, "w") as f:
                f.write(content)
            print("✓ Integrated feature tracking with SysMon")


def create_integration_example():
    """Create a comprehensive integration example"""
    integration_example = '''
"""
CloudCurio Feature Tracking Integration Example
"""

# Example of how to integrate feature tracking in different modules

from feature_tracking.feature_tracker import track_feature, FeatureCategory, feature_tracker

# Example 1: Track AI provider usage
@track_feature("openrouter_query", FeatureCategory.AI_PROVIDER)
def example_ai_query(prompt: str):
    """Example function that queries an AI provider"""
    # Simulate AI query
    import time
    time.sleep(0.1)  # Simulate API call
    return f"Response to: {prompt}"

# Example 2: Track configuration operations
@track_feature("update_config", FeatureCategory.CONFIG_EDITOR)
def example_config_update(config_data: dict):
    """Example function that updates configuration"""
    # Simulate config update
    import time
    time.sleep(0.05)  # Simulate processing
    return {"status": "success", "updated_keys": list(config_data.keys())}

# Example 3: Track system monitoring
@track_feature("scan_packages", FeatureCategory.SYSMON)
def example_package_scan():
    """Example function that scans system packages"""
    # Simulate package scan
    import time
    time.sleep(0.2)  # Simulate scanning
    return {"packages_found": 42, "scan_time": 0.2}

# Example 4: Complex operation with manual tracking
def example_complex_operation():
    """Example of a complex operation with manual tracking"""
    record_id = feature_tracker.start_custom_tracking(
        "complex_operation",
        FeatureCategory.AGENT_PLATFORM,
        metadata={"operation_type": "data_analysis", "data_size": "large"}
    )
    
    try:
        # Simulate complex work
        import time
        time.sleep(0.5)
        
        # Determine success and calculate metrics
        success = True
        if success:
            feature_tracker.complete_custom_tracking(
                record_id,
                status="success",
                input_size=10000,
                output_size=500,
                efficiency_score=0.85
            )
            return "Success"
        else:
            feature_tracker.complete_custom_tracking(
                record_id,
                status="failed",
                error_message="Operation failed",
                efficiency_score=0.0
            )
            return "Failed"
    except Exception as e:
        feature_tracker.complete_custom_tracking(
            record_id,
            status="failed", 
            error_message=str(e),
            efficiency_score=0.0
        )
        raise

if __name__ == "__main__":
    print("Running feature tracking integration examples...")
    
    # Run examples
    result1 = example_ai_query("Hello, world!")
    print(f"AI Query result: {result1[:30]}...")
    
    result2 = example_config_update({"setting1": "value1", "setting2": "value2"})
    print(f"Config Update result: {result2}")
    
    result3 = example_package_scan()
    print(f"Package Scan result: {result3}")
    
    result4 = example_complex_operation()
    print(f"Complex Operation result: {result4}")
    
    print("Feature tracking examples completed!")
'''
    
    with open("feature_tracking/integration_example.py", "w") as f:
        f.write(integration_example)
    print("✓ Created integration example")


def main():
    """Main integration setup function"""
    print("CloudCurio Feature Tracking Integration Setup")
    print("=" * 50)
    
    print("Integrating feature tracking with CloudCurio components...")
    
    integrate_with_ai_tools()
    integrate_with_mcp_server()
    integrate_with_sysmon()
    create_integration_example()
    
    print("\n✓ Feature tracking integration setup complete!")
    print("\nTo use feature tracking in your code:")
    print("1. Import: from feature_tracking.feature_tracker import track_feature, FeatureCategory")
    print("2. Decorate functions: @track_feature('feature_name', FeatureCategory.CATEGORY)")
    print("3. Access dashboard: python -m feature_tracking.dashboard")
    print("4. View CLI: python -m feature_tracking.cli --help")


if __name__ == "__main__":
    main()