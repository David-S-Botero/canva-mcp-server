"""
Autofill tools for Canva MCP Server
"""

import time
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP

from ..services.autofill_service import AutofillService
from ..utils.logging import log_tool_execution

# Import the global config from auth_tools
from .auth_tools import canva_config

autofill_service = AutofillService(canva_config)

async def create_design_autofill_job(
    mcp: FastMCP,
    brand_template_id: str,
    dataset: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create an asynchronous job to autofill a design from a brand template.
    
    Args:
        brand_template_id: The ID of the brand template
        dataset: Data to autofill the template with
        
    Returns:
        Autofill job information
    """
    start_time = time.time()
    try:
        result = await autofill_service.create_design_autofill_job(brand_template_id, dataset)
        duration = time.time() - start_time
        log_tool_execution("create_design_autofill_job", True, duration)
        return {
            "id": result.id,
            "status": result.status.value,
            "brand_template_id": result.brand_template_id,
            "created_at": result.created_at.isoformat(),
            "completed_at": result.completed_at.isoformat() if result.completed_at else None,
            "design_id": result.design_id,
            "error_message": result.error_message
        }
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("create_design_autofill_job", False, duration, str(e))
        raise

async def get_design_autofill_job(mcp: FastMCP, job_id: str) -> Dict[str, Any]:
    """
    Get the status and results of an autofill job.
    
    Args:
        job_id: The ID of the autofill job
        
    Returns:
        Autofill job status and results
    """
    start_time = time.time()
    try:
        result = await autofill_service.get_design_autofill_job(job_id)
        duration = time.time() - start_time
        log_tool_execution("get_design_autofill_job", True, duration)
        return {
            "id": result.id,
            "status": result.status.value,
            "brand_template_id": result.brand_template_id,
            "created_at": result.created_at.isoformat(),
            "completed_at": result.completed_at.isoformat() if result.completed_at else None,
            "design_id": result.design_id,
            "error_message": result.error_message
        }
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("get_design_autofill_job", False, duration, str(e))
        raise 