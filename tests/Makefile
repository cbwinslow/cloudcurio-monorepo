# CloudCurio Testing Makefile
# Comprehensive testing automation for all test types

# Variables
PYTHON = python3
PIP = pip3
VENV = venv
VENV_BIN = $(VENV)/bin
TEST_DIR = tests
UNIT_TEST_DIR = $(TEST_DIR)/unit
INTEGRATION_TEST_DIR = $(TEST_DIR)/integration
E2E_TEST_DIR = $(TEST_DIR)/e2e
PERFORMANCE_TEST_DIR = $(TEST_DIR)/performance
SECURITY_TEST_DIR = $(TEST_DIR)/security
ACCESSIBILITY_TEST_DIR = $(TEST_DIR)/accessibility
CROSS_BROWSER_TEST_DIR = $(TEST_DIR)/cross_browser
MOBILE_TEST_DIR = $(TEST_DIR)/mobile
CHAOS_TEST_DIR = $(TEST_DIR)/chaos
CONTRACT_TEST_DIR = $(TEST_DIR)/contract
MUTATION_TEST_DIR = $(TEST_DIR)/mutation
PROPERTY_TEST_DIR = $(TEST_DIR)/property

# Default target
.PHONY: help
help:
	@echo "CloudCurio Testing Automation"
	@echo "============================="
	@echo "make setup            - Setup testing environment"
	@echo "make install-dev      - Install development dependencies"
	@echo "make test             - Run all tests"
	@echo "make test-unit        - Run unit tests"
	@echo "make test-integration - Run integration tests"
	@echo "make test-e2e         - Run end-to-end tests"
	@echo "make test-performance - Run performance tests"
	@echo "make test-security    - Run security tests"
	@echo "make test-accessibility - Run accessibility tests"
	@echo "make test-cross-browser - Run cross-browser tests"
	@echo "make test-mobile      - Run mobile tests"
	@echo "make test-chaos       - Run chaos engineering tests"
	@echo "make test-contract    - Run contract tests"
	@echo "make test-mutation    - Run mutation tests"
	@echo "make test-property    - Run property-based tests"
	@echo "make coverage         - Generate coverage report"
	@echo "make clean            - Clean test artifacts"

# Setup testing environment
.PHONY: setup
setup:
	@echo "Setting up CloudCurio testing environment..."
	@if [ ! -d "$(VENV)" ]; then \
		$(PYTHON) -m venv $(VENV); \
		echo "Virtual environment created"; \
	fi
	@$(VENV_BIN)/$(PIP) install --upgrade pip
	@echo "Testing environment setup complete"

# Install development dependencies
.PHONY: install-dev
install-dev: setup
	@echo "Installing development dependencies..."
	@$(VENV_BIN)/$(PIP) install pytest pytest-cov pytest-asyncio pytest-mock
	@$(VENV_BIN)/$(PIP) install flake8 black mypy pylint
	@$(VENV_BIN)/$(PIP) install bandit safety
	@$(VENV_BIN)/$(PIP) install playwright selenium
	@$(VENV_BIN)/$(PIP) install locust k6 vegeta
	@$(VENV_BIN)/$(PIP) install hypothesis
	@echo "Development dependencies installed"

# Run all tests
.PHONY: test
test: test-unit test-integration test-e2e test-security test-accessibility

# Run unit tests
.PHONY: test-unit
test-unit: install-dev
	@echo "Running unit tests..."
	@$(VENV_BIN)/$(PYTHON) -m pytest $(UNIT_TEST_DIR) -v --cov=. --cov-report=term-missing
	@echo "Unit tests completed"

# Run integration tests
.PHONY: test-integration
test-integration: install-dev
	@echo "Running integration tests..."
	@$(VENV_BIN)/$(PYTHON) -m pytest $(INTEGRATION_TEST_DIR) -v
	@echo "Integration tests completed"

# Run end-to-end tests
.PHONY: test-e2e
test-e2e: install-dev
	@echo "Running end-to-end tests..."
	@$(VENV_BIN)/$(PYTHON) -m pytest $(E2E_TEST_DIR) -v
	@echo "End-to-end tests completed"

# Run performance tests
.PHONY: test-performance
test-performance: install-dev
	@echo "Running performance tests..."
	@$(VENV_BIN)/$(PYTHON) -m pytest $(PERFORMANCE_TEST_DIR) -v
	@echo "Performance tests completed"

# Run security tests
.PHONY: test-security
test-security: install-dev
	@echo "Running security tests..."
	@$(VENV_BIN)/$(PYTHON) -m pytest $(SECURITY_TEST_DIR) -v
	@echo "Security tests completed"

# Run accessibility tests
.PHONY: test-accessibility
test-accessibility: install-dev
	@echo "Running accessibility tests..."
	@$(VENV_BIN)/$(PYTHON) -m pytest $(ACCESSIBILITY_TEST_DIR) -v
	@echo "Accessibility tests completed"

# Run cross-browser tests
.PHONY: test-cross-browser
test-cross-browser: install-dev
	@echo "Running cross-browser tests..."
	@$(VENV_BIN)/$(PYTHON) -m pytest $(CROSS_BROWSER_TEST_DIR) -v
	@echo "Cross-browser tests completed"

# Run mobile tests
.PHONY: test-mobile
test-mobile: install-dev
	@echo "Running mobile tests..."
	@$(VENV_BIN)/$(PYTHON) -m pytest $(MOBILE_TEST_DIR) -v
	@echo "Mobile tests completed"

# Run chaos engineering tests
.PHONY: test-chaos
test-chaos: install-dev
	@echo "Running chaos engineering tests..."
	@$(VENV_BIN)/$(PYTHON) -m pytest $(CHAOS_TEST_DIR) -v
	@echo "Chaos engineering tests completed"

# Run contract tests
.PHONY: test-contract
test-contract: install-dev
	@echo "Running contract tests..."
	@$(VENV_BIN)/$(PYTHON) -m pytest $(CONTRACT_TEST_DIR) -v
	@echo "Contract tests completed"

# Run mutation tests
.PHONY: test-mutation
test-mutation: install-dev
	@echo "Running mutation tests..."
	@$(VENV_BIN)/$(PYTHON) -m pytest $(MUTATION_TEST_DIR) -v
	@echo "Mutation tests completed"

# Run property-based tests
.PHONY: test-property
test-property: install-dev
	@echo "Running property-based tests..."
	@$(VENV_BIN)/$(PYTHON) -m pytest $(PROPERTY_TEST_DIR) -v
	@echo "Property-based tests completed"

# Generate coverage report
.PHONY: coverage
coverage: install-dev
	@echo "Generating coverage report..."
	@$(VENV_BIN)/$(PYTHON) -m pytest --cov=. --cov-report=html --cov-report=xml --cov-report=term
	@echo "Coverage report generated in htmlcov/ directory"

# Clean test artifacts
.PHONY: clean
clean:
	@echo "Cleaning test artifacts..."
	rm -rf htmlcov/ .coverage coverage.xml
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name "*.py,cover" -delete
	@echo "Test artifacts cleaned"