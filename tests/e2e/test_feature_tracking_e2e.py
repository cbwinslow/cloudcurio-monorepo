"""
CloudCurio Feature Tracking End-to-End Tests
Complete end-to-end tests for the feature tracking system
"""

import unittest
import tempfile
import os
import sys
import time
import json
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


class TestFeatureTrackingEndToEnd(unittest.TestCase):
    """End-to-end tests for feature tracking system"""
    
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
    
    def test_complete_e2e_workflow(self):
        """Test complete end-to-end workflow"""
        print("🧪 Starting complete end-to-end test workflow...")
        
        # 1. Define and decorate multiple functions
        @track_feature("e2e_ai_query", FeatureCategory.AI_PROVIDER)
        def ai_query_function(prompt):
            time.sleep(0.05)  # Simulate AI query
            return f"AI response to: {prompt}"
        
        @track_feature("e2e_config_update", FeatureCategory.CONFIG_EDITOR)
        def config_update_function(service_name, config):
            time.sleep(0.02)  # Simulate config update
            return f"Updated {service_name} with {len(config)} settings"
        
        @track_feature("e2e_sysmon_check", FeatureCategory.SYSMON)
        def sysmon_check_function():
            time.sleep(0.03)  # Simulate system monitoring
            return "System status: OK"
        
        # 2. Execute functions multiple times
        print("🔄 Executing tracked functions...")
        
        # Execute AI queries
        ai_results = []
        for i in range(3):
            result = ai_query_function(f"Test prompt {i+1}")
            ai_results.append(result)
            time.sleep(0.01)
        
        # Execute config updates
        config_results = []
        for i in range(2):
            result = config_update_function(f"service_{i+1}", {"setting1": "value1", "setting2": "value2"})
            config_results.append(result)
            time.sleep(0.01)
        
        # Execute system monitoring
        sysmon_results = []
        for i in range(4):
            result = sysmon_check_function()
            sysmon_results.append(result)
            time.sleep(0.01)
        
        # 3. Manually track a complex operation
        print("📝 Tracking manual operation...")
        
        record_id = self.tracker.start_custom_tracking(
            "e2e_complex_operation",
            FeatureCategory.MCP_SERVER,
            metadata={
                "operation_type": "data_processing",
                "data_size": 10000,
                "algorithm": "advanced_sorting"
            },
            user_id="e2e_test_user"
        )
        
        # Simulate complex work
        time.sleep(0.1)
        
        self.tracker.complete_custom_tracking(
            record_id,
            FeatureStatus.SUCCESS,
            input_size=10000,
            output_size=5000,
            efficiency_score=0.85,
            iterations=3
        )
        
        # 4. Test error tracking
        print("💥 Testing error tracking...")
        
        @track_feature("e2e_error_test", FeatureCategory.SYSMON)
        def error_function():
            time.sleep(0.01)
            raise ValueError("Test error for E2E")
        
        # Expect this to fail
        with self.assertRaises(ValueError):
            error_function()
        
        # 5. Verify tracking through database
        print("🔍 Verifying database tracking...")
        
        all_records = self.tracker.get_all_records()
        self.assertEqual(len(all_records), 11)  # 3 AI + 2 Config + 4 SysMon + 1 Manual + 1 Error
        
        # Check specific feature records
        ai_records = self.tracker.get_all_records(feature_name="e2e_ai_query")
        self.assertEqual(len(ai_records), 3)
        for record in ai_records:
            self.assertEqual(record.feature_name, "e2e_ai_query")
            self.assertEqual(record.category, FeatureCategory.AI_PROVIDER)
            self.assertEqual(record.status, FeatureStatus.SUCCESS)
            self.assertGreater(record.duration, 0.02)
            self.assertLess(record.duration, 0.2)
        
        config_records = self.tracker.get_all_records(feature_name="e2e_config_update")
        self.assertEqual(len(config_records), 2)
        for record in config_records:
            self.assertEqual(record.feature_name, "e2e_config_update")
            self.assertEqual(record.category, FeatureCategory.CONFIG_EDITOR)
            self.assertEqual(record.status, FeatureStatus.SUCCESS)
            self.assertGreater(record.duration, 0.01)
            self.assertLess(record.duration, 0.1)
        
        sysmon_records = self.tracker.get_all_records(feature_name="e2e_sysmon_check")
        self.assertEqual(len(sysmon_records), 4)
        for record in sysmon_records:
            self.assertEqual(record.feature_name, "e2e_sysmon_check")
            self.assertEqual(record.category, FeatureCategory.SYSMON)
            self.assertEqual(record.status, FeatureStatus.SUCCESS)
            self.assertGreater(record.duration, 0.01)
            self.assertLess(record.duration, 0.1)
        
        manual_records = self.tracker.get_all_records(feature_name="e2e_complex_operation")
        self.assertEqual(len(manual_records), 1)
        manual_record = manual_records[0]
        self.assertEqual(manual_record.feature_name, "e2e_complex_operation")
        self.assertEqual(manual_record.category, FeatureCategory.MCP_SERVER)
        self.assertEqual(manual_record.status, FeatureStatus.SUCCESS)
        self.assertEqual(manual_record.input_size, 10000)
        self.assertEqual(manual_record.output_size, 5000)
        self.assertEqual(manual_record.efficiency_score, 0.85)
        self.assertEqual(manual_record.iterations, 3)
        self.assertEqual(manual_record.user_id, "e2e_test_user")
        self.assertIn("operation_type", manual_record.metadata)
        self.assertIn("data_size", manual_record.metadata)
        self.assertIn("algorithm", manual_record.metadata)
        
        error_records = self.tracker.get_all_records(feature_name="e2e_error_test")
        self.assertEqual(len(error_records), 1)
        error_record = error_records[0]
        self.assertEqual(error_record.feature_name, "e2e_error_test")
        self.assertEqual(error_record.category, FeatureCategory.SYSMON)
        self.assertEqual(error_record.status, FeatureStatus.FAILED)
        self.assertIn("Test error for E2E", error_record.error_message)
        self.assertEqual(error_record.efficiency_score, 0.0)
        
        # 6. Verify tracking statistics
        print("📊 Verifying tracking statistics...")
        
        ai_stats = self.tracker.get_feature_stats("e2e_ai_query")
        self.assertEqual(ai_stats["total_calls"], 3)
        self.assertEqual(ai_stats["success_count"], 3)
        self.assertEqual(ai_stats["failure_count"], 0)
        self.assertEqual(ai_stats["success_rate"], 100.0)
        self.assertGreater(ai_stats["avg_duration"], 0.02)
        self.assertLess(ai_stats["avg_duration"], 0.2)
        self.assertGreater(ai_stats["avg_efficiency"], 0.5)
        
        config_stats = self.tracker.get_feature_stats("e2e_config_update")
        self.assertEqual(config_stats["total_calls"], 2)
        self.assertEqual(config_stats["success_count"], 2)
        self.assertEqual(config_stats["failure_count"], 0)
        self.assertEqual(config_stats["success_rate"], 100.0)
        self.assertGreater(config_stats["avg_duration"], 0.01)
        self.assertLess(config_stats["avg_duration"], 0.1)
        self.assertGreater(config_stats["avg_efficiency"], 0.5)
        
        sysmon_stats = self.tracker.get_feature_stats("e2e_sysmon_check")
        self.assertEqual(sysmon_stats["total_calls"], 4)
        self.assertEqual(sysmon_stats["success_count"], 4)
        self.assertEqual(sysmon_stats["failure_count"], 0)
        self.assertEqual(sysmon_stats["success_rate"], 100.0)
        self.assertGreater(sysmon_stats["avg_duration"], 0.01)
        self.assertLess(sysmon_stats["avg_duration"], 0.1)
        self.assertGreater(sysmon_stats["avg_efficiency"], 0.5)
        
        error_stats = self.tracker.get_feature_stats("e2e_error_test")
        self.assertEqual(error_stats["total_calls"], 1)
        self.assertEqual(error_stats["success_count"], 0)
        self.assertEqual(error_stats["failure_count"], 1)
        self.assertEqual(error_stats["success_rate"], 0.0)
        self.assertEqual(error_stats["avg_efficiency"], 0.0)
        
        # 7. Verify top features
        print("🏆 Verifying top features...")
        
        top_features = self.tracker.get_top_features(10)
        self.assertGreaterEqual(len(top_features), 5)
        
        # Check that features are sorted by usage count
        usage_counts = [f["usage_count"] for f in top_features]
        self.assertEqual(usage_counts, sorted(usage_counts, reverse=True))
        
        # Find our features in the top list
        feature_dict = {f["feature_name"]: f for f in top_features}
        self.assertIn("e2e_sysmon_check", feature_dict)
        self.assertIn("e2e_ai_query", feature_dict)
        self.assertIn("e2e_config_update", feature_dict)
        self.assertIn("e2e_complex_operation", feature_dict)
        self.assertIn("e2e_error_test", feature_dict)
        
        self.assertEqual(feature_dict["e2e_sysmon_check"]["usage_count"], 4)
        self.assertEqual(feature_dict["e2e_ai_query"]["usage_count"], 3)
        self.assertEqual(feature_dict["e2e_config_update"]["usage_count"], 2)
        self.assertEqual(feature_dict["e2e_complex_operation"]["usage_count"], 1)
        self.assertEqual(feature_dict["e2e_error_test"]["usage_count"], 1)
        
        # 8. Verify CLI functionality
        print("🖥️ Verifying CLI functionality...")
        
        with patch('sys.stdout', new_callable=MagicMock) as mock_stdout:
            # Test list-features command
            with patch.object(self.tracker, 'get_top_features') as mock_get_top_features:
                mock_get_top_features.return_value = top_features
                self.cli.list_features(limit=10)
                mock_get_top_features.assert_called_once_with(10)
        
        with patch('sys.stdout', new_callable=MagicMock) as mock_stdout:
            # Test feature-stats command
            with patch.object(self.tracker, 'get_feature_stats') as mock_get_feature_stats:
                mock_get_feature_stats.return_value = ai_stats
                self.cli.feature_stats("e2e_ai_query")
                mock_get_feature_stats.assert_called_once_with("e2e_ai_query")
        
        with patch('sys.stdout', new_callable=MagicMock) as mock_stdout:
            # Test list-records command
            with patch.object(self.tracker, 'get_all_records') as mock_get_all_records:
                mock_get_all_records.return_value = all_records[:5]  # Limit to first 5
                self.cli.list_records(limit=5)
                mock_get_all_records.assert_called_once_with(limit=5)
        
        # 9. Verify dashboard functionality
        print("📈 Verifying dashboard functionality...")
        
        dashboard_data = self.dashboard.get_dashboard_data()
        
        # Check overall statistics
        self.assertIn("total_features", dashboard_data)
        self.assertIn("total_calls", dashboard_data)
        self.assertIn("success_rate", dashboard_data)
        self.assertIn("avg_duration", dashboard_data)
        self.assertIn("avg_efficiency", dashboard_data)
        self.assertIn("top_features", dashboard_data)
        self.assertIn("recent_records", dashboard_data)
        
        # Verify values are reasonable
        self.assertGreaterEqual(dashboard_data["total_features"], 5)
        self.assertEqual(dashboard_data["total_calls"], 11)
        self.assertGreater(dashboard_data["success_rate"], 50.0)  # 10/11 successful
        self.assertGreater(dashboard_data["avg_duration"], 0.01)
        self.assertGreater(dashboard_data["avg_efficiency"], 0.3)
        self.assertEqual(len(dashboard_data["top_features"]), min(10, dashboard_data["total_features"]))
        self.assertEqual(len(dashboard_data["recent_records"]), min(20, 11))
        
        # 10. Verify dashboard filtering
        print("🔎 Verifying dashboard filtering...")
        
        # Filter by category
        ai_dashboard_data = self.dashboard.get_dashboard_data(category=FeatureCategory.AI_PROVIDER)
        self.assertIn("total_features", ai_dashboard_data)
        self.assertIn("total_calls", ai_dashboard_data)
        self.assertIn("success_rate", ai_dashboard_data)
        
        # Filter by feature name
        specific_dashboard_data = self.dashboard.get_dashboard_data(feature_name="e2e_ai_query")
        self.assertIn("total_features", specific_dashboard_data)
        self.assertIn("total_calls", specific_dashboard_data)
        self.assertIn("success_rate", specific_dashboard_data)
        
        print("✅ End-to-end test workflow completed successfully!")
    
    def test_performance_under_load(self):
        """Test feature tracking performance under load"""
        print("🏃 Testing performance under load...")
        
        @track_feature("load_test_feature", FeatureCategory.AI_PROVIDER)
        def load_test_function(x):
            # Very fast function to test tracking overhead
            return x * 2
        
        # Execute many calls rapidly
        start_time = time.time()
        results = []
        
        for i in range(100):
            result = load_test_function(i)
            results.append(result)
        
        end_time = time.time()
        total_duration = end_time - start_time
        
        # Verify all calls completed successfully
        expected_results = [i * 2 for i in range(100)]
        self.assertEqual(results, expected_results)
        
        # Verify tracking
        records = self.tracker.get_all_records(feature_name="load_test_feature")
        self.assertEqual(len(records), 100)
        
        # Check that tracking overhead is reasonable (< 50% increase in execution time)
        avg_duration_per_call = total_duration / 100
        self.assertLess(avg_duration_per_call, 0.01)  # Should be very fast
        
        print(f"⏱️  Load test completed in {total_duration:.3f}s for 100 calls")
        print(f"⏱️  Average time per call: {avg_duration_per_call:.6f}s")
    
    def test_concurrent_access(self):
        """Test concurrent access to feature tracking system"""
        import threading
        import concurrent.futures
        
        print("🧵 Testing concurrent access...")
        
        @track_feature("concurrent_test_feature", FeatureCategory.AI_PROVIDER)
        def concurrent_function(thread_id, call_num):
            time.sleep(0.001)  # Very short delay
            return f"thread_{thread_id}_call_{call_num}"
        
        # Run concurrent threads
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for thread_id in range(5):
                for call_num in range(10):
                    future = executor.submit(concurrent_function, thread_id, call_num)
                    futures.append(future)
            
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
        
        # Verify all calls completed
        self.assertEqual(len(results), 50)
        
        # Verify tracking
        records = self.tracker.get_all_records(feature_name="concurrent_test_feature")
        self.assertEqual(len(records), 50)
        
        # Check for any tracking errors
        failed_records = [r for r in records if r.status == FeatureStatus.FAILED]
        self.assertEqual(len(failed_records), 0)
        
        print("✅ Concurrent access test completed successfully!")
        print(f"🧵 Processed {len(results)} concurrent calls")


if __name__ == '__main__':
    unittest.main(verbosity=2)