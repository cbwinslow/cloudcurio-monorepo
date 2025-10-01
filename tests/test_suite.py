"""
CloudCurio Comprehensive Test Suite
Run all tests for the CloudCurio platform
"""

import unittest
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Import all test modules
from tests.unit.test_feature_tracking import *
from tests.unit.test_feature_tracking_cli import *
from tests.integration.test_feature_tracking_integration import *
from tests.e2e.test_feature_tracking_e2e import *


class CloudCurioTestSuite(unittest.TestSuite):
    """Comprehensive test suite for CloudCurio platform"""
    
    def __init__(self):
        super().__init__()
        
        # Add all test cases to the suite
        self.addTest(unittest.makeSuite(TestFeatureTrackerDB))
        self.addTest(unittest.makeSuite(TestFeatureTracker))
        self.addTest(unittest.makeSuite(TestFeatureTrackingIntegration))
        self.addTest(unittest.makeSuite(TestFeatureTrackingCLI))
        self.addTest(unittest.makeSuite(TestFeatureTrackingEndToEnd))


def run_all_tests():
    """Run all CloudCurio tests"""
    print("🧪 Running CloudCurio Comprehensive Test Suite...")
    print("=" * 50)
    
    # Create test suite
    suite = CloudCurioTestSuite()
    
    # Create test runner
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Run tests
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {(result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100:.1f}%")
    
    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\n💥 Errors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    if len(result.failures) == 0 and len(result.errors) == 0:
        print("\n🎉 All tests passed!")
        return True
    else:
        print("\n⚠️  Some tests failed. Please review the output above.")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)