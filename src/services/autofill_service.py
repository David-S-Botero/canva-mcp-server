"""
Autofill service for Canva API
Handles design autofill operations
"""

from typing import Dict, Any
from datetime import datetime

from .base_service import BaseService
from ..models.canva_types import CanvaConfig, CanvaAutofillJob

class AutofillService(BaseService):
    """Service for handling autofill operations"""
    
    async def create_design_autofill_job(
        self,
        brand_template_id: str,
        dataset: Dict[str, Any]
    ) -> CanvaAutofillJob:
        """
        Create an asynchronous job to autofill a design from a brand template.
        
        Args:
            brand_template_id: The ID of the brand template
            dataset: Data to autofill the template with
            
        Returns:
            Autofill job information
        """
        data = {
            "brand_template_id": brand_template_id,
            "dataset": dataset
        }
        
        response = await self.post("/autofills", data=data)
        
        return CanvaAutofillJob(
            id=response["job"]["id"],
            status=response["job"]["status"],
            brand_template_id=brand_template_id,
            created_at=datetime.fromisoformat(response["job"]["created_at"].replace("Z", "+00:00")),
            completed_at=datetime.fromisoformat(response["job"]["completed_at"].replace("Z", "+00:00")) if response["job"].get("completed_at") else None,
            design_id=response["job"].get("design_id"),
            error_message=response["job"].get("error_message")
        )
    
    async def get_design_autofill_job(self, job_id: str) -> CanvaAutofillJob:
        """
        Get the status and results of an autofill job.
        
        Args:
            job_id: The ID of the autofill job
            
        Returns:
            Autofill job status and results
        """
        response = await self.get(f"/autofills/{job_id}")
        
        return CanvaAutofillJob(
            id=response["job"]["id"],
            status=response["job"]["status"],
            brand_template_id=response["job"]["brand_template_id"],
            created_at=datetime.fromisoformat(response["job"]["created_at"].replace("Z", "+00:00")),
            completed_at=datetime.fromisoformat(response["job"]["completed_at"].replace("Z", "+00:00")) if response["job"].get("completed_at") else None,
            design_id=response["job"].get("design_id"),
            error_message=response["job"].get("error_message")
        ) 