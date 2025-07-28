"""
Canva MCP Server - Main Server File
Refactored version with organized structure
"""

import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from src.utils.logging import log_server_startup, log_server_shutdown, logger
from src.tools.auth_tools import canva_config as auth_config

# Load environment variables
load_dotenv()

# Initialize MCP server
mcp = FastMCP(
    "Canva MCP Server", 
    "1.0.0"
)

def setup_configuration():
    """Setup configuration from environment variables"""
    auth_config.client_id = os.getenv("CANVA_CLIENT_ID", "")
    auth_config.client_secret = os.getenv("CANVA_CLIENT_SECRET", "")
    auth_config.redirect_uri = os.getenv("CANVA_REDIRECT_URI", "")

def register_tools():
    """Register all MCP tools"""
    from src.tools import (
        # Auth tools
        create_authorization_url,
        exchange_code_for_token,
        refresh_access_token,
        get_oauth_config,
        clear_tokens,
        
        # User tools
        get_current_user,
        get_user_profile,
        get_user_capabilities,
        
        # Design tools
        create_design,
        list_designs,
        get_design,
        get_design_pages,
        get_design_export_formats,
        
        # Asset tools
        create_asset_upload_job,
        get_asset_upload_job,
        create_url_asset_upload_job,
        get_url_asset_upload_job,
        get_asset,
        update_asset,
        delete_asset,
        
        # Folder tools
        create_folder,
        get_folder,
        update_folder,
        delete_folder,
        list_folder_items,
        move_folder_item,
        
        # Export tools
        create_design_export_job,
        get_design_export_job,
        
        # Brand template tools
        list_brand_templates,
        get_brand_template,
        get_brand_template_dataset,
        
        # Autofill tools
        create_design_autofill_job,
        get_design_autofill_job,
        
        # Comment tools
        create_comment_thread,
        create_comment_reply,
        get_comment_thread,
        list_comment_replies,
    )
    
    # Register all tools with the MCP server
    tools = [
        # Auth tools
        create_authorization_url,
        exchange_code_for_token,
        refresh_access_token,
        get_oauth_config,
        clear_tokens,
        
        # User tools
        get_current_user,
        get_user_profile,
        get_user_capabilities,
        
        # Design tools
        create_design,
        list_designs,
        get_design,
        get_design_pages,
        get_design_export_formats,
        
        # Asset tools
        create_asset_upload_job,
        get_asset_upload_job,
        create_url_asset_upload_job,
        get_url_asset_upload_job,
        get_asset,
        update_asset,
        delete_asset,
        
        # Folder tools
        create_folder,
        get_folder,
        update_folder,
        delete_folder,
        list_folder_items,
        move_folder_item,
        
        # Export tools
        create_design_export_job,
        get_design_export_job,
        
        # Brand template tools
        list_brand_templates,
        get_brand_template,
        get_brand_template_dataset,
        
        # Autofill tools
        create_design_autofill_job,
        get_design_autofill_job,
        
        # Comment tools
        create_comment_thread,
        create_comment_reply,
        get_comment_thread,
        list_comment_replies,
    ]
    
    for tool in tools:
        mcp.tool()(tool)

def main():
    """Main server function"""
    try:
        # Setup configuration
        setup_configuration()
        
        # Log server startup
        log_server_startup()
        
        # Register all tools
        register_tools()
        
        # Start the server with SSE transport
        logger.info("Starting Canva MCP Server with SSE transport...")
        mcp.run(transport="sse")
        
    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise
    finally:
        log_server_shutdown()

if __name__ == "__main__":
    main()



