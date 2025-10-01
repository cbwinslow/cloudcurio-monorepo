"""
CloudCurio Feature Tracking CLI Tests
Tests for the command-line interface of the feature tracking system
"""

import unittest
import tempfile
import os
import sys
from unittest.mock import patch, MagicMock
from io import StringIO

# Add the project root to the path so we can import the CLI module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from feature_tracking.cli import FeatureTrackingCLI


class TestFeatureTrackingCLI(unittest.TestCase):
    """Test the FeatureTrackingCLI class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary database file
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_path = self.temp_db.name
        
        # Initialize CLI with temp database
        self.cli = FeatureTrackingCLI(db_path=self.db_path)
    
    def tearDown(self):
        """Tear down test fixtures"""
        # Clean up the temporary database file
        os.unlink(self.db_path)
    
    def test_cli_initialization(self):
        """Test CLI initialization"""
        self.assertIsNotNone(self.cli)
        self.assertIsNotNone(self.cli.tracker)
        self.assertEqual(self.cli.tracker.db_path, self.db_path)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_features_command(self, mock_stdout):
        """Test the list-features command"""
        # Mock the tracker's get_top_features method
        with patch.object(self.cli.tracker, 'get_top_features') as mock_get_top_features:
            mock_get_top_features.return_value = [
                {"feature_name": "test_feature_1", "usage_count": 10, "avg_duration": 0.5, "success_rate": 90.0},
                {"feature_name": "test_feature_2", "usage_count": 5, "avg_duration": 1.2, "success_rate": 80.0}
            ]
            
            # Run the command
            self.cli.list_features(limit=10)
            
            # Check output
            output = mock_stdout.getvalue()
            self.assertIn("Top Features by Usage", output)
            self.assertIn("test_feature_1", output)
            self.assertIn("test_feature_2", output)
            self.assertIn("10 calls", output)
            self.assertIn("5 calls", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_feature_stats_command(self, mock_stdout):
        """Test the feature-stats command"""
        # Mock the tracker's get_feature_stats method
        with patch.object(self.cli.tracker, 'get_feature_stats') as mock_get_feature_stats:
            mock_get_feature_stats.return_value = {
                "total_calls": 25,
                "success_count": 20,
                "failure_count": 5,
                "avg_duration": 0.75,
                "avg_efficiency": 0.85,
                "success_rate": 80.0
            }
            
            # Run the command
            self.cli.feature_stats("test_feature")
            
            # Check output
            output = mock_stdout.getvalue()
            self.assertIn("Statistics for feature: test_feature", output)
            self.assertIn("Total calls: 25", output)
            self.assertIn("Success count: 20", output)
            self.assertIn("Failure count: 5", output)
            self.assertIn("Average duration: 0.750s", output)
            self.assertIn("Success rate: 80.0%", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_records_command(self, mock_stdout):
        """Test the list-records command"""
        # Mock the tracker's get_all_records method
        with patch.object(self.cli.tracker, 'get_all_records') as mock_get_all_records:
            from datetime import datetime
            mock_records = [
                MagicMock(
                    feature_name="test_feature_1",
                    status="success",
                    duration=0.5,
                    start_time=datetime.now(),
                    end_time=datetime.now(),
                    efficiency_score=0.9,
                    user_id="test_user"
                ),
                MagicMock(
                    feature_name="test_feature_2",
                    status="failed",
                    duration=1.2,
                    start_time=datetime.now(),
                    end_time=datetime.now(),
                    error_message="Test error",
                    user_id="test_user"
                )
            ]
            mock_get_all_records.return_value = mock_records
            
            # Run the command
            self.cli.list_records(limit=20)
            
            # Check output
            output = mock_stdout.getvalue()
            self.assertIn("Feature Usage Records", output)
            self.assertIn("test_feature_1", output)
            self.assertIn("test_feature_2", output)
            self.assertIn("0.500s", output)
            self.assertIn("1.200s", output)
            self.assertIn("success", output)
            self.assertIn("failed", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_dashboard_command(self, mock_stdout):
        """Test the dashboard command"""
        # Mock the tracker's get_dashboard_data method
        with patch.object(self.cli.tracker, 'get_dashboard_data') as mock_get_dashboard_data:
            mock_get_dashboard_data.return_value = {
                "total_features": 15,
                "total_calls": 1250,
                "success_rate": 87.5,
                "avg_duration": 0.65,
                "top_features": [
                    {"feature_name": "ai_generation", "usage_count": 300},
                    {"feature_name": "mcp_server", "usage_count": 250},
                    {"feature_name": "sysmon_check", "usage_count": 200}
                ]
            }
            
            # Run the command
            self.cli.dashboard()
            
            # Check output
            output = mock_stdout.getvalue()
            self.assertIn("CloudCurio Feature Tracking Dashboard", output)
            self.assertIn("Total Features: 15", output)
            self.assertIn("Total Calls: 1250", output)
            self.assertIn("Success Rate: 87.5%", output)
            self.assertIn("Average Duration: 0.650s", output)
            self.assertIn("ai_generation", output)
            self.assertIn("mcp_server", output)
            self.assertIn("sysmon_check", output)
    
    def test_run_cli_with_commands(self):
        """Test running CLI with various commands"""
        # Test help command
        with patch('sys.stdout', new_callable=StringIO):
            with self.assertRaises(SystemExit):
                self.cli.run(["--help"])
        
        # Test list-features command
        with patch('sys.stdout', new_callable=StringIO):
            with patch.object(self.cli.tracker, 'get_top_features') as mock_get_top_features:
                mock_get_top_features.return_value = []
                self.cli.run(["list-features"])
        
        # Test feature-stats command
        with patch('sys.stdout', new_callable=StringIO):
            with patch.object(self.cli.tracker, 'get_feature_stats') as mock_get_feature_stats:
                mock_get_feature_stats.return_value = {}
                self.cli.run(["feature-stats", "test_feature"])
        
        # Test list-records command
        with patch('sys.stdout', new_callable=StringIO):
            with patch.object(self.cli.tracker, 'get_all_records') as mock_get_all_records:
                mock_get_all_records.return_value = []
                self.cli.run(["list-records"])
        
        # Test dashboard command
        with patch('sys.stdout', new_callable=StringIO):
            with patch.object(self.cli.tracker, 'get_dashboard_data') as mock_get_dashboard_data:
                mock_get_dashboard_data.return_value = {}
                self.cli.run(["dashboard"])
    
    def test_cli_error_handling(self):
        """Test CLI error handling"""
        # Test invalid command
        with patch('sys.stderr', new_callable=StringIO):
            with self.assertRaises(SystemExit):
                self.cli.run(["invalid-command"])
        
        # Test missing arguments
        with patch('sys.stderr', new_callable=StringIO):
            with self.assertRaises(SystemExit):
                self.cli.run(["feature-stats"])  # Missing feature name


if __name__ == '__main__':
    unittest.main()