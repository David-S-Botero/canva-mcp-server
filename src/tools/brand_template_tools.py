"""
Brand template tools for Canva MCP Server
"""

import time
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

from ..services.brand_template_service import BrandTemplateService
from ..utils.logging import log_tool_execution

# Import the global config from auth_tools
from .auth_tools import canva_config

brand_template_service = BrandTemplateService(canva_config)

async def list_brand_templates(
    mcp: FastMCP,
    limit: int = 50,
    page_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    List all brand templates for the user.
    
    Args:
        limit: Maximum number of templates to return
        page_token: Token for pagination
        
    Returns:
        List of brand templates
    """
    start_time = time.time()
    try:
        result = await brand_template_service.list_brand_templates(limit, page_token)
        duration = time.time() - start_time
        log_tool_execution("list_brand_templates", True, duration)
        return result
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("list_brand_templates", False, duration, str(e))
        raise

async def get_brand_template(mcp: FastMCP, template_id: str) -> Dict[str, Any]:
    """
    Get metadata for a brand template.
    
    Args:
        template_id: The ID of the brand template
        
    Returns:
        Brand template metadata
    """
    start_time = time.time()
    try:
        result = await brand_template_service.get_brand_template(template_id)
        duration = time.time() - start_time
        log_tool_execution("get_brand_template", True, duration)
        return {
            "id": result.id,
            "title": result.title,
            "description": result.description,
            "created_at": result.created_at.isoformat(),
            "updated_at": result.updated_at.isoformat(),
            "has_dataset": result.has_dataset
        }
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("get_brand_template", False, duration, str(e))
        raise

async def get_brand_template_dataset(mcp: FastMCP, template_id: str) -> Dict[str, Any]:
    """
    Get the dataset for a brand template to check autofill capabilities.
    
    Args:
        template_id: The ID of the brand template
        
    Returns:
        Brand template dataset information
    """
    start_time = time.time()
    try:
        result = await brand_template_service.get_brand_template_dataset(template_id)
        duration = time.time() - start_time
        log_tool_execution("get_brand_template_dataset", True, duration)
        return result
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("get_brand_template_dataset", False, duration, str(e))
        raise 