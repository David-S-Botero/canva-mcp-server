"""
Utility tools for Canva MCP Server
"""

import time
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP

from ..utils.logging import log_tool_execution, log_server_startup, log_server_shutdown

def get_server_info(mcp: FastMCP) -> Dict[str, Any]:
    """
    Get server information and status.
    
    Returns:
        Server information
    """
    start_time = time.time()
    try:
        result = {
            "name": "Canva MCP Server",
            "version": "1.0.0",
            "status": "running",
            "features": [
                "Authentication (OAuth 2.0)",
                "User Management",
                "Design Management",
                "Asset Management",
                "Folder Management",
                "Export Operations",
                "Brand Templates",
                "Autofill Operations",
                "Comment Management"
            ]
        }
        duration = time.time() - start_time
        log_tool_execution("get_server_info", True, duration)
        return result
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("get_server_info", False, duration, str(e))
        raise

def ping_server(mcp: FastMCP) -> Dict[str, str]:
    """
    Ping the server to check if it's running.
    
    Returns:
        Ping response
    """
    start_time = time.time()
    try:
        result = {"message": "pong", "timestamp": time.time()}
        duration = time.time() - start_time
        log_tool_execution("ping_server", True, duration)
        return result
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("ping_server", False, duration, str(e))
        raise 