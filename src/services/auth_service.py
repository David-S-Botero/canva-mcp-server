"""
Authentication service for Canva API
Handles OAuth 2.0 flow and token management
"""

import base64
import hashlib
import secrets
import time
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

import httpx

from ..models.canva_types import CanvaConfig, CanvaAuthResponse, CanvaScope
from ..utils.logging import logger, log_oauth_flow, log_api_request

class AuthService:
    """Service for handling Canva API authentication"""
    
    def __init__(self, config: CanvaConfig):
        self.config = config
        self.api_base = "https://api.canva.com/rest/v1"
        self.auth_base = "https://www.canva.com/api/oauth"
    
    def generate_code_verifier(self) -> str:
        """Generate a code verifier for PKCE"""
        return base64.urlsafe_b64encode(secrets.token_bytes(96)).decode('utf-8').rstrip('=')
    
    def generate_code_challenge(self, code_verifier: str) -> str:
        """Generate a code challenge from code verifier"""
        sha256_hash = hashlib.sha256(code_verifier.encode('utf-8')).digest()
        return base64.urlsafe_b64encode(sha256_hash).decode('utf-8').rstrip('=')
    
    def generate_state(self) -> str:
        """Generate a state parameter for OAuth"""
        return base64.urlsafe_b64encode(secrets.token_bytes(96)).decode('utf-8').rstrip('=')
    
    def create_authorization_url(self, scopes: str = None) -> Dict[str, str]:
        """
        Create an OAuth authorization URL for Canva API access.
        
        Args:
            scopes: Space-separated list of scopes to request
            
        Returns:
            Dictionary containing authorization URL and code verifier
        """
        if not self.config.client_id:
            raise Exception("CANVA_CLIENT_ID not configured")
        
        if scopes is None:
            scopes = " ".join([
                CanvaScope.ASSET_READ.value,
                CanvaScope.ASSET_WRITE.value,
                CanvaScope.DESIGN_META_READ.value,
                CanvaScope.FOLDER_READ.value
            ])
        
        code_verifier = self.generate_code_verifier()
        code_challenge = self.generate_code_challenge(code_verifier)
        state = self.generate_state()
        
        auth_url = (
            f"{self.auth_base}/authorize?"
            f"code_challenge={code_challenge}&"
            f"code_challenge_method=s256&"
            f"scope={scopes}&"
            f"response_type=code&"
            f"client_id={self.config.client_id}&"
            f"state={state}&"
            f"redirect_uri={self.config.redirect_uri}"
        )
        
        log_oauth_flow("Authorization URL created", {
            "scopes": scopes,
            "state": state[:10] + "..."
        })
        
        return {
            "authorization_url": auth_url,
            "code_verifier": code_verifier,
            "state": state
        }
    
    async def exchange_code_for_token(self, authorization_code: str, code_verifier: str) -> CanvaAuthResponse:
        """
        Exchange authorization code for access token.
        
        Args:
            authorization_code: The authorization code received from Canva
            code_verifier: The code verifier used in the authorization request
            
        Returns:
            Token response with access_token, refresh_token, and expiry
        """
        if not self.config.client_id or not self.config.client_secret:
            raise Exception("CANVA_CLIENT_ID and CANVA_CLIENT_SECRET must be configured")
        
        credentials = base64.b64encode(
            f"{self.config.client_id}:{self.config.client_secret}".encode()
        ).decode()
        
        headers = {
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "authorization_code",
            "code_verifier": code_verifier,
            "code": authorization_code,
            "redirect_uri": self.config.redirect_uri
        }
        
        start_time = time.time()
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_base}/oauth/token",
                headers=headers,
                data=data
            )
            duration = time.time() - start_time
        
        log_api_request("POST", "/oauth/token", response.status_code, duration)
        
        if response.status_code >= 400:
            error_detail = response.json() if response.content else {}
            raise Exception(f"Token exchange failed: {response.status_code} - {error_detail}")
        
        response_data = response.json()
        
        # Update stored tokens
        self.config.access_token = response_data.get("access_token")
        self.config.refresh_token = response_data.get("refresh_token")
        self.config.token_expires_at = datetime.now() + timedelta(seconds=response_data.get("expires_in", 3600))
        
        log_oauth_flow("Token exchange successful", {
            "expires_in": response_data.get("expires_in"),
            "scope": response_data.get("scope")
        })
        
        return CanvaAuthResponse(
            access_token=response_data["access_token"],
            token_type=response_data["token_type"],
            expires_in=response_data["expires_in"],
            scope=response_data["scope"],
            refresh_token=response_data["refresh_token"]
        )
    
    async def refresh_access_token(self) -> CanvaAuthResponse:
        """
        Refresh the access token using the refresh token.
        
        Returns:
            New token response
        """
        if not self.config.refresh_token:
            raise Exception("No refresh token available")
        
        credentials = base64.b64encode(
            f"{self.config.client_id}:{self.config.client_secret}".encode()
        ).decode()
        
        headers = {
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.config.refresh_token
        }
        
        start_time = time.time()
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_base}/oauth/token",
                headers=headers,
                data=data
            )
            duration = time.time() - start_time
        
        log_api_request("POST", "/oauth/token", response.status_code, duration)
        
        if response.status_code >= 400:
            error_detail = response.json() if response.content else {}
            raise Exception(f"Token refresh failed: {response.status_code} - {error_detail}")
        
        response_data = response.json()
        
        # Update stored tokens
        self.config.access_token = response_data.get("access_token")
        self.config.refresh_token = response_data.get("refresh_token")
        self.config.token_expires_at = datetime.now() + timedelta(seconds=response_data.get("expires_in", 3600))
        
        log_oauth_flow("Token refresh successful", {
            "expires_in": response_data.get("expires_in")
        })
        
        return CanvaAuthResponse(
            access_token=response_data["access_token"],
            token_type=response_data["token_type"],
            expires_in=response_data["expires_in"],
            scope=response_data["scope"],
            refresh_token=response_data["refresh_token"]
        )
    
    def is_token_expired(self) -> bool:
        """Check if the current access token is expired"""
        if not self.config.token_expires_at:
            return True
        return datetime.now() >= self.config.token_expires_at
    
    def clear_tokens(self):
        """Clear stored access and refresh tokens"""
        self.config.access_token = None
        self.config.refresh_token = None
        self.config.token_expires_at = None
        log_oauth_flow("Tokens cleared")
    
    def get_auth_headers(self) -> Dict[str, str]:
        """Get headers with authentication token"""
        if not self.config.access_token:
            raise Exception("No access token available")
        
        return {
            "Authorization": f"Bearer {self.config.access_token}",
            "Content-Type": "application/json"
        } 