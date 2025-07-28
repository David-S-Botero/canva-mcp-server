"""
Comment service for Canva API
Handles comment operations
"""

from typing import Dict, Any, Optional
from datetime import datetime

from .base_service import BaseService
from ..models.canva_types import CanvaConfig, CanvaComment

class CommentService(BaseService):
    """Service for handling comment operations"""
    
    async def create_comment_thread(
        self,
        design_id: str,
        content: str,
        page_id: Optional[str] = None
    ) -> CanvaComment:
        """
        Create a new comment thread on a design.
        
        Args:
            design_id: The ID of the design
            content: Comment content
            page_id: Optional page ID for the comment
            
        Returns:
            Created comment thread information
        """
        data = {"content": content}
        if page_id:
            data["page_id"] = page_id
        
        response = await self.post(f"/designs/{design_id}/comments", data=data)
        
        return CanvaComment(
            id=response["comment"]["id"],
            content=response["comment"]["content"],
            created_at=datetime.fromisoformat(response["comment"]["created_at"].replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(response["comment"]["updated_at"].replace("Z", "+00:00")),
            author_id=response["comment"]["author_id"],
            design_id=design_id,
            page_id=response["comment"].get("page_id"),
            parent_id=response["comment"].get("parent_id")
        )
    
    async def create_comment_reply(
        self,
        design_id: str,
        thread_id: str,
        content: str
    ) -> CanvaComment:
        """
        Reply to a comment on a design.
        
        Args:
            design_id: The ID of the design
            thread_id: The ID of the comment thread
            content: Reply content
            
        Returns:
            Created reply information
        """
        data = {"content": content}
        
        response = await self.post(f"/designs/{design_id}/comments/{thread_id}/replies", data=data)
        
        return CanvaComment(
            id=response["comment"]["id"],
            content=response["comment"]["content"],
            created_at=datetime.fromisoformat(response["comment"]["created_at"].replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(response["comment"]["updated_at"].replace("Z", "+00:00")),
            author_id=response["comment"]["author_id"],
            design_id=design_id,
            page_id=response["comment"].get("page_id"),
            parent_id=thread_id
        )
    
    async def get_comment_thread(self, design_id: str, thread_id: str) -> CanvaComment:
        """
        Get metadata for a comment thread.
        
        Args:
            design_id: The ID of the design
            thread_id: The ID of the comment thread
            
        Returns:
            Comment thread metadata
        """
        response = await self.get(f"/designs/{design_id}/comments/{thread_id}")
        
        return CanvaComment(
            id=response["comment"]["id"],
            content=response["comment"]["content"],
            created_at=datetime.fromisoformat(response["comment"]["created_at"].replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(response["comment"]["updated_at"].replace("Z", "+00:00")),
            author_id=response["comment"]["author_id"],
            design_id=design_id,
            page_id=response["comment"].get("page_id"),
            parent_id=response["comment"].get("parent_id")
        )
    
    async def list_comment_replies(
        self,
        design_id: str,
        thread_id: str,
        limit: int = 50,
        page_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List the replies to a comment on a design.
        
        Args:
            design_id: The ID of the design
            thread_id: The ID of the comment thread
            limit: Maximum number of replies to return
            page_token: Token for pagination
            
        Returns:
            List of comment replies
        """
        params = {"limit": limit}
        if page_token:
            params["page_token"] = page_token
        
        return await self.get(f"/designs/{design_id}/comments/{thread_id}/replies", params=params) 