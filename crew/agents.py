import os
from crewai import Agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool

# Initialize the LLM
# Note: You'll need to set OPENAI_API_KEY in your environment variables
llm = ChatOpenAI(model="gpt-4")

# Define custom tools for the agents
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

# Create the agents
code_analyst = Agent(
    role="Code Analyst",
    goal="Analyze the CloudCurio codebase to understand its structure, components, and functionality",
    backstory="""You are an expert software engineer with extensive experience in code analysis. 
    Your task is to examine the CloudCurio codebase in detail, identifying key components, 
    understanding how they interact, and documenting the overall architecture.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[list_files, read_file]
)

documentation_specialist = Agent(
    role="Documentation Specialist",
    goal="Create comprehensive documentation and procedures based on the codebase analysis",
    backstory="""You are a technical writer with deep expertise in creating developer documentation. 
    Your task is to transform the code analysis into clear, comprehensive documentation and standard 
    operating procedures that will help developers understand and work with the CloudCurio platform.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

qa_engineer = Agent(
    role="QA Engineer",
    goal="Review the generated documentation for accuracy and completeness",
    backstory="""You are a quality assurance engineer with experience in both code review and 
    technical documentation. Your task is to ensure that all generated documentation accurately 
    reflects the codebase and that procedures are complete and actionable.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)