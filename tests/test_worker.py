import unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
import os
import json

# Add the worker directory to the path so we can import the worker script
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'worker'))

class TestReviewWorker(unittest.TestCase):
    def setUp(self):
        # Import the worker script
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "review_worker_v2", 
            os.path.join(os.path.dirname(__file__), '..', 'worker', 'review_worker_v2.py')
        )
        self.worker_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.worker_module)

    @patch('builtins.print')
    def test_log_function(self, mock_print):
        """Test the log function outputs JSON"""
        self.worker_module.log("test message", key="value")
        
        # Check that print was called
        mock_print.assert_called_once()
        
        # Check that the output is valid JSON
        printed_output = mock_print.call_args[0][0]
        parsed_json = json.loads(printed_output)
        
        self.assertEqual(parsed_json["msg"], "test message")
        self.assertEqual(parsed_json["key"], "value")
        self.assertIn("ts", parsed_json)

    def test_device_initialization(self):
        """Test Device class initialization"""
        device = self.worker_module.Device("rtx3060", "0", "quick")
        
        self.assertEqual(device.label, "rtx3060")
        self.assertEqual(device.index, "0")
        self.assertEqual(device.klass, "quick")
        self.assertFalse(device.busy)
        self.assertTrue(device.healthy)

    @patch('subprocess.Popen')
    def test_run_command_success(self, mock_popen):
        """Test run function with successful command execution"""
        # Mock subprocess.Popen to return a successful result
        mock_process = MagicMock()
        mock_process.communicate.return_value = ("output", "error")
        mock_process.returncode = 0
        mock_popen.return_value = mock_process
        
        code, out, err = self.worker_module.run(["echo", "test"])
        
        self.assertEqual(code, 0)
        self.assertEqual(out, "output")
        self.assertEqual(err, "error")

    @patch('subprocess.Popen')
    def test_run_command_timeout(self, mock_popen):
        """Test run function with command timeout"""
        # Mock subprocess.Popen to raise TimeoutExpired
        mock_process = MagicMock()
        mock_process.communicate.side_effect = subprocess.TimeoutExpired("cmd", 1)
        mock_process.kill = MagicMock()
        mock_popen.return_value = mock_process
        
        code, out, err = self.worker_module.run(["sleep", "10"], timeout=1)
        
        self.assertEqual(code, 124)  # 124 is the standard timeout exit code
        self.assertEqual(out, "")
        self.assertEqual(err, "timeout")

if __name__ == '__main__':
    unittest.main()