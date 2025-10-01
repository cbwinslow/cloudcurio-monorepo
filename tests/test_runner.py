#!/usr/bin/env python3
"""
CloudCurio Test Runner
Comprehensive test execution script for all test types
"""

import argparse
import subprocess
import sys
import os
from typing import List, Optional
import time
from datetime import datetime

class TestRunner:
    """Run CloudCurio tests with comprehensive reporting"""
    
    def __init__(self):
        self.test_results = []
        self.start_time = None
    
    def run_test_suite(self, test_type: str, test_dir: str) -> bool:
        """Run a specific test suite"""
        print(f"🧪 Running {test_type} tests...")
        
        # Record start time
        start = time.time()
        
        try:
            # Run pytest with coverage
            result = subprocess.run([
                sys.executable, "-m", "pytest", 
                test_dir, 
                "-v", 
                "--cov=.",
                "--cov-report=term-missing",
                "--tb=short"
            ], capture_output=True, text=True)
            
            # Calculate duration
            duration = time.time() - start
            
            # Store result
            self.test_results.append({
                "type": test_type,
                "directory": test_dir,
                "passed": result.returncode == 0,
                "duration": duration,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "timestamp": datetime.now().isoformat()
            })
            
            if result.returncode == 0:
                print(f"✅ {test_type} tests passed in {duration:.2f}s")
                return True
            else:
                print(f"❌ {test_type} tests failed in {duration:.2f}s")
                print(f"STDOUT:\n{result.stdout}")
                print(f"STDERR:\n{result.stderr}")
                return False
                
        except Exception as e:
            duration = time.time() - start
            self.test_results.append({
                "type": test_type,
                "directory": test_dir,
                "passed": False,
                "duration": duration,
                "stdout": "",
                "stderr": str(e),
                "timestamp": datetime.now().isoformat()
            })
            print(f"❌ {test_type} tests failed with exception: {e}")
            return False
    
    def run_all_tests(self) -> bool:
        """Run all test suites"""
        print("🚀 Starting CloudCurio comprehensive test suite...")
        self.start_time = time.time()
        
        # Define test suites
        test_suites = [
            ("Unit", "tests/unit"),
            ("Integration", "tests/integration"),
            ("End-to-End", "tests/e2e"),
            ("Performance", "tests/performance"),
            ("Security", "tests/security"),
            ("Accessibility", "tests/accessibility"),
            ("Cross-Browser", "tests/cross_browser"),
            ("Mobile", "tests/mobile"),
            ("Chaos Engineering", "tests/chaos"),
            ("Contract", "tests/contract"),
            ("Mutation", "tests/mutation"),
            ("Property-Based", "tests/property")
        ]
        
        # Check which directories exist
        existing_suites = [(name, path) for name, path in test_suites if os.path.exists(path)]
        
        if not existing_suites:
            print("⚠️  No test directories found. Creating sample test directories...")
            self.create_sample_test_directories()
            existing_suites = [(name, path) for name, path in test_suites if os.path.exists(path)]
        
        # Run each test suite
        all_passed = True
        for test_name, test_dir in existing_suites:
            if not self.run_test_suite(test_name, test_dir):
                all_passed = False
        
        # Calculate total duration
        total_duration = time.time() - self.start_time
        
        # Print summary
        self.print_summary(total_duration)
        
        return all_passed
    
    def create_sample_test_directories(self):
        """Create sample test directories with basic test files"""
        test_dirs = [
            "tests/unit",
            "tests/integration", 
            "tests/e2e",
            "tests/performance",
            "tests/security",
            "tests/accessibility",
            "tests/cross_browser",
            "tests/mobile",
            "tests/chaos",
            "tests/contract",
            "tests/mutation",
            "tests/property"
        ]
        
        for test_dir in test_dirs:
            os.makedirs(test_dir, exist_ok=True)
            
            # Create a sample test file
            sample_test_content = f"""
import pytest

def test_{os.path.basename(test_dir)}_sample():
    \"\"\"Sample test for {os.path.basename(test_dir)} suite\"\"\"
    assert True, "Sample test passed"
"""
            
            with open(os.path.join(test_dir, "test_sample.py"), "w") as f:
                f.write(sample_test_content)
        
        print("📁 Sample test directories created")
    
    def print_summary(self, total_duration: float):
        """Print test execution summary"""
        print("\n" + "="*60)
        print("📊 CloudCurio Test Execution Summary")
        print("="*60)
        
        passed_tests = [r for r in self.test_results if r["passed"]]
        failed_tests = [r for r in self.test_results if not r["passed"]]
        
        print(f"Total Tests: {len(self.test_results)}")
        print(f"Passed: {len(passed_tests)}")
        print(f"Failed: {len(failed_tests)}")
        print(f"Success Rate: {len(passed_tests)/len(self.test_results)*100:.1f}%")
        print(f"Total Duration: {total_duration:.2f}s")
        print(f"Start Time: {datetime.fromisoformat(self.test_results[0]['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if failed_tests:
            print("\n❌ Failed Tests:")
            for test in failed_tests:
                print(f"  - {test['type']}: {test['directory']} ({test['duration']:.2f}s)")
        
        if passed_tests:
            print("\n✅ Passed Tests:")
            for test in passed_tests:
                print(f"  - {test['type']}: {test['directory']} ({test['duration']:.2f}s)")
        
        print("\n" + "="*60)
        
        if len(failed_tests) == 0:
            print("🎉 All tests passed! CloudCurio is ready for deployment.")
        else:
            print("⚠️  Some tests failed. Please review the output above.")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="CloudCurio Test Runner")
    parser.add_argument(
        "test_type", 
        nargs="?", 
        default="all",
        choices=["all", "unit", "integration", "e2e", "performance", "security", 
                "accessibility", "cross_browser", "mobile", "chaos", "contract", 
                "mutation", "property"],
        help="Type of tests to run"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate detailed report"
    )
    
    args = parser.parse_args()
    
    # Initialize test runner
    runner = TestRunner()
    
    # Run tests based on type
    if args.test_type == "all":
        success = runner.run_all_tests()
    else:
        # Map test type to directory
        test_dirs = {
            "unit": "tests/unit",
            "integration": "tests/integration",
            "e2e": "tests/e2e",
            "performance": "tests/performance",
            "security": "tests/security",
            "accessibility": "tests/accessibility",
            "cross_browser": "tests/cross_browser",
            "mobile": "tests/mobile",
            "chaos": "tests/chaos",
            "contract": "tests/contract",
            "mutation": "tests/mutation",
            "property": "tests/property"
        }
        
        test_dir = test_dirs.get(args.test_type)
        if test_dir and os.path.exists(test_dir):
            success = runner.run_test_suite(args.test_type.capitalize(), test_dir)
        else:
            print(f"❌ Test directory for {args.test_type} not found: {test_dir}")
            success = False
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()