# CloudCurio Makefile
# Comprehensive build and packaging system for CloudCurio platform

# Variables
VERSION = 1.0.0
NAME = cloudcurio
PYTHON = python3
PIP = pip3
VENV = venv
VENV_BIN = $(VENV)/bin
REQ_DIR = .
BUILD_DIR = build
DIST_DIR = dist
DOCS_DIR = docs
TEST_DIR = tests

# Default target
.PHONY: help
help:
	@echo "CloudCurio Build System"
	@echo "======================="
	@echo "make setup            - Setup development environment"
	@echo "make install          - Install CloudCurio"
	@echo "make install-dev      - Install development dependencies"
	@echo "make build            - Build CloudCurio packages"
	@echo "make build-pip        - Build pip package"
	@echo "make build-docker     - Build Docker images"
	@echo "make test             - Run tests"
	@echo "make test-unit        - Run unit tests"
	@echo "make test-integration - Run integration tests"
	@echo "make docs             - Build documentation"
	@echo "make clean            - Clean build artifacts"
	@echo "make clean-all        - Clean everything including venv"
	@echo "make run-mcp          - Run MCP server"
	@echo "make run-config-editor - Run configuration editor"
	@echo "make run-sysmon       - Run system monitor"
	@echo "make release          - Create release artifacts"
	@echo "make release-pip      - Build and upload pip package"
	@echo "make release-docker   - Build and upload docker images"
	@echo "make deploy           - Deploy to target environment"
	@echo "make agentic-setup    - Setup agentic environment"
	@echo "make agentic-run      - Run agentic platform"

# Setup development environment
.PHONY: setup
setup:
	@echo "Setting up CloudCurio development environment..."
	@if [ ! -d "$(VENV)" ]; then \
		$(PYTHON) -m venv $(VENV); \
		echo "Virtual environment created"; \
	fi
	@$(VENV_BIN)/$(PIP) install --upgrade pip
	@$(VENV_BIN)/$(PIP) install -r $(REQ_DIR)/crew/requirements.txt
	@$(VENV_BIN)/$(PIP) install -r $(REQ_DIR)/config_editor/requirements.txt
	@$(VENV_BIN)/$(PIP) install -r $(REQ_DIR)/ai_tools/requirements.txt
	@echo "Development environment setup complete"

# Install CloudCurio
.PHONY: install
install: setup
	@echo "Installing CloudCurio..."
	@$(VENV_BIN)/$(PIP) install .
	@echo "CloudCurio installed"

# Install development dependencies
.PHONY: install-dev
install-dev: setup
	@echo "Installing development dependencies..."
	@$(VENV_BIN)/$(PIP) install pytest pytest-cov flake8 black mypy
	@echo "Development dependencies installed"

# Build pip package
.PHONY: build-pip
build-pip:
	@echo "Building pip package for CloudCurio..."
	@$(PYTHON) -m pip install build
	@$(PYTHON) -m build --wheel
	@echo "Pip package built in $(DIST_DIR)/ directory"

# Build Docker images
.PHONY: build-docker
build-docker:
	@echo "Building Docker images for CloudCurio..."
	docker build -f Dockerfile.mcp -t cbwinslow/cloudcurio-mcp:$(VERSION) .
	docker build -f Dockerfile.mcp -t cbwinslow/cloudcurio-mcp:latest .
	@echo "Docker images built"

# Build all packages
.PHONY: build
build: build-pip build-docker
	@echo "All packages built successfully"

# Run tests
.PHONY: test
test: test-unit test-integration
	@echo "All tests passed"

.PHONY: test-unit
test-unit:
	@echo "Running unit tests..."
	@$(VENV_BIN)/$(PYTHON) -m pytest $(TEST_DIR)/unit/ -v

.PHONY: test-integration
test-integration:
	@echo "Running integration tests..."
	@$(VENV_BIN)/$(PYTHON) -m pytest $(TEST_DIR)/integration/ -v

# Build documentation
.PHONY: docs
docs:
	@echo "Building documentation..."
	@$(VENV_BIN)/$(PYTHON) -m pip install sphinx
	@cd $(DOCS_DIR) && $(VENV_BIN)/sphinx-build -b html . _build/html
	@echo "Documentation built in $(DOCS_DIR)/_build/html/"

# Clean build artifacts
.PHONY: clean
clean:
	@echo "Cleaning build artifacts..."
	rm -rf $(BUILD_DIR) $(DIST_DIR) *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "Build artifacts cleaned"

# Clean everything
.PHONY: clean-all
clean-all: clean
	@echo "Cleaning everything including virtual environment..."
	rm -rf $(VENV)
	@echo "Everything cleaned"

# Run MCP server
.PHONY: run-mcp
run-mcp: setup
	@echo "Starting CloudCurio MCP Server..."
	@$(VENV_BIN)/$(PYTHON) crew/mcp_server/start_server.py

# Run configuration editor
.PHONY: run-config-editor
run-config-editor: setup
	@echo "Starting CloudCurio Configuration Editor..."
	@$(VENV_BIN)/$(PYTHON) config_editor/launcher.py

# Run system monitor
.PHONY: run-sysmon
run-sysmon: setup
	@echo "Starting CloudCurio SysMon..."
	@$(VENV_BIN)/cloudcurio-sysmon monitor --continuous

# Create release artifacts
.PHONY: release
release: build
	@echo "Creating release artifacts for version $(VERSION)..."
	mkdir -p releases/v$(VERSION)
	cp -r $(DIST_DIR)/* releases/v$(VERSION)/
	@echo "Release artifacts created in releases/v$(VERSION)/"

# Upload pip package (requires PyPI credentials)
.PHONY: release-pip
release-pip:
	@echo "Uploading pip package..."
	@$(PYTHON) -m pip install twine
	@$(PYTHON) -m twine upload $(DIST_DIR)/*

# Upload docker images
.PHONY: release-docker
release-docker: build-docker
	@echo "Uploading Docker images..."
	docker push cbwinslow/cloudcurio-mcp:$(VERSION)
	docker push cbwinslow/cloudcurio-mcp:latest

# Deploy to target environment
.PHONY: deploy
deploy:
	@echo "Deploying CloudCurio version $(VERSION)..."
	@echo "Deployment steps would be implemented here"

# Setup agentic environment
.PHONY: agentic-setup
agentic-setup: setup
	@echo "Setting up agentic environment..."
	@$(VENV_BIN)/$(PIP) install crewai langchain langchain-openai
	@$(VENV_BIN)/$(PIP) install pyautogen open-interpreter
	@echo "Agentic environment setup complete"

# Run agentic platform
.PHONY: agentic-run
agentic-run: agentic-setup
	@echo "Starting CloudCurio Agentic Platform..."
	@$(VENV_BIN)/$(PYTHON) -c "
import os
import sys
sys.path.insert(0, '.')

from crewai import Crew, Agent, Task, Process
from langchain.tools import tool

# Example agentic workflow
@tool('example_tool')
def example_tool(query: str) -> str:
    return f'Processed: {query}'

example_agent = Agent(
    role='Example Agent',
    goal='Process user requests',
    backstory='An AI agent designed to help with CloudCurio tasks',
    tools=[example_tool]
)

example_task = Task(
    description='Process this request: {request}',
    agent=example_agent,
    expected_output='Processed result'
)

print('Agentic platform ready. Example agent created.')
print('To run a crew: Use the MCP server API or CrewAI directly')
"
	@echo "Agentic platform started"

# Run feature tracking demo
.PHONY: demo-tracking
demo-tracking: setup
	@echo "Running CloudCurio Feature Tracking Demo..."
	@$(VENV_BIN)/$(PYTHON) demo_feature_tracking.py
	@echo "Feature tracking demo completed"

# Run AI code review demo
.PHONY: demo-ai-review
demo-ai-review: setup
	@echo "Running CloudCurio AI Code Review Demo..."
	@$(VENV_BIN)/$(PYTHON) scripts/ai_code_review.py --file demo_feature_tracking.py
	@echo "AI code review demo completed"

# Install script
.PHONY: install-script
install-script:
	@echo '#!/bin/bash' > scripts/installers/install.sh
	@echo 'echo "Installing CloudCurio..."' >> scripts/installers/install.sh
	@echo 'python3 -m venv cloudcurio_env' >> scripts/installers/install.sh
	@echo 'source cloudcurio_env/bin/activate' >> scripts/installers/install.sh
	@echo 'pip install -r crew/requirements.txt' >> scripts/installers/install.sh
	@echo 'echo "CloudCurio installation complete"' >> scripts/installers/install.sh
	@chmod +x scripts/installers/install.sh
	@echo "Install script created"

# All-in-one setup
.PHONY: all
all: setup build docs install-script
	@echo "CloudCurio platform fully set up!"