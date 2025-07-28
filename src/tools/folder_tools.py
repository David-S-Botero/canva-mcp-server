"""
Folder tools for Canva MCP Server
"""

import time
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

from ..services.folder_service import FolderService
from ..utils.logging import log_tool_execution

# Import the global config from auth_tools
from .auth_tools import canva_config

folder_service = FolderService(canva_config)

async def create_folder(
    mcp: FastMCP,
    name: str,
    parent_folder_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new folder.
    
    Args:
        name: Name of the folder
        parent_folder_id: Optional parent folder ID
        
    Returns:
        Created folder information
    """
    start_time = time.time()
    try:
        result = await folder_service.create_folder(name, parent_folder_id)
        duration = time.time() - start_time
        log_tool_execution("create_folder", True, duration)
        return {
            "id": result.id,
            "name": result.name,
            "created_at": result.created_at.isoformat(),
            "updated_at": result.updated_at.isoformat(),
            "parent_folder_id": result.parent_folder_id,
            "item_count": result.item_count
        }
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("create_folder", False, duration, str(e))
        raise

async def get_folder(mcp: FastMCP, folder_id: str) -> Dict[str, Any]:
    """
    Get folder metadata.
    
    Args:
        folder_id: The ID of the folder
        
    Returns:
        Folder metadata
    """
    start_time = time.time()
    try:
        result = await folder_service.get_folder(folder_id)
        duration = time.time() - start_time
        log_tool_execution("get_folder", True, duration)
        return {
            "id": result.id,
            "name": result.name,
            "created_at": result.created_at.isoformat(),
            "updated_at": result.updated_at.isoformat(),
            "parent_folder_id": result.parent_folder_id,
            "item_count": result.item_count
        }
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("get_folder", False, duration, str(e))
        raise

async def update_folder(
    mcp: FastMCP,
    folder_id: str,
    name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update folder metadata.
    
    Args:
        folder_id: The ID of the folder to update
        name: New name for the folder
        
    Returns:
        Updated folder information
    """
    start_time = time.time()
    try:
        result = await folder_service.update_folder(folder_id, name)
        duration = time.time() - start_time
        log_tool_execution("update_folder", True, duration)
        return {
            "id": result.id,
            "name": result.name,
            "created_at": result.created_at.isoformat(),
            "updated_at": result.updated_at.isoformat(),
            "parent_folder_id": result.parent_folder_id,
            "item_count": result.item_count
        }
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("update_folder", False, duration, str(e))
        raise

async def delete_folder(mcp: FastMCP, folder_id: str) -> Dict[str, Any]:
    """
    Delete a folder.
    
    Args:
        folder_id: The ID of the folder to delete
        
    Returns:
        Deletion confirmation
    """
    start_time = time.time()
    try:
        result = await folder_service.delete_folder(folder_id)
        duration = time.time() - start_time
        log_tool_execution("delete_folder", True, duration)
        return result
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("delete_folder", False, duration, str(e))
        raise

async def list_folder_items(
    mcp: FastMCP,
    folder_id: str,
    limit: int = 50,
    page_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    List the contents of a folder.
    
    Args:
        folder_id: The ID of the folder
        limit: Maximum number of items to return
        page_token: Token for pagination
        
    Returns:
        Folder contents
    """
    start_time = time.time()
    try:
        result = await folder_service.list_folder_items(folder_id, limit, page_token)
        duration = time.time() - start_time
        log_tool_execution("list_folder_items", True, duration)
        return result
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("list_folder_items", False, duration, str(e))
        raise

async def move_folder_item(
    mcp: FastMCP,
    item_id: str,
    destination_folder_id: str,
    item_type: str
) -> Dict[str, Any]:
    """
    Move an item from one folder to another.
    
    Args:
        item_id: The ID of the item to move
        destination_folder_id: The ID of the destination folder
        item_type: Type of item (design, asset, folder)
        
    Returns:
        Move confirmation
    """
    start_time = time.time()
    try:
        result = await folder_service.move_folder_item(item_id, destination_folder_id, item_type)
        duration = time.time() - start_time
        log_tool_execution("move_folder_item", True, duration)
        return result
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("move_folder_item", False, duration, str(e))
        raise 