"""
Design tools for Canva MCP Server
"""

import time
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

from ..services.design_service import DesignService
from ..utils.logging import log_tool_execution

# Import the global config from auth_tools
from .auth_tools import canva_config

design_service = DesignService(canva_config)

async def create_design(
    mcp: FastMCP,
    title: str,
    brand_kit_id: Optional[str] = None,
    folder_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new Canva design.
    
    Args:
        title: Title for the new design
        brand_kit_id: Optional brand kit ID to use
        folder_id: Optional folder ID to place the design in
        
    Returns:
        Created design information
    """
    start_time = time.time()
    try:
        result = await design_service.create_design(title, brand_kit_id, folder_id)
        duration = time.time() - start_time
        log_tool_execution("create_design", True, duration)
        return {
            "id": result.id,
            "title": result.title,
            "created_at": result.created_at.isoformat(),
            "updated_at": result.updated_at.isoformat(),
            "thumbnail_url": result.thumbnail_url,
            "folder_id": result.folder_id,
            "brand_kit_id": result.brand_kit_id
        }
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("create_design", False, duration, str(e))
        raise

async def list_designs(
    mcp: FastMCP,
    limit: int = 50,
    page_token: Optional[str] = None,
    folder_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    List all designs for the current user.
    
    Args:
        limit: Maximum number of designs to return
        page_token: Token for pagination
        folder_id: Optional folder ID to filter designs
        
    Returns:
        List of designs
    """
    start_time = time.time()
    try:
        result = await design_service.list_designs(limit, page_token, folder_id)
        duration = time.time() - start_time
        log_tool_execution("list_designs", True, duration)
        return result
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("list_designs", False, duration, str(e))
        raise

async def get_design(mcp: FastMCP, design_id: str) -> Dict[str, Any]:
    """
    Get metadata for a specific design.
    
    Args:
        design_id: The ID of the design to retrieve
        
    Returns:
        Design metadata
    """
    start_time = time.time()
    try:
        result = await design_service.get_design(design_id)
        duration = time.time() - start_time
        log_tool_execution("get_design", True, duration)
        return {
            "id": result.id,
            "title": result.title,
            "created_at": result.created_at.isoformat(),
            "updated_at": result.updated_at.isoformat(),
            "thumbnail_url": result.thumbnail_url,
            "folder_id": result.folder_id,
            "brand_kit_id": result.brand_kit_id
        }
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("get_design", False, duration, str(e))
        raise

async def get_design_pages(mcp: FastMCP, design_id: str) -> Dict[str, Any]:
    """
    Get metadata for pages in a design.
    
    Args:
        design_id: The ID of the design
        
    Returns:
        Design pages information
    """
    start_time = time.time()
    try:
        result = await design_service.get_design_pages(design_id)
        duration = time.time() - start_time
        log_tool_execution("get_design_pages", True, duration)
        return result
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("get_design_pages", False, duration, str(e))
        raise

async def get_design_export_formats(mcp: FastMCP, design_id: str) -> Dict[str, Any]:
    """
    Get the export formats available for a design.
    
    Args:
        design_id: The ID of the design
        
    Returns:
        Available export formats
    """
    start_time = time.time()
    try:
        result = await design_service.get_design_export_formats(design_id)
        duration = time.time() - start_time
        log_tool_execution("get_design_export_formats", True, duration)
        return result
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("get_design_export_formats", False, duration, str(e))
        raise 