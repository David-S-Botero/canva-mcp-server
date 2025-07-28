"""
Base service for common HTTP operations
"""

import time
from typing import Dict, Any, Optional
import httpx

from ..models.canva_types import CanvaConfig
from ..utils.logging import log_api_request

class BaseService:
    """Base service for common HTTP operations"""
    
    def __init__(self, config: CanvaConfig):
        self.config = config
        self.api_base = "https://api.canva.com/rest/v1"
    
    async def make_request(
        self,
        method: str,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make a request to the Canva API
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            headers: Request headers
            data: Request body data
            params: Query parameters
            
        Returns:
            API response data
        """
        if headers is None:
            headers = {}
        
        # Add authentication header if token is available
        if self.config.access_token:
            headers['Authorization'] = f'Bearer {self.config.access_token}'
        
        url = f"{self.api_base}{endpoint}"
        
        start_time = time.time()
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                json=data if data else None,
                params=params
            )
            duration = time.time() - start_time
        
        log_api_request(method, endpoint, response.status_code, duration)
        
        if response.status_code >= 400:
            error_detail = response.json() if response.content else {}
            raise Exception(f"Canva API error: {response.status_code} - {error_detail}")
        
        return response.json() if response.content else {}
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request"""
        return await self.make_request("GET", endpoint, params=params)
    
    async def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a POST request"""
        return await self.make_request("POST", endpoint, data=data)
    
    async def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a PATCH request"""
        return await self.make_request("PATCH", endpoint, data=data)
    
    async def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make a DELETE request"""
        return await self.make_request("DELETE", endpoint) 