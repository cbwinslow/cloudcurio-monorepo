"""
CloudCurio Test Configuration
Configuration settings for the test suite
"""

import os
from typing import Dict, Any


class TestConfig:
    """Test configuration class"""
    
    def __init__(self):
        self.config = {
            # Database configuration
            "database": {
                "url": os.getenv("TEST_DATABASE_URL", "sqlite:///./test.db"),
                "pool_size": int(os.getenv("TEST_DB_POOL_SIZE", "5")),
                "max_overflow": int(os.getenv("TEST_DB_MAX_OVERFLOW", "10"))
            },
            
            # API configuration
            "api": {
                "base_url": os.getenv("TEST_API_BASE_URL", "http://localhost:8000"),
                "timeout": int(os.getenv("TEST_API_TIMEOUT", "30")),
                "retries": int(os.getenv("TEST_API_RETRIES", "3"))
            },
            
            # AI provider configuration
            "ai_providers": {
                "default": os.getenv("TEST_DEFAULT_AI_PROVIDER", "openrouter"),
                "openrouter": {
                    "api_key": os.getenv("TEST_OPENROUTER_API_KEY", ""),
                    "model": os.getenv("TEST_OPENROUTER_MODEL", "mistralai/mistral-7b-instruct")
                },
                "openai": {
                    "api_key": os.getenv("TEST_OPENAI_API_KEY", ""),
                    "model": os.getenv("TEST_OPENAI_MODEL", "gpt-3.5-turbo")
                },
                "gemini": {
                    "api_key": os.getenv("TEST_GEMINI_API_KEY", ""),
                    "model": os.getenv("TEST_GEMINI_MODEL", "gemini-pro")
                }
            },
            
            # Test execution configuration
            "execution": {
                "parallel": os.getenv("TEST_PARALLEL", "true").lower() == "true",
                "max_workers": int(os.getenv("TEST_MAX_WORKERS", "4")),
                "timeout": int(os.getenv("TEST_TIMEOUT", "300")),  # 5 minutes
                "retry_attempts": int(os.getenv("TEST_RETRY_ATTEMPTS", "3"))
            },
            
            # Test reporting configuration
            "reporting": {
                "output_dir": os.getenv("TEST_OUTPUT_DIR", "./test-results"),
                "format": os.getenv("TEST_REPORT_FORMAT", "html"),
                "generate_coverage": os.getenv("TEST_GENERATE_COVERAGE", "true").lower() == "true",
                "coverage_threshold": int(os.getenv("TEST_COVERAGE_THRESHOLD", "80"))
            },
            
            # Test environment configuration
            "environment": {
                "debug": os.getenv("TEST_DEBUG", "false").lower() == "true",
                "log_level": os.getenv("TEST_LOG_LEVEL", "INFO"),
                "capture_output": os.getenv("TEST_CAPTURE_OUTPUT", "true").lower() == "true"
            },
            
            # Feature tracking test configuration
            "feature_tracking": {
                "enabled": os.getenv("TEST_FEATURE_TRACKING_ENABLED", "true").lower() == "true",
                "database_url": os.getenv("TEST_FT_DATABASE_URL", "sqlite:///./test_feature_tracking.db"),
                "track_all": os.getenv("TEST_FT_TRACK_ALL", "false").lower() == "true"
            },
            
            # Security test configuration
            "security": {
                "scan_dependencies": os.getenv("TEST_SECURITY_SCAN_DEPENDENCIES", "true").lower() == "true",
                "scan_code": os.getenv("TEST_SECURITY_SCAN_CODE", "true").lower() == "true",
                "fail_on_critical": os.getenv("TEST_SECURITY_FAIL_ON_CRITICAL", "true").lower() == "true"
            }
        }
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """Get configuration value by dot-separated key path"""
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any):
        """Set configuration value by dot-separated key path"""
        keys = key_path.split('.')
        config = self.config
        
        # Navigate to the parent of the target key
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # Set the value
        config[keys[-1]] = value
    
    def update(self, updates: Dict[str, Any]):
        """Update configuration with a dictionary of values"""
        def deep_update(original: Dict, updates: Dict):
            for key, value in updates.items():
                if isinstance(value, dict) and key in original and isinstance(original[key], dict):
                    deep_update(original[key], value)
                else:
                    original[key] = value
        
        deep_update(self.config, updates)


# Global test configuration instance
test_config = TestConfig()


# Test environment setup
def setup_test_environment():
    """Setup test environment based on configuration"""
    import logging
    
    # Configure logging
    log_level = test_config.get("environment.log_level", "INFO")
    logging.basicConfig(level=getattr(logging, log_level))
    
    # Create output directory
    output_dir = test_config.get("reporting.output_dir", "./test-results")
    os.makedirs(output_dir, exist_ok=True)
    
    # Setup database
    database_url = test_config.get("database.url", "sqlite:///./test.db")
    # Database setup would go here
    
    print(f"🔧 Test environment configured with log level: {log_level}")
    print(f"📂 Test output directory: {output_dir}")
    print(f"🗄️  Test database: {database_url}")


# Test utilities
def get_test_database_url():
    """Get test database URL"""
    return test_config.get("database.url", "sqlite:///./test.db")


def get_test_api_base_url():
    """Get test API base URL"""
    return test_config.get("api.base_url", "http://localhost:8000")


def is_parallel_execution_enabled():
    """Check if parallel test execution is enabled"""
    return test_config.get("execution.parallel", True)


def get_max_workers():
    """Get maximum number of workers for parallel execution"""
    return test_config.get("execution.max_workers", 4)


# Setup test environment on import
setup_test_environment()