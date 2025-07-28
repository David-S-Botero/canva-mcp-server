"""
Configuration utilities for Canva MCP Server
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the Canva MCP Server"""
    
    # Canva API Configuration
    CANVA_CLIENT_ID: str = os.getenv("CANVA_CLIENT_ID", "")
    CANVA_CLIENT_SECRET: str = os.getenv("CANVA_CLIENT_SECRET", "")
    CANVA_REDIRECT_URI: str = os.getenv("CANVA_REDIRECT_URI", "")
    
    # Server Configuration
    MCP_SERVER_HOST: str = os.getenv("MCP_SERVER_HOST", "localhost")
    MCP_SERVER_PORT: int = int(os.getenv("MCP_SERVER_PORT", "8000"))
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "canva_mcp_server.log")
    LOG_ERROR_FILE: str = os.getenv("LOG_ERROR_FILE", "canva_mcp_server_errors.log")
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that all required configuration is present"""
        required_vars = [
            "CANVA_CLIENT_ID",
            "CANVA_CLIENT_SECRET", 
            "CANVA_REDIRECT_URI"
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            print(f"Missing required environment variables: {', '.join(missing_vars)}")
            print("Please set these variables in your .env file")
            return False
        
        return True
    
    @classmethod
    def get_config_summary(cls) -> dict:
        """Get a summary of the current configuration"""
        return {
            "client_id_configured": bool(cls.CANVA_CLIENT_ID),
            "client_secret_configured": bool(cls.CANVA_CLIENT_SECRET),
            "redirect_uri_configured": bool(cls.CANVA_REDIRECT_URI),
            "server_host": cls.MCP_SERVER_HOST,
            "server_port": cls.MCP_SERVER_PORT,
            "log_level": cls.LOG_LEVEL
        }