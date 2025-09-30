#!/usr/bin/env python3
"""
CloudCurio Feature Tracking Demo

This script demonstrates the feature tracking system in action.
"""

import time
import random
from feature_tracking.feature_tracker import track_feature, FeatureCategory, FeatureStatus, feature_tracker
from ai_tools.ai_provider import ai_manager
from crew.mcp_server.server import app
from sysmon.sysmon import SysMon


@track_feature("demo_ai_query", FeatureCategory.AI_PROVIDER)
def demo_ai_query(prompt: str):
    """Demo function that queries an AI provider"""
    # Simulate AI query
    time.sleep(random.uniform(0.1, 0.5))
    return f"Response to: {prompt}"


@track_feature("demo_package_install", FeatureCategory.SYSMON)
def demo_package_install(package_name: str):
    """Demo function that simulates package installation"""
    # Simulate package installation
    time.sleep(random.uniform(0.2, 1.0))
    success = random.choice([True, True, True, False])  # 75% success rate
    if success:
        return f"Successfully installed {package_name}"
    else:
        raise Exception(f"Failed to install {package_name}")


@track_feature("demo_service_config", FeatureCategory.CONFIG_EDITOR)
def demo_service_config(service_name: str, config: dict):
    """Demo function that simulates service configuration"""
    # Simulate service configuration
    time.sleep(random.uniform(0.1, 0.3))
    return f"Configured {service_name} with {len(config)} settings"


@track_feature("demo_crew_execution", FeatureCategory.MCP_SERVER)
def demo_crew_execution(crew_type: str):
    """Demo function that simulates crew execution"""
    # Simulate crew execution
    time.sleep(random.uniform(0.5, 2.0))
    return f"Executed {crew_type} crew successfully"


def run_demo():
    """Run the feature tracking demo"""
    print("CloudCurio Feature Tracking Demo")
    print("=" * 40)
    
    # Run some demo functions
    print("Running demo functions...")
    
    try:
        result1 = demo_ai_query("What is the capital of France?")
        print(f"AI Query Result: {result1}")
    except Exception as e:
        print(f"AI Query Error: {e}")
    
    try:
        result2 = demo_package_install("numpy")
        print(f"Package Install Result: {result2}")
    except Exception as e:
        print(f"Package Install Error: {e}")
    
    try:
        result3 = demo_service_config("nginx", {"port": 80, "workers": 4})
        print(f"Service Config Result: {result3}")
    except Exception as e:
        print(f"Service Config Error: {e}")
    
    try:
        result4 = demo_crew_execution("code_review")
        print(f"Crew Execution Result: {result4}")
    except Exception as e:
        print(f"Crew Execution Error: {e}")
    
    # Show tracking dashboard
    print("\nFeature Tracking Dashboard:")
    print("-" * 30)
    
    # Get top features
    top_features = feature_tracker.get_top_features(10)
    for feature in top_features:
        print(f"{feature['feature_name']:20} | {feature['usage_count']:3} calls | "
              f"{feature['avg_duration']:.3f}s avg | {feature['success_rate']:.1f}% success")
    
    # Get recent records
    print("\nRecent Feature Calls:")
    print("-" * 50)
    recent_records = feature_tracker.get_all_records(limit=5)
    for record in recent_records:
        status_icon = "✅" if record.status == FeatureStatus.SUCCESS else "❌"
        print(f"{status_icon} {record.feature_name:20} | {record.duration:.3f}s | "
              f"{record.timestamp.strftime('%H:%M:%S')}")


if __name__ == "__main__":
    run_demo()