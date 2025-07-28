import logging
import sys
import os
from datetime import datetime
from typing import Optional

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('canva_mcp_server.log')
    ]
)

def setup_logger(name: str = "canva_mcp_server", level: Optional[str] = None) -> logging.Logger:
    """
    Set up a logger with the specified name and level.
    
    Args:
        name: Name of the logger
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Set log level
    if level:
        log_level = getattr(logging, level.upper(), logging.INFO)
        logger.setLevel(log_level)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Console handler with simple format
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    
    # File handler with detailed format
    file_handler = logging.FileHandler('canva_mcp_server.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    
    # Error file handler
    error_handler = logging.FileHandler('canva_mcp_server_errors.log')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    
    # Clear existing handlers and add new ones
    logger.handlers.clear()
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    
    return logger

def log_api_request(method: str, endpoint: str, status_code: int, duration: float):
    """
    Log API request details.
    
    Args:
        method: HTTP method
        endpoint: API endpoint
        status_code: HTTP status code
        duration: Request duration in seconds
    """
    logger = logging.getLogger("canva_mcp_server.api")
    
    if status_code >= 400:
        logger.error(f"API Request failed: {method} {endpoint} - Status: {status_code} - Duration: {duration:.3f}s")
    elif status_code >= 300:
        logger.warning(f"API Request redirected: {method} {endpoint} - Status: {status_code} - Duration: {duration:.3f}s")
    else:
        logger.info(f"API Request successful: {method} {endpoint} - Status: {status_code} - Duration: {duration:.3f}s")

def log_oauth_flow(step: str, details: dict = None):
    """
    Log OAuth flow steps.
    
    Args:
        step: OAuth step description
        details: Additional details (optional)
    """
    logger = logging.getLogger("canva_mcp_server.oauth")
    
    if details:
        logger.info(f"OAuth Flow - {step}: {details}")
    else:
        logger.info(f"OAuth Flow - {step}")

def log_tool_execution(tool_name: str, success: bool, duration: float, error: str = None):
    """
    Log tool execution details.
    
    Args:
        tool_name: Name of the executed tool
        success: Whether the tool execution was successful
        duration: Execution duration in seconds
        error: Error message if execution failed
    """
    logger = logging.getLogger("canva_mcp_server.tools")
    
    if success:
        logger.info(f"Tool executed successfully: {tool_name} - Duration: {duration:.3f}s")
    else:
        logger.error(f"Tool execution failed: {tool_name} - Duration: {duration:.3f}s - Error: {error}")

def log_configuration_check():
    """
    Log configuration status.
    """
    logger = logging.getLogger("canva_mcp_server.config")
    
    # Check environment variables
    client_id = os.getenv("CANVA_CLIENT_ID")
    client_secret = os.getenv("CANVA_CLIENT_SECRET")
    redirect_uri = os.getenv("CANVA_REDIRECT_URI")
    
    logger.info("Configuration check:")
    logger.info(f"  - CANVA_CLIENT_ID: {'✅ Set' if client_id else '❌ Not set'}")
    logger.info(f"  - CANVA_CLIENT_SECRET: {'✅ Set' if client_secret else '❌ Not set'}")
    logger.info(f"  - CANVA_REDIRECT_URI: {'✅ Set' if redirect_uri else '❌ Not set'}")

def log_server_startup():
    """
    Log server startup information.
    """
    logger = logging.getLogger("canva_mcp_server")
    
    logger.info("=" * 50)
    logger.info("Canva MCP Server Starting")
    logger.info("=" * 50)
    logger.info(f"Startup time: {datetime.now().isoformat()}")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Working directory: {os.getcwd()}")
    
    # Log configuration
    log_configuration_check()

def log_server_shutdown():
    """
    Log server shutdown information.
    """
    logger = logging.getLogger("canva_mcp_server")
    
    logger.info("=" * 50)
    logger.info("Canva MCP Server Shutting Down")
    logger.info("=" * 50)
    logger.info(f"Shutdown time: {datetime.now().isoformat()}")

# Create default logger instance
logger = setup_logger()

# Export commonly used functions
__all__ = [
    'setup_logger',
    'log_api_request',
    'log_oauth_flow',
    'log_tool_execution',
    'log_configuration_check',
    'log_server_startup',
    'log_server_shutdown',
    'logger'
]

