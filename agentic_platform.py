"""
CloudCurio Agentic Environment
Advanced multi-agent platform for AI-driven development tasks
"""

import os
import sys
import json
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

from crewai import Crew, Agent, Task, Process
from langchain.tools import tool
from langchain_openai import ChatOpenAI

from ai_tools.ai_provider import ai_manager
from ai_tools.config_manager import global_config_manager
from crew.config.crew_config_manager import config_manager as crew_config_manager
from sysmon.sysmon import SysMon


@dataclass
class AgenticTask:
    """Represents a task for the agentic system"""
    id: str
    name: str
    description: str
    assigned_agent: str
    priority: str  # low, medium, high, critical
    status: str  # pending, running, completed, failed
    created_at: datetime
    completed_at: Optional[datetime] = None
    result: Optional[str] = None
    error: Optional[str] = None


class CloudCurioAgenticPlatform:
    """Main class for the CloudCurio Agentic Platform"""
    
    def __init__(self):
        self.agents = {}
        self.tasks = {}
        self.crews = {}
        self.sysmon = SysMon()
        self.active_sessions = []
        
        # Initialize with default agents
        self._initialize_default_agents()
    
    def _initialize_default_agents(self):
        """Initialize default agents for the platform"""
        # Code Analyst Agent
        self.agents["code_analyst"] = Agent(
            role="Code Analyst",
            goal="Analyze codebases to understand structure, components, and functionality",
            backstory="You are an expert software engineer with extensive experience in code analysis. "
                     "Your task is to examine codebases in detail, identifying key components, "
                     "understanding how they interact, and documenting the overall architecture.",
            verbose=True,
            allow_delegation=False,
            llm=ChatOpenAI(model="gpt-4")
        )
        
        # Documentation Specialist Agent
        self.agents["documentation_specialist"] = Agent(
            role="Documentation Specialist",
            goal="Create comprehensive documentation and procedures based on codebase analysis",
            backstory="You are a technical writer with deep expertise in creating developer documentation. "
                     "Your task is to transform code analysis into clear, comprehensive documentation "
                     "and standard operating procedures that will help developers understand "
                     "and work with systems.",
            verbose=True,
            allow_delegation=False,
            llm=ChatOpenAI(model="gpt-4")
        )
        
        # QA Engineer Agent
        self.agents["qa_engineer"] = Agent(
            role="QA Engineer",
            goal="Review generated documentation for accuracy and completeness",
            backstory="You are a quality assurance engineer with experience in both code review "
                     "and technical documentation. Your task is to ensure that all generated "
                     "documentation accurately reflects the codebase and that procedures "
                     "are complete and actionable.",
            verbose=True,
            allow_delegation=False,
            llm=ChatOpenAI(model="gpt-4")
        )
        
        # System Monitor Agent
        self.agents["sys_monitor"] = Agent(
            role="System Monitor",
            goal="Monitor system changes and configuration updates",
            backstory="You are a system monitoring expert that tracks changes to the system "
                     "including package installations, service modifications, and configuration updates. "
                     "Your task is to maintain an accurate view of the system state.",
            verbose=True,
            allow_delegation=False,
            llm=ChatOpenAI(model="gpt-4")
        )
    
    def create_custom_agent(self, name: str, role: str, goal: str, backstory: str, 
                           llm_provider: str = "openrouter", model: str = "mistralai/mistral-7b-instruct"):
        """Create a custom agent with specified parameters"""
        llm = ChatOpenAI(model=model)
        
        agent = Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            verbose=True,
            allow_delegation=False,
            llm=llm
        )
        
        self.agents[name] = agent
        return agent
    
    def create_crew_from_config(self, crew_type: str):
        """Create a crew based on configuration"""
        config = crew_config_manager.get_config(crew_type)
        if not config:
            raise ValueError(f"Crew configuration '{crew_type}' not found")
        
        # Map agent names to actual agent objects
        crew_agents = []
        for agent_config in config["agents"]:
            agent_name = agent_config["name"]
            if agent_name in self.agents:
                crew_agents.append(self.agents[agent_name])
        
        # Create tasks
        crew_tasks = []
        for task_config in config["tasks"]:
            task = Task(
                description=task_config["description"],
                agent=self.agents[task_config["agent"]] if "agent" in task_config else crew_agents[0],
                expected_output=task_config["expected_output"]
            )
            crew_tasks.append(task)
        
        # Create and store the crew
        crew = Crew(
            agents=crew_agents,
            tasks=crew_tasks,
            process=Process[config["process"].upper()] if config["process"].upper() in Process.__members__ else Process.sequential,
            verbose=config.get("verbose", 2)
        )
        
        crew_id = f"{crew_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.crews[crew_id] = crew
        
        return crew_id, crew
    
    def create_agentic_task(self, name: str, description: str, agent_name: str, priority: str = "medium"):
        """Create a new task for the agentic system"""
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        task = AgenticTask(
            id=task_id,
            name=name,
            description=description,
            assigned_agent=agent_name,
            priority=priority,
            status="pending",
            created_at=datetime.now()
        )
        
        self.tasks[task_id] = task
        return task_id
    
    async def execute_task(self, task_id: str):
        """Execute a specific task"""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        
        task = self.tasks[task_id]
        
        try:
            task.status = "running"
            
            # Get the assigned agent
            if task.assigned_agent not in self.agents:
                raise ValueError(f"Agent {task.assigned_agent} not found")
            
            agent = self.agents[task.assigned_agent]
            
            # Create a simple task for the agent
            simple_task = Task(
                description=task.description,
                agent=agent,
                expected_output="Result of the task execution"
            )
            
            # Execute the task (in a real implementation, this would be more complex)
            result = simple_task.execute_sync()  # This is a simplified execution
            
            task.status = "completed"
            task.completed_at = datetime.now()
            task.result = result
            
        except Exception as e:
            task.status = "failed"
            task.completed_at = datetime.now()
            task.error = str(e)
        
        return task
    
    def list_agents(self) -> List[str]:
        """List all available agents"""
        return list(self.agents.keys())
    
    def list_crews(self) -> List[str]:
        """List all available crews"""
        return list(self.crews.keys())
    
    def list_tasks(self) -> List[AgenticTask]:
        """List all tasks"""
        return list(self.tasks.values())
    
    def run_crew(self, crew_id: str):
        """Run a specific crew"""
        if crew_id not in self.crews:
            raise ValueError(f"Crew {crew_id} not found")
        
        crew = self.crews[crew_id]
        result = crew.kickoff()
        
        return result
    
    def create_custom_crew(self, name: str, agents: List[str], tasks: List[Dict]):
        """Create a custom crew from provided agents and tasks"""
        crew_agents = [self.agents[agent_name] for agent_name in agents if agent_name in self.agents]
        
        crew_tasks = []
        for task_config in tasks:
            agent_name = task_config.get("agent", agents[0] if agents else None)
            agent = self.agents[agent_name] if agent_name in self.agents else None
            
            task = Task(
                description=task_config["description"],
                agent=agent,
                expected_output=task_config.get("expected_output", "Result of the task")
            )
            crew_tasks.append(task)
        
        crew = Crew(
            agents=crew_agents,
            tasks=crew_tasks,
            process=Process.sequential,  # Default, can be configured
            verbose=2
        )
        
        crew_id = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.crews[crew_id] = crew
        
        return crew_id, crew


class AgenticCLI:
    """Command Line Interface for the Agentic Platform"""
    
    def __init__(self):
        self.platform = CloudCurioAgenticPlatform()
    
    def run(self):
        """Run the CLI interface"""
        print("CloudCurio Agentic Platform")
        print("=========================")
        
        while True:
            print("\nAvailable commands:")
            print("1. list-agents - List all available agents")
            print("2. list-crews - List all available crews")
            print("3. create-crew <crew_type> - Create a crew from configuration")
            print("4. run-crew <crew_id> - Run a specific crew")
            print("5. create-task <name> <description> <agent> - Create a new task")
            print("6. list-tasks - List all tasks")
            print("7. execute-task <task_id> - Execute a specific task")
            print("8. create-agent <name> <role> <goal> <backstory> - Create a custom agent")
            print("9. exit - Exit the platform")
            
            command = input("\nEnter command: ").strip().split()
            
            if not command:
                continue
                
            cmd = command[0].lower()
            
            if cmd == "list-agents":
                agents = self.platform.list_agents()
                print(f"Available agents: {', '.join(agents)}")
                
            elif cmd == "list-crews":
                crews = self.platform.list_crews()
                print(f"Available crews: {', '.join(crews)}")
                
            elif cmd == "create-crew" and len(command) > 1:
                try:
                    crew_id, crew = self.platform.create_crew_from_config(command[1])
                    print(f"Created crew: {crew_id}")
                except Exception as e:
                    print(f"Error creating crew: {e}")
                    
            elif cmd == "run-crew" and len(command) > 1:
                try:
                    result = self.platform.run_crew(command[1])
                    print(f"Crew result: {result}")
                except Exception as e:
                    print(f"Error running crew: {e}")
                    
            elif cmd == "create-task" and len(command) > 3:
                task_id = self.platform.create_agentic_task(
                    command[1],  # name
                    " ".join(command[2:-1]),  # description (everything except last element)
                    command[-1],  # agent
                )
                print(f"Created task: {task_id}")
                
            elif cmd == "list-tasks":
                tasks = self.platform.list_tasks()
                for task in tasks:
                    print(f"  {task.id}: {task.name} ({task.status}) - {task.assigned_agent}")
                    
            elif cmd == "execute-task" and len(command) > 1:
                try:
                    task = asyncio.run(self.platform.execute_task(command[1]))
                    print(f"Task {task.id} completed with status: {task.status}")
                    if task.result:
                        print(f"Result: {task.result[:200]}...")  # Truncate long results
                except Exception as e:
                    print(f"Error executing task: {e}")
                    
            elif cmd == "create-agent" and len(command) > 4:
                try:
                    agent = self.platform.create_custom_agent(
                        command[1],  # name
                        command[2],  # role
                        " ".join(command[3:-1]),  # goal (everything except last element)
                        command[-1]  # backstory
                    )
                    print(f"Created agent: {command[1]}")
                except Exception as e:
                    print(f"Error creating agent: {e}")
                    
            elif cmd == "exit" or cmd == "quit":
                print("Exiting CloudCurio Agentic Platform...")
                break
                
            else:
                print("Invalid command or insufficient arguments")


# Example advanced agent with local AI support
class LocalAIAgent:
    """Agent that can utilize local AI models via Ollama"""
    
    def __init__(self, model: str = "llama3"):
        self.model = model
        self.api_base = "http://localhost:11434/api/generate"
    
    def generate(self, prompt: str) -> str:
        """Generate response using local AI"""
        try:
            import requests
            response = requests.post(self.api_base, json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            })
            return response.json()["response"]
        except:
            # Fallback to API-based model
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(model="gpt-3.5-turbo")
            return llm.invoke(prompt).content


def main():
    """Main entry point for the agentic platform"""
    cli = AgenticCLI()
    cli.run()


if __name__ == "__main__":
    main()