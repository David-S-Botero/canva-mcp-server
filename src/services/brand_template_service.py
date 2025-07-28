"""
Brand template service for Canva API
Handles brand template operations
"""

from typing import Dict, Any, Optional
from datetime import datetime

from .base_service import BaseService
from ..models.canva_types import CanvaConfig, CanvaBrandTemplate

class BrandTemplateService(BaseService):
    """Service for handling brand template operations"""
    
    async def list_brand_templates(
        self,
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
        params = {"limit": limit}
        if page_token:
            params["page_token"] = page_token
        
        return await self.get("/brand-templates", params=params)
    
    async def get_brand_template(self, template_id: str) -> CanvaBrandTemplate:
        """
        Get metadata for a brand template.
        
        Args:
            template_id: The ID of the brand template
            
        Returns:
            Brand template metadata
        """
        response = await self.get(f"/brand-templates/{template_id}")
        
        return CanvaBrandTemplate(
            id=response["brand_template"]["id"],
            title=response["brand_template"]["title"],
            description=response["brand_template"].get("description"),
            created_at=datetime.fromisoformat(response["brand_template"]["created_at"].replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(response["brand_template"]["updated_at"].replace("Z", "+00:00")),
            has_dataset=response["brand_template"].get("has_dataset", False)
        )
    
    async def get_brand_template_dataset(self, template_id: str) -> Dict[str, Any]:
        """
        Get the dataset for a brand template to check autofill capabilities.
        
        Args:
            template_id: The ID of the brand template
            
        Returns:
            Brand template dataset information
        """
        return await self.get(f"/brand-templates/{template_id}/dataset") 