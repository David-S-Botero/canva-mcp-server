"""
User tools for Canva MCP Server
"""

import time
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP

from ..services.user_service import UserService
from ..types.canva_types import CanvaConfig
from ..utils.logging import log_tool_execution

# Import the global config from auth_tools
from .auth_tools import canva_config

user_service = UserService(canva_config)

async def get_current_user(mcp: FastMCP) -> Dict[str, Any]:
    """
    Get details of the current authenticated user.
    
    Returns:
        User information
    """
    start_time = time.time()
    try:
        result = await user_service.get_current_user()
        duration = time.time() - start_time
        log_tool_execution("get_current_user", True, duration)
        return {
            "id": result.id,
            "display_name": result.display_name,
            "email": result.email,
            "team_id": result.team_id,
            "created_at": result.created_at.isoformat()
        }
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("get_current_user", False, duration, str(e))
        raise

async def get_user_profile(mcp: FastMCP) -> Dict[str, Any]:
    """
    Get the profile information of the current user.
    
    Returns:
        User profile information
    """
    start_time = time.time()
    try:
        result = await user_service.get_user_profile()
        duration = time.time() - start_time
        log_tool_execution("get_user_profile", True, duration)
        return result
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("get_user_profile", False, duration, str(e))
        raise

async def get_user_capabilities(mcp: FastMCP) -> Dict[str, Any]:
    """
    Get the API capabilities for the user account.
    
    Returns:
        User capabilities information
    """
    start_time = time.time()
    try:
        result = await user_service.get_user_capabilities()
        duration = time.time() - start_time
        log_tool_execution("get_user_capabilities", True, duration)
        return result
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("get_user_capabilities", False, duration, str(e))
        raise 