"""
Export tools for Canva MCP Server
"""

import time
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

from ..services.export_service import ExportService
from ..models.canva_types import CanvaFileType
from ..utils.logging import log_tool_execution

# Import the global config from auth_tools
from .auth_tools import canva_config

export_service = ExportService(canva_config)

async def create_design_export_job(
    mcp: FastMCP,
    design_id: str,
    file_type: str,
    page_range: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create an asynchronous job to export a design.
    
    Args:
        design_id: The ID of the design to export
        file_type: Export format (pdf, jpg, png, gif, pptx, mp4)
        page_range: Optional page range (e.g., "1-3", "1,3,5")
        
    Returns:
        Export job information
    """
    start_time = time.time()
    try:
        canva_file_type = CanvaFileType(file_type)
        result = await export_service.create_design_export_job(design_id, canva_file_type, page_range)
        duration = time.time() - start_time
        log_tool_execution("create_design_export_job", True, duration)
        return {
            "id": result.id,
            "status": result.status.value,
            "file_type": result.file_type.value,
            "created_at": result.created_at.isoformat(),
            "completed_at": result.completed_at.isoformat() if result.completed_at else None,
            "download_url": result.download_url,
            "error_message": result.error_message
        }
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("create_design_export_job", False, duration, str(e))
        raise

async def get_design_export_job(mcp: FastMCP, job_id: str) -> Dict[str, Any]:
    """
    Get the status and results of an export job.
    
    Args:
        job_id: The ID of the export job
        
    Returns:
        Export job status and results
    """
    start_time = time.time()
    try:
        result = await export_service.get_design_export_job(job_id)
        duration = time.time() - start_time
        log_tool_execution("get_design_export_job", True, duration)
        return {
            "id": result.id,
            "status": result.status.value,
            "file_type": result.file_type.value,
            "created_at": result.created_at.isoformat(),
            "completed_at": result.completed_at.isoformat() if result.completed_at else None,
            "download_url": result.download_url,
            "error_message": result.error_message
        }
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("get_design_export_job", False, duration, str(e))
        raise 