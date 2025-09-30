import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from crew.mcp_server.config import MCPConfig
from crew.mcp_server.server import app
import uvicorn

def main():
    """Start the MCP server"""
    print(f"Starting CloudCurio MCP Server on {MCPConfig.HOST}:{MCPConfig.PORT}")
    print(f"Debug mode: {MCPConfig.DEBUG}")
    
    # Check if required environment variables are set
    if not MCPConfig.OPENAI_API_KEY:
        print("Warning: OPENAI_API_KEY is not set. Some features may not work properly.")
    
    uvicorn.run(
        app,
        host=MCPConfig.HOST,
        port=MCPConfig.PORT,
        reload=MCPConfig.DEBUG,
        log_level=MCPConfig.LOG_LEVEL.lower()
    )

if __name__ == "__main__":
    main()