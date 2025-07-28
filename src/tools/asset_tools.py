"""
Asset tools for Canva MCP Server
"""

import time
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from ..services.asset_service import AssetService
from ..utils.logging import log_tool_execution

# Import the global config from auth_tools
from .auth_tools import canva_config

asset_service = AssetService(canva_config)

async def create_asset_upload_job(
    mcp: FastMCP,
    filename: str,
    file_size: int,
    folder_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create an asynchronous job to upload an asset.
    
    Args:
        filename: Name of the file to upload
        file_size: Size of the file in bytes
        folder_id: Optional folder ID to place the asset in
        
    Returns:
        Upload job information
    """
    start_time = time.time()
    try:
        result = await asset_service.create_asset_upload_job(filename, file_size, folder_id)
        duration = time.time() - start_time
        log_tool_execution("create_asset_upload_job", True, duration)
        return {
            "id": result.id,
            "status": result.status.value,
            "filename": result.filename,
            "file_size": result.file_size,
            "created_at": result.created_at.isoformat(),
            "completed_at": result.completed_at.isoformat() if result.completed_at else None,
            "asset_id": result.asset_id,
            "error_message": result.error_message
        }
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("create_asset_upload_job", False, duration, str(e))
        raise

async def get_asset_upload_job(mcp: FastMCP, job_id: str) -> Dict[str, Any]:
    """
    Get the status and results of an upload asset job.
    
    Args:
        job_id: The ID of the upload job
        
    Returns:
        Upload job status and results
    """
    start_time = time.time()
    try:
        result = await asset_service.get_asset_upload_job(job_id)
        duration = time.time() - start_time
        log_tool_execution("get_asset_upload_job", True, duration)
        return {
            "id": result.id,
            "status": result.status.value,
            "filename": result.filename,
            "file_size": result.file_size,
            "created_at": result.created_at.isoformat(),
            "completed_at": result.completed_at.isoformat() if result.completed_at else None,
            "asset_id": result.asset_id,
            "error_message": result.error_message
        }
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("get_asset_upload_job", False, duration, str(e))
        raise

async def create_url_asset_upload_job(
    mcp: FastMCP,
    url: str,
    filename: str,
    folder_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create an asynchronous job to upload an asset from a URL.
    
    Args:
        url: URL of the asset to upload
        filename: Name for the uploaded file
        folder_id: Optional folder ID to place the asset in
        
    Returns:
        Upload job information
    """
    start_time = time.time()
    try:
        result = await asset_service.create_url_asset_upload_job(url, filename, folder_id)
        duration = time.time() - start_time
        log_tool_execution("create_url_asset_upload_job", True, duration)
        return {
            "id": result.id,
            "status": result.status.value,
            "filename": result.filename,
            "file_size": result.file_size,
            "created_at": result.created_at.isoformat(),
            "completed_at": result.completed_at.isoformat() if result.completed_at else None,
            "asset_id": result.asset_id,
            "error_message": result.error_message
        }
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("create_url_asset_upload_job", False, duration, str(e))
        raise

async def get_url_asset_upload_job(mcp: FastMCP, job_id: str) -> Dict[str, Any]:
    """
    Get the status and results of a URL asset upload job.
    
    Args:
        job_id: The ID of the upload job
        
    Returns:
        Upload job status and results
    """
    start_time = time.time()
    try:
        result = await asset_service.get_url_asset_upload_job(job_id)
        duration = time.time() - start_time
        log_tool_execution("get_url_asset_upload_job", True, duration)
        return {
            "id": result.id,
            "status": result.status.value,
            "filename": result.filename,
            "file_size": result.file_size,
            "created_at": result.created_at.isoformat(),
            "completed_at": result.completed_at.isoformat() if result.completed_at else None,
            "asset_id": result.asset_id,
            "error_message": result.error_message
        }
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("get_url_asset_upload_job", False, duration, str(e))
        raise

async def get_asset(mcp: FastMCP, asset_id: str) -> Dict[str, Any]:
    """
    Get the metadata for an asset.
    
    Args:
        asset_id: The ID of the asset
        
    Returns:
        Asset metadata
    """
    start_time = time.time()
    try:
        result = await asset_service.get_asset(asset_id)
        duration = time.time() - start_time
        log_tool_execution("get_asset", True, duration)
        return {
            "id": result.id,
            "title": result.title,
            "filename": result.filename,
            "file_size": result.file_size,
            "mime_type": result.mime_type,
            "created_at": result.created_at.isoformat(),
            "updated_at": result.updated_at.isoformat(),
            "folder_id": result.folder_id,
            "tags": result.tags
        }
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("get_asset", False, duration, str(e))
        raise

async def update_asset(
    mcp: FastMCP,
    asset_id: str,
    title: Optional[str] = None,
    tags: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Update the metadata for an asset.
    
    Args:
        asset_id: The ID of the asset to update
        title: New title for the asset
        tags: New tags for the asset
        
    Returns:
        Updated asset information
    """
    start_time = time.time()
    try:
        result = await asset_service.update_asset(asset_id, title, tags)
        duration = time.time() - start_time
        log_tool_execution("update_asset", True, duration)
        return {
            "id": result.id,
            "title": result.title,
            "filename": result.filename,
            "file_size": result.file_size,
            "mime_type": result.mime_type,
            "created_at": result.created_at.isoformat(),
            "updated_at": result.updated_at.isoformat(),
            "folder_id": result.folder_id,
            "tags": result.tags
        }
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("update_asset", False, duration, str(e))
        raise

async def delete_asset(mcp: FastMCP, asset_id: str) -> Dict[str, Any]:
    """
    Delete an asset.
    
    Args:
        asset_id: The ID of the asset to delete
        
    Returns:
        Deletion confirmation
    """
    start_time = time.time()
    try:
        result = await asset_service.delete_asset(asset_id)
        duration = time.time() - start_time
        log_tool_execution("delete_asset", True, duration)
        return result
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("delete_asset", False, duration, str(e))
        raise 