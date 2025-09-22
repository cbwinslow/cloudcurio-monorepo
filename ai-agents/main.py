#!/usr/bin/env python3

import sys
import os
from dotenv import load_dotenv
from agents.base import AgentManager
from agents.impl import DataCollectorAgent, AnalyzerAgent, ReporterAgent, AlerterAgent
from agents.dashboard_agent import DashboardAgent

def main():
    """Main entry point for the AI agents system"""
    
    # Load environment variables
    load_dotenv()
    
    # Add the current directory to the Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Initialize the agent manager
    agent_manager = AgentManager()
    
    # Register specific agent implementations
    # In a real implementation, we would dynamically register agents
    # based on the configuration file
    
    print("OSINT AI Agents System")
    print("=" * 30)
    print(f"Available agents: {', '.join(agent_manager.list_agents())}")
    print()
    
    # Example usage
    print("Example: Running data collector agent")
    try:
        result = agent_manager.run_agent("data_collector", "Collect information about cybersecurity threats")
        print(result)
    except Exception as e:
        print(f"Error running agent: {e}")
    
    print()
    print("Example: Running analyzer agent")
    try:
        result = agent_manager.run_agent("analyzer", "Analyze collected cybersecurity threat data")
        print(result)
    except Exception as e:
        print(f"Error running agent: {e}")
    
    print()
    print("Example: Running dashboard agent")
    try:
        result = agent_manager.run_agent("dashboard", "Create an OSINT dashboard")
        print(result)
    except Exception as e:
        print(f"Error running agent: {e}")

if __name__ == "__main__":
    main()