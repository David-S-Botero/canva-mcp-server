"""
Design service for Canva API
Handles design creation, listing, and management
"""

from typing import Dict, Any, Optional, List
from datetime import datetime

from .base_service import BaseService
from ..models.canva_types import CanvaConfig, CanvaDesign

class DesignService(BaseService):
    """Service for handling design-related operations"""
    
    async def create_design(
        self,
        title: str,
        brand_kit_id: Optional[str] = None,
        folder_id: Optional[str] = None
    ) -> CanvaDesign:
        """
        Create a new Canva design.
        
        Args:
            title: Title for the new design
            brand_kit_id: Optional brand kit ID to use
            folder_id: Optional folder ID to place the design in
            
        Returns:
            Created design information
        """
        data = {"title": title}
        if brand_kit_id:
            data["brand_kit_id"] = brand_kit_id
        if folder_id:
            data["folder_id"] = folder_id
        
        response = await self.post("/designs", data=data)
        
        return CanvaDesign(
            id=response["design"]["id"],
            title=response["design"]["title"],
            created_at=datetime.fromisoformat(response["design"]["created_at"].replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(response["design"]["updated_at"].replace("Z", "+00:00")),
            thumbnail_url=response["design"].get("thumbnail_url"),
            folder_id=response["design"].get("folder_id"),
            brand_kit_id=response["design"].get("brand_kit_id")
        )
    
    async def list_designs(
        self,
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
        params = {"limit": limit}
        if page_token:
            params["page_token"] = page_token
        if folder_id:
            params["folder_id"] = folder_id
        
        return await self.get("/designs", params=params)
    
    async def get_design(self, design_id: str) -> CanvaDesign:
        """
        Get metadata for a specific design.
        
        Args:
            design_id: The ID of the design to retrieve
            
        Returns:
            Design metadata
        """
        response = await self.get(f"/designs/{design_id}")
        
        return CanvaDesign(
            id=response["design"]["id"],
            title=response["design"]["title"],
            created_at=datetime.fromisoformat(response["design"]["created_at"].replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(response["design"]["updated_at"].replace("Z", "+00:00")),
            thumbnail_url=response["design"].get("thumbnail_url"),
            folder_id=response["design"].get("folder_id"),
            brand_kit_id=response["design"].get("brand_kit_id")
        )
    
    async def get_design_pages(self, design_id: str) -> Dict[str, Any]:
        """
        Get metadata for pages in a design.
        
        Args:
            design_id: The ID of the design
            
        Returns:
            Design pages information
        """
        return await self.get(f"/designs/{design_id}/pages")
    
    async def get_design_export_formats(self, design_id: str) -> Dict[str, Any]:
        """
        Get the export formats available for a design.
        
        Args:
            design_id: The ID of the design
            
        Returns:
            Available export formats
        """
        return await self.get(f"/designs/{design_id}/export/formats") 