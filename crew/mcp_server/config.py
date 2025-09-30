import os
from typing import Optional

class MCPConfig:
    """Configuration for the MCP server"""
    
    # Server configuration
    HOST: str = os.getenv("MCP_HOST", "0.0.0.0")
    PORT: int = int(os.getenv("MCP_PORT", "8000"))
    DEBUG: bool = os.getenv("MCP_DEBUG", "False").lower() == "true"
    
    # Database configuration (for crew results logging)
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    SUPABASE_URL: Optional[str] = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: Optional[str] = os.getenv("SUPABASE_KEY")
    
    # AI model configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "gpt-4")
    
    # Crew configuration
    DEFAULT_CREW_TIMEOUT: int = int(os.getenv("DEFAULT_CREW_TIMEOUT", "3600"))  # 1 hour
    MAX_CONCURRENT_CREWS: int = int(os.getenv("MAX_CONCURRENT_CREWS", "5"))
    
    # Logging configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"