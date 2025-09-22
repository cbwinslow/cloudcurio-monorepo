from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from abc import ABC, abstractmethod
import yaml
import os

class Tool(BaseModel):
    """Base class for tools that agents can use"""
    name: str
    description: str
    type: str
    config: Dict[str, Any] = {}
    
    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """Execute the tool with given parameters"""
        pass

class Agent(BaseModel):
    """Base class for AI agents"""
    name: str
    description: str
    enabled: bool = True
    tools: List[str] = []
    
    def __init__(self, **data):
        super().__init__(**data)
        self.tool_instances: Dict[str, Tool] = {}
    
    def register_tool(self, tool: Tool):
        """Register a tool with this agent"""
        self.tool_instances[tool.name] = tool
    
    def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """Execute a registered tool"""
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not registered with agent {self.name}")
        
        return self.tool_instances[tool_name].execute(**kwargs)
    
    @abstractmethod
    def run(self, task: str) -> str:
        """Run the agent with a specific task"""
        pass

class AgentManager:
    """Manager for loading and running agents"""
    
    def __init__(self, config_path: str = "config/agents.yaml"):
        self.config_path = config_path
        self.agents: Dict[str, Agent] = {}
        self.tools: Dict[str, Tool] = {}
        self.load_config()
    
    def load_config(self):
        """Load agent and tool configuration from YAML file"""
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Load tools
        for tool_name, tool_config in config.get('tools', {}).items():
            # In a real implementation, we would create specific tool instances
            # based on the tool type. For now, we'll create a generic tool.
            self.tools[tool_name] = Tool(
                name=tool_name,
                description=f"Tool for {tool_name}",
                type=tool_config.get('type', 'generic'),
                config=tool_config
            )
        
        # Load agents
        for agent_config in config.get('agents', []):
            agent = Agent(
                name=agent_config['name'],
                description=agent_config['description'],
                enabled=agent_config.get('enabled', True),
                tools=agent_config.get('tools', [])
            )
            
            # Register tools with the agent
            for tool_name in agent.tools:
                if tool_name in self.tools:
                    agent.register_tool(self.tools[tool_name])
            
            self.agents[agent.name] = agent
    
    def get_agent(self, name: str) -> Optional[Agent]:
        """Get an agent by name"""
        return self.agents.get(name)
    
    def list_agents(self) -> List[str]:
        """List all available agents"""
        return list(self.agents.keys())
    
    def run_agent(self, agent_name: str, task: str) -> str:
        """Run an agent with a specific task"""
        agent = self.get_agent(agent_name)
        if not agent:
            raise ValueError(f"Agent {agent_name} not found")
        
        if not agent.enabled:
            raise ValueError(f"Agent {agent_name} is disabled")
        
        return agent.run(task)