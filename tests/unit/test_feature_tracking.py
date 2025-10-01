"""
CloudCurio Feature Tracking System Tests
Comprehensive test suite for the feature tracking system
"""

import unittest
import tempfile
import os
import json
import time
from datetime import datetime
from unittest.mock import patch, MagicMock

# Add the project root to the path so we can import the feature tracking module
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from feature_tracking.feature_tracker import (
    FeatureTracker, 
    track_feature, 
    FeatureCategory, 
    FeatureStatus,
    FeatureTrackerDB,
    FeatureUsageRecord
)


class TestFeatureTrackerDB(unittest.TestCase):
    """Test the FeatureTrackerDB class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary database file
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_path = self.temp_db.name
        self.db = FeatureTrackerDB(self.db_path)
    
    def tearDown(self):
        """Tear down test fixtures"""
        # Clean up the temporary database file
        os.unlink(self.db_path)
    
    def test_init_db(self):
        """Test database initialization"""
        # The database should be initialized when FeatureTrackerDB is created
        self.assertTrue(os.path.exists(self.db_path))
        
        # Check that tables were created
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            self.assertIn('feature_usage', tables)
    
    def test_insert_and_retrieve_record(self):
        """Test inserting and retrieving a feature usage record"""
        # Create a test record
        record = FeatureUsageRecord(
            record_id="test-record-123",
            feature_name="test_feature",
            category=FeatureCategory.AI_PROVIDER,
            status=FeatureStatus.SUCCESS,
            duration=1.23,
            start_time=datetime.now(),
            end_time=datetime.now(),
            input_size=100,
            output_size=200,
            metadata={"test": "data"},
            user_id="test-user",
            session_id="test-session",
            error_message=None,
            efficiency_score=0.85,
            iterations=1
        )
        
        # Insert the record
        record_id = self.db.insert_record(record)
        self.assertEqual(record_id, "test-record-123")
        
        # Retrieve the record
        retrieved_records = self.db.get_records(feature_name="test_feature")
        self.assertEqual(len(retrieved_records), 1)
        
        retrieved_record = retrieved_records[0]
        self.assertEqual(retrieved_record.record_id, "test-record-123")
        self.assertEqual(retrieved_record.feature_name, "test_feature")
        self.assertEqual(retrieved_record.category, FeatureCategory.AI_PROVIDER)
        self.assertEqual(retrieved_record.status, FeatureStatus.SUCCESS)
        self.assertEqual(retrieved_record.duration, 1.23)
        self.assertEqual(retrieved_record.input_size, 100)
        self.assertEqual(retrieved_record.output_size, 200)
        self.assertEqual(retrieved_record.metadata, {"test": "data"})
        self.assertEqual(retrieved_record.user_id, "test-user")
        self.assertEqual(retrieved_record.session_id, "test-session")
        self.assertEqual(retrieved_record.efficiency_score, 0.85)
        self.assertEqual(retrieved_record.iterations, 1)
    
    def test_get_usage_stats(self):
        """Test getting usage statistics"""
        # Insert some test records
        record1 = FeatureUsageRecord(
            record_id="test-record-1",
            feature_name="test_feature",
            category=FeatureCategory.AI_PROVIDER,
            status=FeatureStatus.SUCCESS,
            duration=1.0,
            start_time=datetime.now(),
            end_time=datetime.now(),
            input_size=100,
            output_size=200,
            metadata={},
            user_id="test-user",
            session_id="test-session",
            efficiency_score=0.9
        )
        
        record2 = FeatureUsageRecord(
            record_id="test-record-2",
            feature_name="test_feature",
            category=FeatureCategory.AI_PROVIDER,
            status=FeatureStatus.FAILED,
            duration=2.0,
            start_time=datetime.now(),
            end_time=datetime.now(),
            input_size=150,
            output_size=0,
            metadata={},
            user_id="test-user",
            session_id="test-session",
            error_message="Test error"
        )
        
        self.db.insert_record(record1)
        self.db.insert_record(record2)
        
        # Get usage stats
        stats = self.db.get_usage_stats("test_feature")
        
        self.assertEqual(stats['total_calls'], 2)
        self.assertEqual(stats['success_count'], 1)
        self.assertEqual(stats['failure_count'], 1)
        self.assertAlmostEqual(stats['avg_duration'], 1.5, places=1)
        self.assertAlmostEqual(stats['avg_efficiency'], 0.45, places=2)
        self.assertAlmostEqual(stats['success_rate'], 50.0, places=1)


class TestFeatureTracker(unittest.TestCase):
    """Test the FeatureTracker class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary database file
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_path = self.temp_db.name
        self.tracker = FeatureTracker(self.db_path)
    
    def tearDown(self):
        """Tear down test fixtures"""
        # Clean up the temporary database file
        os.unlink(self.db_path)
    
    def test_track_feature_decorator(self):
        """Test the @track_feature decorator"""
        # Define a test function with the decorator
        @track_feature("test_decorator_feature", FeatureCategory.AI_PROVIDER)
        def test_function(x, y):
            time.sleep(0.1)  # Simulate some work
            return x + y
        
        # Call the function
        result = test_function(5, 3)
        
        # Check the result
        self.assertEqual(result, 8)
        
        # Check that the feature was tracked
        records = self.tracker.db.get_records(feature_name="test_decorator_feature")
        self.assertEqual(len(records), 1)
        
        record = records[0]
        self.assertEqual(record.feature_name, "test_decorator_feature")
        self.assertEqual(record.category, FeatureCategory.AI_PROVIDER)
        self.assertEqual(record.status, FeatureStatus.SUCCESS)
        self.assertGreater(record.duration, 0.05)  # Should be > 0.1s due to sleep
        self.assertLess(record.duration, 0.5)     # Should be < 0.5s
        self.assertEqual(record.input_size, 7)    # "5, 3"
        self.assertEqual(record.output_size, 1)   # "8"
        self.assertGreater(record.efficiency_score, 0.5)  # Should be reasonably efficient
    
    def test_manual_tracking(self):
        """Test manual feature tracking"""
        # Start manual tracking
        record_id = self.tracker.start_custom_tracking(
            "manual_test_feature",
            FeatureCategory.MCP_SERVER,
            metadata={"test_param": "value"},
            user_id="test_user"
        )
        
        # Simulate some work
        time.sleep(0.1)
        
        # Complete manual tracking
        self.tracker.complete_custom_tracking(
            record_id,
            FeatureStatus.SUCCESS,
            input_size=100,
            output_size=50,
            efficiency_score=0.75
        )
        
        # Check that the feature was tracked
        records = self.tracker.db.get_records(feature_name="manual_test_feature")
        self.assertEqual(len(records), 1)
        
        record = records[0]
        self.assertEqual(record.feature_name, "manual_test_feature")
        self.assertEqual(record.category, FeatureCategory.MCP_SERVER)
        self.assertEqual(record.status, FeatureStatus.SUCCESS)
        self.assertGreater(record.duration, 0.05)
        self.assertEqual(record.input_size, 100)
        self.assertEqual(record.output_size, 50)
        self.assertEqual(record.efficiency_score, 0.75)
        self.assertEqual(record.metadata.get("test_param"), "value")
        self.assertEqual(record.user_id, "test_user")
    
    def test_failed_feature_tracking(self):
        """Test tracking of failed features"""
        # Define a function that raises an exception
        @track_feature("failing_feature", FeatureCategory.SYSMON)
        def failing_function():
            raise ValueError("Test error")
        
        # Call the function and expect it to raise an exception
        with self.assertRaises(ValueError):
            failing_function()
        
        # Check that the feature was tracked as failed
        records = self.tracker.db.get_records(feature_name="failing_feature")
        self.assertEqual(len(records), 1)
        
        record = records[0]
        self.assertEqual(record.feature_name, "failing_feature")
        self.assertEqual(record.category, FeatureCategory.SYSMON)
        self.assertEqual(record.status, FeatureStatus.FAILED)
        self.assertIsNotNone(record.error_message)
        self.assertIn("Test error", record.error_message)
        self.assertEqual(record.efficiency_score, 0.0)  # Failed features get 0 efficiency
    
    def test_get_feature_stats(self):
        """Test getting feature statistics"""
        # Track some features
        @track_feature("stats_test_feature", FeatureCategory.AI_PROVIDER)
        def fast_function():
            return "result"
        
        @track_feature("stats_test_feature", FeatureCategory.AI_PROVIDER)
        def slow_function():
            time.sleep(0.1)
            return "result"
        
        # Call the functions multiple times
        for _ in range(3):
            fast_function()
        
        for _ in range(2):
            slow_function()
        
        # Get statistics
        stats = self.tracker.get_feature_stats("stats_test_feature")
        
        self.assertEqual(stats['total_calls'], 5)
        self.assertEqual(stats['success_count'], 5)
        self.assertEqual(stats['failure_count'], 0)
        self.assertGreater(stats['avg_duration'], 0.02)  # Should be > 0 due to sleep
        self.assertLess(stats['avg_duration'], 0.1)      # Should be < 0.1s
        self.assertGreater(stats['avg_efficiency'], 0.5) # Should be reasonably efficient
        self.assertGreater(stats['success_rate'], 90.0)  # Should be high success rate
    
    def test_get_top_features(self):
        """Test getting top features by usage"""
        # Track multiple features with different usage counts
        @track_feature("popular_feature_1", FeatureCategory.AI_PROVIDER)
        def popular_function_1():
            return "result"
        
        @track_feature("popular_feature_2", FeatureCategory.MCP_SERVER)
        def popular_function_2():
            return "result"
        
        @track_feature("unpopular_feature", FeatureCategory.SYSMON)
        def unpopular_function():
            return "result"
        
        # Call popular features multiple times
        for _ in range(10):
            popular_function_1()
        
        for _ in range(5):
            popular_function_2()
        
        # Call unpopular feature once
        unpopular_function()
        
        # Get top features
        top_features = self.tracker.get_top_features(5)
        
        # Check that we got the right number of features
        self.assertEqual(len(top_features), 3)
        
        # Check that features are sorted by usage count (descending)
        self.assertEqual(top_features[0]['feature_name'], 'popular_feature_1')
        self.assertEqual(top_features[0]['usage_count'], 10)
        self.assertEqual(top_features[1]['feature_name'], 'popular_feature_2')
        self.assertEqual(top_features[1]['usage_count'], 5)
        self.assertEqual(top_features[2]['feature_name'], 'unpopular_feature')
        self.assertEqual(top_features[2]['usage_count'], 1)


class TestFeatureTrackingIntegration(unittest.TestCase):
    """Integration tests for the feature tracking system"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary database file
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_path = self.temp_db.name
    
    def tearDown(self):
        """Tear down test fixtures"""
        # Clean up the temporary database file
        os.unlink(self.db_path)
    
    def test_full_tracking_workflow(self):
        """Test the complete feature tracking workflow"""
        # Initialize the tracker
        tracker = FeatureTracker(self.db_path)
        
        # 1. Track a decorated function
        @track_feature("workflow_feature_1", FeatureCategory.AI_PROVIDER)
        def workflow_function_1(data):
            time.sleep(0.05)  # Simulate work
            return f"processed_{data}"
        
        # 2. Track a manual operation
        record_id = tracker.start_custom_tracking(
            "workflow_feature_2",
            FeatureCategory.MCP_SERVER,
            metadata={"operation": "data_processing"}
        )
        
        # 3. Execute the decorated function
        result1 = workflow_function_1("test_data")
        self.assertEqual(result1, "processed_test_data")
        
        # 4. Simulate manual operation
        time.sleep(0.1)  # Simulate work
        tracker.complete_custom_tracking(
            record_id,
            FeatureStatus.SUCCESS,
            input_size=1000,
            output_size=500,
            efficiency_score=0.8
        )
        
        # 5. Verify tracking results
        all_records = tracker.get_all_records()
        self.assertEqual(len(all_records), 2)
        
        # Check decorated function record
        decorated_records = [r for r in all_records if r.feature_name == "workflow_feature_1"]
        self.assertEqual(len(decorated_records), 1)
        self.assertEqual(decorated_records[0].status, FeatureStatus.SUCCESS)
        self.assertGreater(decorated_records[0].duration, 0.02)
        self.assertEqual(decorated_records[0].input_size, 14)  # "'test_data'"
        self.assertEqual(decorated_records[0].output_size, 23)  # "'processed_test_data'"
        
        # Check manual operation record
        manual_records = [r for r in all_records if r.feature_name == "workflow_feature_2"]
        self.assertEqual(len(manual_records), 1)
        self.assertEqual(manual_records[0].status, FeatureStatus.SUCCESS)
        self.assertGreater(manual_records[0].duration, 0.05)
        self.assertEqual(manual_records[0].input_size, 1000)
        self.assertEqual(manual_records[0].output_size, 500)
        self.assertEqual(manual_records[0].efficiency_score, 0.8)
        self.assertEqual(manual_records[0].metadata.get("operation"), "data_processing")
    
    def test_concurrent_tracking(self):
        """Test concurrent feature tracking"""
        import threading
        import concurrent.futures
        
        tracker = FeatureTracker(self.db_path)
        
        # Define a function to track
        @track_feature("concurrent_feature", FeatureCategory.AI_PROVIDER)
        def concurrent_function(thread_id):
            time.sleep(0.01)  # Small delay
            return f"result_from_thread_{thread_id}"
        
        # Run multiple threads concurrently
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(concurrent_function, i) for i in range(10)]
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
        
        # Verify all functions completed
        self.assertEqual(len(results), 10)
        
        # Verify all were tracked
        records = tracker.get_all_records(feature_name="concurrent_feature")
        self.assertEqual(len(records), 10)
        
        # Verify all succeeded
        success_count = sum(1 for r in records if r.status == FeatureStatus.SUCCESS)
        self.assertEqual(success_count, 10)


if __name__ == '__main__':
    unittest.main()