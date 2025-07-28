"""
User service for Canva API
Handles user information and capabilities
"""

from typing import Dict, Any
from datetime import datetime

from .base_service import BaseService
from ..models.canva_types import CanvaConfig, CanvaUser

class UserService(BaseService):
    """Service for handling user-related operations"""
    
    async def get_current_user(self) -> CanvaUser:
        """
        Get details of the current authenticated user.
        
        Returns:
            User information
        """
        response = await self.get("/users/me")
        
        return CanvaUser(
            id=response["id"],
            display_name=response["display_name"],
            email=response.get("email"),
            team_id=response.get("team_id"),
            created_at=datetime.fromisoformat(response["created_at"].replace("Z", "+00:00"))
        )
    
    async def get_user_profile(self) -> Dict[str, Any]:
        """
        Get the profile information of the current user.
        
        Returns:
            User profile information
        """
        return await self.get("/users/profile")
    
    async def get_user_capabilities(self) -> Dict[str, Any]:
        """
        Get the API capabilities for the user account.
        
        Returns:
            User capabilities information
        """
        return await self.get("/users/capabilities") 