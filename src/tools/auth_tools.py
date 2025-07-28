"""
Authentication tools for Canva MCP Server
"""

import time
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP

from ..services.auth_service import AuthService
from ..types.canva_types import CanvaConfig
from ..utils.logging import log_tool_execution, logger

# Global configuration (in production, this should be stored securely)
canva_config = CanvaConfig(
    client_id="",  # Will be loaded from environment
    client_secret="",  # Will be loaded from environment
    redirect_uri=""  # Will be loaded from environment
)

auth_service = AuthService(canva_config)

def create_authorization_url(mcp: FastMCP, scopes: str = None) -> Dict[str, str]:
    """
    Create an OAuth authorization URL for Canva API access.
    
    Args:
        scopes: Space-separated list of scopes to request
        
    Returns:
        Dictionary containing authorization URL and code verifier
    """
    start_time = time.time()
    try:
        result = auth_service.create_authorization_url(scopes)
        duration = time.time() - start_time
        log_tool_execution("create_authorization_url", True, duration)
        return result
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("create_authorization_url", False, duration, str(e))
        raise

async def exchange_code_for_token(mcp: FastMCP, authorization_code: str, code_verifier: str) -> Dict[str, Any]:
    """
    Exchange authorization code for access token.
    
    Args:
        authorization_code: The authorization code received from Canva
        code_verifier: The code verifier used in the authorization request
        
    Returns:
        Token response with access_token, refresh_token, and expiry
    """
    start_time = time.time()
    try:
        result = await auth_service.exchange_code_for_token(authorization_code, code_verifier)
        duration = time.time() - start_time
        log_tool_execution("exchange_code_for_token", True, duration)
        return {
            "access_token": result.access_token,
            "token_type": result.token_type,
            "expires_in": result.expires_in,
            "scope": result.scope,
            "refresh_token": result.refresh_token
        }
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("exchange_code_for_token", False, duration, str(e))
        raise

async def refresh_access_token(mcp: FastMCP) -> Dict[str, Any]:
    """
    Refresh the access token using the refresh token.
    
    Returns:
        New token response
    """
    start_time = time.time()
    try:
        result = await auth_service.refresh_access_token()
        duration = time.time() - start_time
        log_tool_execution("refresh_access_token", True, duration)
        return {
            "access_token": result.access_token,
            "token_type": result.token_type,
            "expires_in": result.expires_in,
            "scope": result.scope,
            "refresh_token": result.refresh_token
        }
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("refresh_access_token", False, duration, str(e))
        raise

def get_oauth_config(mcp: FastMCP) -> Dict[str, str]:
    """
    Get the current OAuth configuration.
    
    Returns:
        Current OAuth configuration
    """
    start_time = time.time()
    try:
        result = {
            "client_id": canva_config.client_id,
            "redirect_uri": canva_config.redirect_uri,
            "has_access_token": bool(canva_config.access_token),
            "has_refresh_token": bool(canva_config.refresh_token),
            "token_expires_at": canva_config.token_expires_at.isoformat() if canva_config.token_expires_at else None
        }
        duration = time.time() - start_time
        log_tool_execution("get_oauth_config", True, duration)
        return result
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("get_oauth_config", False, duration, str(e))
        raise

def clear_tokens(mcp: FastMCP) -> Dict[str, str]:
    """
    Clear stored access and refresh tokens.
    
    Returns:
        Confirmation message
    """
    start_time = time.time()
    try:
        auth_service.clear_tokens()
        duration = time.time() - start_time
        log_tool_execution("clear_tokens", True, duration)
        return {"message": "Tokens cleared successfully"}
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("clear_tokens", False, duration, str(e))
        raise 