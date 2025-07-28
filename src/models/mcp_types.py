"""
MCP-specific data types and models
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, Callable
from enum import Enum

class MCPToolCategory(str, Enum):
    """Categories for MCP tools"""
    AUTHENTICATION = "authentication"
    USER_MANAGEMENT = "user_management"
    DESIGN_MANAGEMENT = "design_management"
    ASSET_MANAGEMENT = "asset_management"
    FOLDER_MANAGEMENT = "folder_management"
    EXPORT = "export"
    BRAND_TEMPLATES = "brand_templates"
    AUTOFILL = "autofill"
    COMMENTS = "comments"
    UTILITY = "utility"

@dataclass
class MCPTool:
    """MCP tool definition"""
    name: str
    description: str
    category: MCPToolCategory
    function: Callable
    parameters: Dict[str, Any]
    return_type: str

@dataclass
class MCPResponse:
    """Standard MCP response format"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    message: Optional[str] = None

@dataclass
class MCPError:
    """MCP error information"""
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None

@dataclass
class MCPToolResult:
    """Result from MCP tool execution"""
    tool_name: str
    success: bool
    duration: float
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None 