"""
Asset service for Canva API
Handles asset upload, management, and operations
"""

from typing import Dict, Any, Optional, List
from datetime import datetime

from .base_service import BaseService
from ..models.canva_types import CanvaConfig, CanvaAsset, CanvaUploadJob

class AssetService(BaseService):
    """Service for handling asset-related operations"""
    
    async def create_asset_upload_job(
        self,
        filename: str,
        file_size: int,
        folder_id: Optional[str] = None
    ) -> CanvaUploadJob:
        """
        Create an asynchronous job to upload an asset.
        
        Args:
            filename: Name of the file to upload
            file_size: Size of the file in bytes
            folder_id: Optional folder ID to place the asset in
            
        Returns:
            Upload job information
        """
        data = {
            "filename": filename,
            "file_size": file_size
        }
        if folder_id:
            data["folder_id"] = folder_id
        
        response = await self.post("/assets/upload", data=data)
        
        return CanvaUploadJob(
            id=response["job"]["id"],
            status=response["job"]["status"],
            filename=filename,
            file_size=file_size,
            created_at=datetime.fromisoformat(response["job"]["created_at"].replace("Z", "+00:00")),
            completed_at=datetime.fromisoformat(response["job"]["completed_at"].replace("Z", "+00:00")) if response["job"].get("completed_at") else None,
            asset_id=response["job"].get("asset_id"),
            error_message=response["job"].get("error_message")
        )
    
    async def get_asset_upload_job(self, job_id: str) -> CanvaUploadJob:
        """
        Get the status and results of an upload asset job.
        
        Args:
            job_id: The ID of the upload job
            
        Returns:
            Upload job status and results
        """
        response = await self.get(f"/assets/upload/{job_id}")
        
        return CanvaUploadJob(
            id=response["job"]["id"],
            status=response["job"]["status"],
            filename=response["job"]["filename"],
            file_size=response["job"]["file_size"],
            created_at=datetime.fromisoformat(response["job"]["created_at"].replace("Z", "+00:00")),
            completed_at=datetime.fromisoformat(response["job"]["completed_at"].replace("Z", "+00:00")) if response["job"].get("completed_at") else None,
            asset_id=response["job"].get("asset_id"),
            error_message=response["job"].get("error_message")
        )
    
    async def create_url_asset_upload_job(
        self,
        url: str,
        filename: str,
        folder_id: Optional[str] = None
    ) -> CanvaUploadJob:
        """
        Create an asynchronous job to upload an asset from a URL.
        
        Args:
            url: URL of the asset to upload
            filename: Name for the uploaded file
            folder_id: Optional folder ID to place the asset in
            
        Returns:
            Upload job information
        """
        data = {
            "url": url,
            "filename": filename
        }
        if folder_id:
            data["folder_id"] = folder_id
        
        response = await self.post("/assets/upload/url", data=data)
        
        return CanvaUploadJob(
            id=response["job"]["id"],
            status=response["job"]["status"],
            filename=filename,
            file_size=0,  # Will be determined during upload
            created_at=datetime.fromisoformat(response["job"]["created_at"].replace("Z", "+00:00")),
            completed_at=datetime.fromisoformat(response["job"]["completed_at"].replace("Z", "+00:00")) if response["job"].get("completed_at") else None,
            asset_id=response["job"].get("asset_id"),
            error_message=response["job"].get("error_message")
        )
    
    async def get_url_asset_upload_job(self, job_id: str) -> CanvaUploadJob:
        """
        Get the status and results of a URL asset upload job.
        
        Args:
            job_id: The ID of the upload job
            
        Returns:
            Upload job status and results
        """
        response = await self.get(f"/assets/upload/url/{job_id}")
        
        return CanvaUploadJob(
            id=response["job"]["id"],
            status=response["job"]["status"],
            filename=response["job"]["filename"],
            file_size=response["job"].get("file_size", 0),
            created_at=datetime.fromisoformat(response["job"]["created_at"].replace("Z", "+00:00")),
            completed_at=datetime.fromisoformat(response["job"]["completed_at"].replace("Z", "+00:00")) if response["job"].get("completed_at") else None,
            asset_id=response["job"].get("asset_id"),
            error_message=response["job"].get("error_message")
        )
    
    async def get_asset(self, asset_id: str) -> CanvaAsset:
        """
        Get the metadata for an asset.
        
        Args:
            asset_id: The ID of the asset
            
        Returns:
            Asset metadata
        """
        response = await self.get(f"/assets/{asset_id}")
        
        return CanvaAsset(
            id=response["asset"]["id"],
            title=response["asset"]["title"],
            filename=response["asset"]["filename"],
            file_size=response["asset"]["file_size"],
            mime_type=response["asset"]["mime_type"],
            created_at=datetime.fromisoformat(response["asset"]["created_at"].replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(response["asset"]["updated_at"].replace("Z", "+00:00")),
            folder_id=response["asset"].get("folder_id"),
            tags=response["asset"].get("tags")
        )
    
    async def update_asset(
        self,
        asset_id: str,
        title: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> CanvaAsset:
        """
        Update the metadata for an asset.
        
        Args:
            asset_id: The ID of the asset to update
            title: New title for the asset
            tags: New tags for the asset
            
        Returns:
            Updated asset information
        """
        data = {}
        if title:
            data["title"] = title
        if tags:
            data["tags"] = tags
        
        response = await self.patch(f"/assets/{asset_id}", data=data)
        
        return CanvaAsset(
            id=response["asset"]["id"],
            title=response["asset"]["title"],
            filename=response["asset"]["filename"],
            file_size=response["asset"]["file_size"],
            mime_type=response["asset"]["mime_type"],
            created_at=datetime.fromisoformat(response["asset"]["created_at"].replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(response["asset"]["updated_at"].replace("Z", "+00:00")),
            folder_id=response["asset"].get("folder_id"),
            tags=response["asset"].get("tags")
        )
    
    async def delete_asset(self, asset_id: str) -> Dict[str, Any]:
        """
        Delete an asset.
        
        Args:
            asset_id: The ID of the asset to delete
            
        Returns:
            Deletion confirmation
        """
        return await self.delete(f"/assets/{asset_id}") 