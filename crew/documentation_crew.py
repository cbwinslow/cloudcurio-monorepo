import os
from crewai import Agent, Task, Crew, Process
from langchain.tools import tool
from .config.crew_config_manager import config_manager
from ..ai_tools.ai_provider import ai_manager, CredentialManager
from ..ai_tools.config_manager import global_config_manager


# Initialize the LLM through the AI provider manager
try:
    # Get the configured provider
    provider_name = global_config_manager.get_default_provider()
    default_model = global_config_manager.get_default_model(provider_name)
    
    # For now, we'll still use the LangChain-compatible OpenAI interface for CrewAI compatibility
    # In a full implementation, we'd need to create LangChain-compatible wrappers for our providers
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="gpt-4")  # Fallback to ensure compatibility with CrewAI
except:
    # Fallback to ensure compatibility with CrewAI
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="gpt-4")

# Define custom tools for the documentation crew
@tool("list_files")
def list_files(directory: str) -> str:
    """List all files in a directory"""
    try:
        files = os.listdir(directory)
        return f"Files in {directory}: {', '.join(files)}"
    except Exception as e:
        return f"Error listing files: {str(e)}"

@tool("read_file")
def read_file(file_path: str) -> str:
    """Read the contents of a file"""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

@tool("search_codebase")
def search_codebase(terms: str) -> str:
    """Search the codebase for specific terms or patterns"""
    import subprocess
    try:
        # This is a simplified search - in a real implementation, you'd want more sophisticated search
        result = subprocess.run(
            ["grep", "-r", "-n", "--include=*.py", "--include=*.ts", "--include=*.tsx", 
             "--include=*.js", "--include=*.json", "--include=*.md", terms, "."],
            capture_output=True, text=True, timeout=30
        )
        return result.stdout if result.stdout else f"No results found for: {terms}"
    except subprocess.TimeoutExpired:
        return "Search timed out"
    except Exception as e:
        return f"Error searching codebase: {str(e)}"


def create_documentation_crew():
    """Create the documentation crew based on the configuration"""
    config = config_manager.get_config("documentation_crew")
    
    if not config:
        raise ValueError("Documentation crew configuration not found")
    
    # Create agents based on configuration
    agents_config = config["agents"]
    agents = {}
    
    for agent_config in agents_config:
        agent_name = agent_config["name"]
        
        if agent_name == "code_explorer":
            agent = Agent(
                role=agent_config["role"],
                goal=agent_config["goal"],
                backstory=agent_config["backstory"],
                verbose=True,
                allow_delegation=False,
                llm=llm,
                tools=[list_files, read_file, search_codebase]
            )
        elif agent_name == "tech_writer":
            agent = Agent(
                role=agent_config["role"],
                goal=agent_config["goal"],
                backstory=agent_config["backstory"],
                verbose=True,
                allow_delegation=False,
                llm=llm
            )
        elif agent_name == "content_reviewer":
            agent = Agent(
                role=agent_config["role"],
                goal=agent_config["goal"],
                backstory=agent_config["backstory"],
                verbose=True,
                allow_delegation=False,
                llm=llm
            )
        else:
            # Default agent creation for any other agents
            agent = Agent(
                role=agent_config["role"],
                goal=agent_config["goal"],
                backstory=agent_config["backstory"],
                verbose=True,
                allow_delegation=False,
                llm=llm
            )
        
        agents[agent_name] = agent
    
    # Create tasks based on configuration
    tasks_config = config["tasks"]
    tasks = []
    
    for task_config in tasks_config:
        task_name = task_config["name"]
        
        # Map task to the appropriate agent
        if task_name == "code_mapping_task":
            agent = agents["code_explorer"]
        elif task_name == "documentation_creation_task":
            agent = agents["tech_writer"]
        elif task_name == "quality_assurance_task":
            agent = agents["content_reviewer"]
        else:
            # Default to the first agent if not specifically mapped
            agent = list(agents.values())[0]
        
        task = Task(
            description=task_config["description"],
            agent=agent,
            expected_output=task_config["expected_output"]
        )
        
        # Add context if specified
        if "context" in task_config:
            # For now, we'll add a simple note about context
            # In a real implementation, you'd link tasks properly
            task.description += f"\n\nContext from previous tasks: {task_config['context']}"
        
        tasks.append(task)
    
    # Create the crew
    documentation_crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,  # Execute tasks in sequence as configured
        verbose=config["verbose"]
    )
    
    return documentation_crew


# For testing the documentation crew independently
if __name__ == "__main__":
    print("Creating documentation crew...")
    doc_crew = create_documentation_crew()
    
    print("Starting documentation crew process...")
    result = doc_crew.kickoff()
    
    print("Documentation crew completed.")
    print("Result:", result)