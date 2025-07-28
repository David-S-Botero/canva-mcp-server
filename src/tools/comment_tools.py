"""
Comment tools for Canva MCP Server
"""

import time
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

from ..services.comment_service import CommentService
from ..utils.logging import log_tool_execution

# Import the global config from auth_tools
from .auth_tools import canva_config

comment_service = CommentService(canva_config)

async def create_comment_thread(
    mcp: FastMCP,
    design_id: str,
    content: str,
    page_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new comment thread on a design.
    
    Args:
        design_id: The ID of the design
        content: Comment content
        page_id: Optional page ID for the comment
        
    Returns:
        Created comment thread information
    """
    start_time = time.time()
    try:
        result = await comment_service.create_comment_thread(design_id, content, page_id)
        duration = time.time() - start_time
        log_tool_execution("create_comment_thread", True, duration)
        return {
            "id": result.id,
            "content": result.content,
            "created_at": result.created_at.isoformat(),
            "updated_at": result.updated_at.isoformat(),
            "author_id": result.author_id,
            "design_id": result.design_id,
            "page_id": result.page_id,
            "parent_id": result.parent_id
        }
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("create_comment_thread", False, duration, str(e))
        raise

async def create_comment_reply(
    mcp: FastMCP,
    design_id: str,
    thread_id: str,
    content: str
) -> Dict[str, Any]:
    """
    Reply to a comment on a design.
    
    Args:
        design_id: The ID of the design
        thread_id: The ID of the comment thread
        content: Reply content
        
    Returns:
        Created reply information
    """
    start_time = time.time()
    try:
        result = await comment_service.create_comment_reply(design_id, thread_id, content)
        duration = time.time() - start_time
        log_tool_execution("create_comment_reply", True, duration)
        return {
            "id": result.id,
            "content": result.content,
            "created_at": result.created_at.isoformat(),
            "updated_at": result.updated_at.isoformat(),
            "author_id": result.author_id,
            "design_id": result.design_id,
            "page_id": result.page_id,
            "parent_id": result.parent_id
        }
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("create_comment_reply", False, duration, str(e))
        raise

async def get_comment_thread(mcp: FastMCP, design_id: str, thread_id: str) -> Dict[str, Any]:
    """
    Get metadata for a comment thread.
    
    Args:
        design_id: The ID of the design
        thread_id: The ID of the comment thread
        
    Returns:
        Comment thread metadata
    """
    start_time = time.time()
    try:
        result = await comment_service.get_comment_thread(design_id, thread_id)
        duration = time.time() - start_time
        log_tool_execution("get_comment_thread", True, duration)
        return {
            "id": result.id,
            "content": result.content,
            "created_at": result.created_at.isoformat(),
            "updated_at": result.updated_at.isoformat(),
            "author_id": result.author_id,
            "design_id": result.design_id,
            "page_id": result.page_id,
            "parent_id": result.parent_id
        }
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("get_comment_thread", False, duration, str(e))
        raise

async def list_comment_replies(
    mcp: FastMCP,
    design_id: str,
    thread_id: str,
    limit: int = 50,
    page_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    List the replies to a comment on a design.
    
    Args:
        design_id: The ID of the design
        thread_id: The ID of the comment thread
        limit: Maximum number of replies to return
        page_token: Token for pagination
        
    Returns:
        List of comment replies
    """
    start_time = time.time()
    try:
        result = await comment_service.list_comment_replies(design_id, thread_id, limit, page_token)
        duration = time.time() - start_time
        log_tool_execution("list_comment_replies", True, duration)
        return result
    except Exception as e:
        duration = time.time() - start_time
        log_tool_execution("list_comment_replies", False, duration, str(e))
        raise 