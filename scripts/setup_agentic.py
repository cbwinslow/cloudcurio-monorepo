#!/usr/bin/env python3
"""
CloudCurio Agentic Environment Setup

This script sets up the complete agentic environment with multiple AI agents,
crew configuration, and local AI support.
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path
from typing import Dict, List, Optional


def run_command(cmd: str, shell=True, cwd=None, capture_output=True):
    """Run a shell command and return the result"""
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(
            cmd, 
            shell=shell, 
            cwd=cwd, 
            capture_output=capture_output, 
            text=True
        )
        if result.returncode != 0:
            print(f"Command failed: {cmd}")
            print(f"Error: {result.stderr}")
            return False, result.stderr
        print(f"Success: {result.stdout[:500]}...")  # Limit output
        return True, result.stdout
    except Exception as e:
        print(f"Exception running command: {e}")
        return False, str(e)


def setup_python_env():
    """Setup Python virtual environment and install dependencies"""
    print("Setting up Python environment...")
    
    # Create virtual environment if it doesn't exist
    venv_path = Path("agentic_env")
    if not venv_path.exists():
        success, output = run_command(f"python3 -m venv {venv_path}")
        if not success:
            return False
    
    # Install dependencies
    pip_path = venv_path / "bin" / "pip" if os.name != "nt" else venv_path / "Scripts" / "pip.exe"
    requirements = [
        "crewai>=0.11.0",
        "langchain>=0.0.300",
        "langchain-openai>=0.0.2",
        "openai>=1.3.5",
        "pyautogen>=0.2.0",
        "flaml>=2.1.0",
        "sentence-transformers>=2.2.2",
        "scikit-learn>=1.3.0",
        "numpy>=1.24.0",
        "requests>=2.31.0",
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "pydantic>=2.5.0",
        "sqlalchemy>=2.0.23",
        "psycopg2-binary>=2.9.9",
        "supabase>=1.0.4",
        "python-multipart>=0.0.6",
        "python-dotenv>=1.0.0",
        "pyppeteer>=1.0.2",
        "ollama>=0.1.0"
    ]
    
    for req in requirements:
        success, output = run_command(f"{pip_path} install {req}")
        if not success:
            print(f"Failed to install {req}, continuing...")
    
    return True


def setup_local_ai():
    """Setup local AI models using Ollama"""
    print("Setting up local AI with Ollama...")
    
    # Check if Ollama is installed
    success, output = run_command("ollama --version")
    if not success:
        print("Ollama is not installed. Please install Ollama first.")
        print("Visit: https://github.com/jmorganca/ollama")
        return False
    
    # Pull required models
    models_to_pull = ["llama3", "mistral", "phi3"]
    
    for model in models_to_pull:
        print(f"Pulling {model} model...")
        success, output = run_command(f"ollama pull {model}")
        if not success:
            print(f"Failed to pull {model}, but continuing...")
    
    return True


def create_agent_configurations():
    """Create configuration files for different types of agents"""
    print("Creating agent configurations...")
    
    config_dir = Path("agentic_configs")
    config_dir.mkdir(exist_ok=True)
    
    # Example agent configurations
    agent_configs = {
        "code_analyst": {
            "role": "Code Analyst",
            "goal": "Analyze codebases to understand structure, components, and functionality",
            "backstory": "Expert software engineer with extensive experience in code analysis",
            "tools": ["list_files", "read_file", "search_codebase"],
            "max_iter": 15,
            "max_rpm": 100
        },
        "documentation_specialist": {
            "role": "Documentation Specialist",
            "goal": "Create comprehensive documentation from codebase analysis",
            "backstory": "Technical writer with deep expertise in creating developer documentation",
            "tools": [],
            "max_iter": 15,
            "max_rpm": 100
        },
        "qa_engineer": {
            "role": "QA Engineer",
            "goal": "Review documentation for accuracy and completeness",
            "backstory": "Quality assurance engineer with experience in code review and documentation",
            "tools": [],
            "max_iter": 15,
            "max_rpm": 100
        },
        "sys_monitor": {
            "role": "System Monitor",
            "goal": "Monitor system changes and configuration updates",
            "backstory": "System monitoring expert tracking changes to packages, services, and configurations",
            "tools": ["system_info", "package_checker"],
            "max_iter": 15,
            "max_rpm": 100
        }
    }
    
    for agent_name, config in agent_configs.items():
        config_path = config_dir / f"{agent_name}.json"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"Created configuration for {agent_name}")
    
    return True


def create_crew_configurations():
    """Create configuration files for different types of crews"""
    print("Creating crew configurations...")
    
    config_dir = Path("agentic_configs")
    
    # Example crew configurations
    crew_configs = {
        "code_review_crew": {
            "name": "Code Review Crew",
            "description": "Reviews codebases and generates documentation",
            "agents": ["code_analyst", "documentation_specialist", "qa_engineer"],
            "tasks": [
                {
                    "name": "code_analysis",
                    "description": "Analyze the codebase structure and components",
                    "expected_output": "Detailed analysis of the codebase",
                    "agent": "code_analyst"
                },
                {
                    "name": "documentation_creation",
                    "description": "Create comprehensive documentation based on code analysis",
                    "expected_output": "Complete documentation files",
                    "agent": "documentation_specialist",
                    "context": ["code_analysis"]
                },
                {
                    "name": "quality_assurance",
                    "description": "Review the created documentation for accuracy",
                    "expected_output": "Review with feedback",
                    "agent": "qa_engineer",
                    "context": ["code_analysis", "documentation_creation"]
                }
            ],
            "process": "sequential",
            "verbose": 2
        },
        "system_monitoring_crew": {
            "name": "System Monitoring Crew",
            "description": "Monitors system changes and maintains configuration snapshots",
            "agents": ["sys_monitor"],
            "tasks": [
                {
                    "name": "config_tracking",
                    "description": "Track system configuration changes",
                    "expected_output": "Configuration change log",
                    "agent": "sys_monitor"
                }
            ],
            "process": "sequential",
            "verbose": 2
        }
    }
    
    for crew_name, config in crew_configs.items():
        config_path = config_dir / f"{crew_name}.json"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"Created configuration for {crew_name}")
    
    return True


def setup_agentic_platform():
    """Setup the complete agentic platform"""
    print("Setting up CloudCurio Agentic Platform...")
    
    # Setup Python environment
    if not setup_python_env():
        print("Failed to setup Python environment")
        return False
    
    # Setup local AI if available
    if not setup_local_ai():
        print("Local AI setup failed, but continuing...")
    
    # Create agent configurations
    if not create_agent_configurations():
        print("Failed to create agent configurations")
        return False
    
    # Create crew configurations
    if not create_crew_configurations():
        print("Failed to create crew configurations")
        return False
    
    print("Agentic platform setup completed successfully!")
    
    # Create a simple test to verify the setup
    test_script = """
import sys
import os
sys.path.insert(0, '.')

print("Testing agentic platform setup...")

try:
    from crewai import Agent, Task, Crew, Process
    print("✓ CrewAI imported successfully")
    
    from langchain.tools import tool
    print("✓ LangChain tools imported successfully")
    
    # Try to import Ollama if available
    try:
        import ollama
        print("✓ Ollama client available")
    except ImportError:
        print("⚠ Ollama client not available")
    
    # Try to create a simple agent
    @tool("test_tool")
    def test_tool(query: str) -> str:
        return f"Processed: {query}"
    
    test_agent = Agent(
        role='Test Agent',
        goal='Test the agentic environment',
        backstory='A simple test agent',
        tools=[test_tool]
    )
    
    print("✓ Test agent created successfully")
    
    print("Agentic platform setup verification: PASSED")
    
except Exception as e:
    print(f"Agentic platform setup verification: FAILED - {e}")
    sys.exit(1)
"""
    
    # Write the test to a file and run it
    with open("test_agentic_setup.py", "w") as f:
        f.write(test_script)
    
    success, output = run_command("python test_agentic_setup.py")
    
    # Clean up
    os.remove("test_agentic_setup.py")
    
    return success


def main():
    """Main entry point for the agentic setup"""
    print("CloudCurio Agentic Environment Setup")
    print("====================================")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        print("Running quick setup...")
        success = setup_local_ai()  # Only setup local AI if requested
        return 0 if success else 1
    
    success = setup_agentic_platform()
    if success:
        print("\\n🎉 CloudCurio Agentic Platform setup completed successfully!")
        print("\\nTo start using the platform:")
        print("- Activate the environment: source agentic_env/bin/activate")
        print("- Run the agentic platform: python agentic_platform.py")
        print("- Or use the CLI: python agentic_platform.py")
        return 0
    else:
        print("\\n❌ CloudCurio Agentic Platform setup failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())