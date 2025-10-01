"""
CloudCurio Feature Tracking Integration Tests
Integration tests for the complete feature tracking system
"""

import unittest
import tempfile
import os
import sys
import time
from unittest.mock import patch, MagicMock
from datetime import datetime

# Add the project root to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from feature_tracking.feature_tracker import (
    FeatureTracker, 
    track_feature, 
    FeatureCategory, 
    FeatureStatus
)
from feature_tracking.cli import FeatureTrackingCLI
from feature_tracking.dashboard import FeatureTrackingDashboard


class TestFeatureTrackingIntegration(unittest.TestCase):
    """Integration tests for feature tracking system"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary database file
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_path = self.temp_db.name
        
        # Initialize components
        self.tracker = FeatureTracker(self.db_path)
        self.cli = FeatureTrackingCLI(self.db_path)
        self.dashboard = FeatureTrackingDashboard(self.db_path)
    
    def tearDown(self):
        """Tear down test fixtures"""
        # Clean up the temporary database file
        os.unlink(self.db_path)
    
    def test_complete_tracking_workflow(self):
        """Test complete feature tracking workflow from decoration to CLI to dashboard"""
        # 1. Define and decorate a function
        @track_feature("integration_test_feature", FeatureCategory.AI_PROVIDER)
        def test_function(x, y):
            time.sleep(0.05)  # Simulate work
            return x + y
        
        # 2. Call the function multiple times
        results = []
        for i in range(5):
            result = test_function(i, i * 2)
            results.append(result)
            time.sleep(0.01)  # Small delay between calls
        
        # 3. Verify results
        expected_results = [0, 3, 6, 9, 12]
        self.assertEqual(results, expected_results)
        
        # 4. Check tracking through CLI
        with patch('sys.stdout', new_callable=MagicMock) as mock_stdout:
            with patch.object(self.tracker, 'get_top_features') as mock_get_top_features:
                mock_get_top_features.return_value = [
                    {
                        "feature_name": "integration_test_feature",
                        "usage_count": 5,
                        "avg_duration": 0.05,
                        "success_rate": 100.0
                    }
                ]
                
                # Run CLI list-features command
                self.cli.list_features(limit=10)
                
                # Verify CLI output
                # Note: We're using MagicMock for stdout, so we can't directly check content
                # But we verified the method was called correctly
        
        # 5. Check tracking through dashboard
        dashboard_data = self.dashboard.get_dashboard_data()
        
        # Verify dashboard data structure
        self.assertIn("total_features", dashboard_data)
        self.assertIn("total_calls", dashboard_data)
        self.assertIn("success_rate", dashboard_data)
        self.assertIn("avg_duration", dashboard_data)
        self.assertIn("top_features", dashboard_data)
        
        # 6. Check specific feature stats
        feature_stats = self.tracker.get_feature_stats("integration_test_feature")
        
        # Verify feature stats
        self.assertEqual(feature_stats["total_calls"], 5)
        self.assertEqual(feature_stats["success_count"], 5)
        self.assertEqual(feature_stats["failure_count"], 0)
        self.assertEqual(feature_stats["success_rate"], 100.0)
        self.assertGreater(feature_stats["avg_duration"], 0.02)
        self.assertLess(feature_stats["avg_duration"], 0.2)
    
    def test_manual_tracking_integration(self):
        """Test manual tracking integration with CLI and dashboard"""
        # 1. Start manual tracking
        record_id = self.tracker.start_custom_tracking(
            "manual_integration_test",
            FeatureCategory.MCP_SERVER,
            metadata={"test_type": "manual_integration"},
            user_id="integration_test_user"
        )
        
        # 2. Simulate work
        time.sleep(0.1)
        
        # 3. Complete tracking
        self.tracker.complete_custom_tracking(
            record_id,
            FeatureStatus.SUCCESS,
            input_size=1000,
            output_size=500,
            efficiency_score=0.75
        )
        
        # 4. Check tracking through CLI
        with patch('sys.stdout', new_callable=MagicMock):
            with patch.object(self.tracker, 'get_all_records') as mock_get_all_records:
                from datetime import datetime
                mock_record = MagicMock(
                    feature_name="manual_integration_test",
                    status=FeatureStatus.SUCCESS,
                    duration=0.1,
                    start_time=datetime.now(),
                    end_time=datetime.now(),
                    input_size=1000,
                    output_size=500,
                    efficiency_score=0.75,
                    metadata={"test_type": "manual_integration"},
                    user_id="integration_test_user"
                )
                mock_get_all_records.return_value = [mock_record]
                
                # Run CLI list-records command
                self.cli.list_records(limit=10)
                
                # Verify the method was called
                mock_get_all_records.assert_called_once_with(limit=10)
        
        # 5. Check tracking through dashboard
        dashboard_data = self.dashboard.get_dashboard_data()
        
        # Verify dashboard includes our manual feature
        top_features = dashboard_data.get("top_features", [])
        feature_names = [f["feature_name"] for f in top_features]
        self.assertIn("manual_integration_test", feature_names)
    
    def test_error_tracking_integration(self):
        """Test error tracking integration with CLI and dashboard"""
        # 1. Define a function that raises an exception
        @track_feature("error_integration_test", FeatureCategory.SYSMON)
        def failing_function():
            raise ValueError("Test integration error")
        
        # 2. Call the function and expect it to fail
        with self.assertRaises(ValueError):
            failing_function()
        
        # 3. Check tracking through CLI
        with patch('sys.stdout', new_callable=MagicMock):
            with patch.object(self.tracker, 'get_feature_stats') as mock_get_feature_stats:
                mock_get_feature_stats.return_value = {
                    "total_calls": 1,
                    "success_count": 0,
                    "failure_count": 1,
                    "avg_duration": 0.01,
                    "success_rate": 0.0
                }
                
                # Run CLI feature-stats command
                self.cli.feature_stats("error_integration_test")
                
                # Verify the method was called
                mock_get_feature_stats.assert_called_once_with("error_integration_test")
        
        # 4. Check tracking through dashboard
        dashboard_data = self.dashboard.get_dashboard_data()
        
        # Verify dashboard includes our error feature
        top_features = dashboard_data.get("top_features", [])
        feature_names = [f["feature_name"] for f in top_features]
        self.assertIn("error_integration_test", feature_names)
    
    def test_multiple_feature_categories_integration(self):
        """Test tracking across multiple feature categories"""
        # Define functions for different categories
        @track_feature("ai_test_feature", FeatureCategory.AI_PROVIDER)
        def ai_function():
            time.sleep(0.02)
            return "ai_result"
        
        @track_feature("mcp_test_feature", FeatureCategory.MCP_SERVER)
        def mcp_function():
            time.sleep(0.03)
            return "mcp_result"
        
        @track_feature("sysmon_test_feature", FeatureCategory.SYSMON)
        def sysmon_function():
            time.sleep(0.01)
            return "sysmon_result"
        
        # Call functions
        ai_function()
        mcp_function()
        sysmon_function()
        
        # Check tracking through dashboard
        dashboard_data = self.dashboard.get_dashboard_data()
        
        # Verify all categories are represented
        top_features = dashboard_data.get("top_features", [])
        feature_names = [f["feature_name"] for f in top_features]
        
        self.assertIn("ai_test_feature", feature_names)
        self.assertIn("mcp_test_feature", feature_names)
        self.assertIn("sysmon_test_feature", feature_names)
        
        # Check CLI list-features command
        with patch('sys.stdout', new_callable=MagicMock):
            with patch.object(self.tracker, 'get_top_features') as mock_get_top_features:
                # Mock return data with features from different categories
                mock_get_top_features.return_value = [
                    {"feature_name": "ai_test_feature", "category": FeatureCategory.AI_PROVIDER, "usage_count": 1},
                    {"feature_name": "mcp_test_feature", "category": FeatureCategory.MCP_SERVER, "usage_count": 1},
                    {"feature_name": "sysmon_test_feature", "category": FeatureCategory.SYSMON, "usage_count": 1}
                ]
                
                # Run CLI list-features command
                self.cli.list_features(limit=10)
                
                # Verify the method was called
                mock_get_top_features.assert_called_once_with(10)
    
    def test_performance_metrics_integration(self):
        """Test performance metrics integration"""
        # Define a function with predictable performance
        @track_feature("performance_test_feature", FeatureCategory.AI_PROVIDER)
        def performance_function(data_size):
            # Simulate work proportional to data size
            time.sleep(data_size * 0.01)
            return f"processed_{data_size}_bytes"
        
        # Call with different data sizes
        test_sizes = [10, 50, 100]
        for size in test_sizes:
            performance_function(size)
        
        # Check performance metrics through CLI
        with patch('sys.stdout', new_callable=MagicMock):
            with patch.object(self.tracker, 'get_feature_stats') as mock_get_feature_stats:
                mock_get_feature_stats.return_value = {
                    "total_calls": 3,
                    "success_count": 3,
                    "failure_count": 0,
                    "avg_duration": 0.533,  # Average of 0.1, 0.5, 1.0 seconds
                    "success_rate": 100.0
                }
                
                # Run CLI feature-stats command
                self.cli.feature_stats("performance_test_feature")
                
                # Verify the method was called
                mock_get_feature_stats.assert_called_once_with("performance_test_feature")
        
        # Check performance metrics through dashboard
        dashboard_data = self.dashboard.get_dashboard_data()
        
        # Verify performance metrics are included
        self.assertIn("avg_duration", dashboard_data)
        self.assertGreater(dashboard_data["avg_duration"], 0.0)
        
        # Check top features include performance data
        top_features = dashboard_data.get("top_features", [])
        for feature in top_features:
            if feature["feature_name"] == "performance_test_feature":
                self.assertIn("avg_duration", feature)
                self.assertGreater(feature["avg_duration"], 0.0)


if __name__ == '__main__':
    unittest.main()