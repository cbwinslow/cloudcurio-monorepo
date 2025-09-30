from crewai import Task
from .agents import code_analyst, documentation_specialist, qa_engineer

# Define the tasks
code_analysis_task = Task(
    description="""Analyze the CloudCurio codebase to understand its structure and components.
    
    The codebase is located at '../' relative to your current directory.
    
    Your analysis should cover:
    1. Overall architecture and main components
    2. Key directories and their purposes
    3. Important files and their functions
    4. Data models and database schema
    5. API endpoints and their functionality
    6. Worker processes and how they function
    7. Configuration and environment variables
    8. Dependencies and external services
    
    Use the list_files and read_file tools to explore the codebase as needed.
    Focus on understanding how all components work together to deliver the CloudCurio service.""",
    agent=code_analyst,
    expected_output="A comprehensive analysis of the CloudCurio codebase structure and components."
)

documentation_task = Task(
    description="""Create comprehensive documentation and procedures based on the code analysis.
    
    Create the following documentation files in the '../docs/' directory:
    1. ARCHITECTURE.md - Overall system architecture and component interactions
    2. COMPONENTS.md - Detailed documentation for each major component
    3. API.md - API endpoints documentation (if not already comprehensive)
    4. DEVELOPMENT.md - Developer setup and contribution guidelines
    5. DEPLOYMENT.md - Deployment procedures and requirements
    6. WORKER.md - Documentation for the review worker system
    7. ENVIRONMENT.md - Environment variables and configuration
    8. TESTING.md - Testing procedures and guidelines
    
    Each document should be comprehensive and clearly written, targeting developers 
    who need to understand, modify, or extend the CloudCurio platform.""",
    agent=documentation_specialist,
    expected_output="Comprehensive documentation files covering all aspects of the CloudCurio platform.",
    context=[code_analysis_task]
)

qa_review_task = Task(
    description="""Review the generated documentation for accuracy and completeness.
    
    Verify that:
    1. All documentation accurately reflects the codebase
    2. Procedures are complete and actionable
    3. Technical details are correct
    4. Documentation covers all major components and processes
    5. There are no gaps or missing information
    
    If you find any issues, provide specific feedback on what needs to be corrected or improved.""",
    agent=qa_engineer,
    expected_output="A review of the documentation with feedback on accuracy and completeness.",
    context=[code_analysis_task, documentation_task]
)