"""
Export service for Canva API
Handles design export operations
"""

from typing import Dict, Any, Optional
from datetime import datetime

from .base_service import BaseService
from ..models.canva_types import CanvaConfig, CanvaExportJob, CanvaFileType

class ExportService(BaseService):
    """Service for handling export-related operations"""
    
    async def create_design_export_job(
        self,
        design_id: str,
        file_type: CanvaFileType,
        page_range: Optional[str] = None
    ) -> CanvaExportJob:
        """
        Create an asynchronous job to export a design.
        
        Args:
            design_id: The ID of the design to export
            file_type: Export format (pdf, jpg, png, gif, pptx, mp4)
            page_range: Optional page range (e.g., "1-3", "1,3,5")
            
        Returns:
            Export job information
        """
        data = {
            "file_type": file_type.value
        }
        if page_range:
            data["page_range"] = page_range
        
        response = await self.post(f"/designs/{design_id}/exports", data=data)
        
        return CanvaExportJob(
            id=response["job"]["id"],
            status=response["job"]["status"],
            file_type=file_type,
            created_at=datetime.fromisoformat(response["job"]["created_at"].replace("Z", "+00:00")),
            completed_at=datetime.fromisoformat(response["job"]["completed_at"].replace("Z", "+00:00")) if response["job"].get("completed_at") else None,
            download_url=response["job"].get("download_url"),
            error_message=response["job"].get("error_message")
        )
    
    async def get_design_export_job(self, job_id: str) -> CanvaExportJob:
        """
        Get the status and results of an export job.
        
        Args:
            job_id: The ID of the export job
            
        Returns:
            Export job status and results
        """
        response = await self.get(f"/exports/{job_id}")
        
        return CanvaExportJob(
            id=response["job"]["id"],
            status=response["job"]["status"],
            file_type=CanvaFileType(response["job"]["file_type"]),
            created_at=datetime.fromisoformat(response["job"]["created_at"].replace("Z", "+00:00")),
            completed_at=datetime.fromisoformat(response["job"]["completed_at"].replace("Z", "+00:00")) if response["job"].get("completed_at") else None,
            download_url=response["job"].get("download_url"),
            error_message=response["job"].get("error_message")
        ) 