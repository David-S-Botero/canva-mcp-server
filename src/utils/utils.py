import base64
import hashlib
import secrets
from typing import Optional, Dict, Any
import httpx

from src.utils.config import canva_config 

def generate_code_verifier() -> str:
    """Generate a code verifier for PKCE"""
    return base64.urlsafe_b64encode(secrets.token_bytes(96)).decode('utf-8').rstrip('=')

def generate_code_challenge(code_verifier: str) -> str:
    """Generate a code challenge from code verifier"""
    sha256_hash = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(sha256_hash).decode('utf-8').rstrip('=')

def generate_state() -> str:
    """Generate a state parameter for OAuth"""
    return base64.urlsafe_b64encode(secrets.token_bytes(96)).decode('utf-8').rstrip('=')

async def make_canva_request(
    method: str, 
    endpoint: str, 
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Make a request to the Canva API"""
    if headers is None:
        headers = {}
    
    if canva_config.access_token:
        headers['Authorization'] = f'Bearer {canva_config.access_token}'
    
    url = f"{canva_config.api_base}{endpoint}"
    
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=method,
            url=url,
            headers=headers,
            json=data if data else None,
            params=params
        )
        
        if response.status_code >= 400:
            error_detail = response.json() if response.content else {}
            raise Exception(f"Canva API error: {response.status_code} - {error_detail}")
        
        return response.json() if response.content else {}
