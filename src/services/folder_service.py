"""
Folder service for Canva API
Handles folder creation, management, and operations
"""

from typing import Dict, Any, Optional
from datetime import datetime

from .base_service import BaseService
from ..models.canva_types import CanvaConfig, CanvaFolder

class FolderService(BaseService):
    """Service for handling folder-related operations"""
    
    async def create_folder(
        self,
        name: str,
        parent_folder_id: Optional[str] = None
    ) -> CanvaFolder:
        """
        Create a new folder.
        
        Args:
            name: Name of the folder
            parent_folder_id: Optional parent folder ID
            
        Returns:
            Created folder information
        """
        data = {"name": name}
        if parent_folder_id:
            data["parent_folder_id"] = parent_folder_id
        
        response = await self.post("/folders", data=data)
        
        return CanvaFolder(
            id=response["folder"]["id"],
            name=response["folder"]["name"],
            created_at=datetime.fromisoformat(response["folder"]["created_at"].replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(response["folder"]["updated_at"].replace("Z", "+00:00")),
            parent_folder_id=response["folder"].get("parent_folder_id"),
            item_count=response["folder"].get("item_count")
        )
    
    async def get_folder(self, folder_id: str) -> CanvaFolder:
        """
        Get folder metadata.
        
        Args:
            folder_id: The ID of the folder
            
        Returns:
            Folder metadata
        """
        response = await self.get(f"/folders/{folder_id}")
        
        return CanvaFolder(
            id=response["folder"]["id"],
            name=response["folder"]["name"],
            created_at=datetime.fromisoformat(response["folder"]["created_at"].replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(response["folder"]["updated_at"].replace("Z", "+00:00")),
            parent_folder_id=response["folder"].get("parent_folder_id"),
            item_count=response["folder"].get("item_count")
        )
    
    async def update_folder(
        self,
        folder_id: str,
        name: Optional[str] = None
    ) -> CanvaFolder:
        """
        Update folder metadata.
        
        Args:
            folder_id: The ID of the folder to update
            name: New name for the folder
            
        Returns:
            Updated folder information
        """
        data = {}
        if name:
            data["name"] = name
        
        response = await self.patch(f"/folders/{folder_id}", data=data)
        
        return CanvaFolder(
            id=response["folder"]["id"],
            name=response["folder"]["name"],
            created_at=datetime.fromisoformat(response["folder"]["created_at"].replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(response["folder"]["updated_at"].replace("Z", "+00:00")),
            parent_folder_id=response["folder"].get("parent_folder_id"),
            item_count=response["folder"].get("item_count")
        )
    
    async def delete_folder(self, folder_id: str) -> Dict[str, Any]:
        """
        Delete a folder.
        
        Args:
            folder_id: The ID of the folder to delete
            
        Returns:
            Deletion confirmation
        """
        return await self.delete(f"/folders/{folder_id}")
    
    async def list_folder_items(
        self,
        folder_id: str,
        limit: int = 50,
        page_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List the contents of a folder.
        
        Args:
            folder_id: The ID of the folder
            limit: Maximum number of items to return
            page_token: Token for pagination
            
        Returns:
            Folder contents
        """
        params = {"limit": limit}
        if page_token:
            params["page_token"] = page_token
        
        return await self.get(f"/folders/{folder_id}/items", params=params)
    
    async def move_folder_item(
        self,
        item_id: str,
        destination_folder_id: str,
        item_type: str
    ) -> Dict[str, Any]:
        """
        Move an item from one folder to another.
        
        Args:
            item_id: The ID of the item to move
            destination_folder_id: The ID of the destination folder
            item_type: Type of item (design, asset, folder)
            
        Returns:
            Move confirmation
        """
        data = {
            "destination_folder_id": destination_folder_id,
            "item_type": item_type
        }
        
        return await self.post(f"/folders/items/{item_id}/move", data=data) 