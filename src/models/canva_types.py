"""
Canva-specific data types and models
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
from enum import Enum

class CanvaScope(str, Enum):
    """Canva API scopes"""
    ASSET_READ = "asset:read"
    ASSET_WRITE = "asset:write"
    DESIGN_META_READ = "design:meta:read"
    DESIGN_META_WRITE = "design:meta:write"
    FOLDER_READ = "folder:read"
    FOLDER_WRITE = "folder:write"
    COMMENT_WRITE = "comment:write"
    BRAND_TEMPLATE_READ = "brand_template:read"

class CanvaFileType(str, Enum):
    """Supported file types for export"""
    PDF = "pdf"
    JPG = "jpg"
    PNG = "png"
    GIF = "gif"
    PPTX = "pptx"
    MP4 = "mp4"

class CanvaJobStatus(str, Enum):
    """Job status values"""
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"

@dataclass
class CanvaConfig:
    """Configuration for Canva API integration"""
    client_id: str
    client_secret: str
    redirect_uri: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_expires_at: Optional[datetime] = None

@dataclass
class CanvaAuthResponse:
    """OAuth authentication response"""
    access_token: str
    token_type: str
    expires_in: int
    scope: str
    refresh_token: str

@dataclass
class CanvaDesign:
    """Canva design information"""
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    thumbnail_url: Optional[str] = None
    folder_id: Optional[str] = None
    brand_kit_id: Optional[str] = None

@dataclass
class CanvaAsset:
    """Canva asset information"""
    id: str
    title: str
    filename: str
    file_size: int
    mime_type: str
    created_at: datetime
    updated_at: datetime
    folder_id: Optional[str] = None
    tags: Optional[List[str]] = None

@dataclass
class CanvaFolder:
    """Canva folder information"""
    id: str
    name: str
    created_at: datetime
    updated_at: datetime
    parent_folder_id: Optional[str] = None
    item_count: Optional[int] = None

@dataclass
class CanvaUser:
    """Canva user information"""
    id: str
    display_name: str
    created_at: datetime
    email: Optional[str] = None
    team_id: Optional[str] = None

@dataclass
class CanvaBrandTemplate:
    """Canva brand template information"""
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    description: Optional[str] = None
    has_dataset: bool = False

@dataclass
class CanvaExportJob:
    """Canva export job information"""
    id: str
    status: CanvaJobStatus
    file_type: CanvaFileType
    created_at: datetime
    completed_at: Optional[datetime] = None
    download_url: Optional[str] = None
    error_message: Optional[str] = None

@dataclass
class CanvaUploadJob:
    """Canva upload job information"""
    id: str
    status: CanvaJobStatus
    filename: str
    file_size: int
    created_at: datetime
    completed_at: Optional[datetime] = None
    asset_id: Optional[str] = None
    error_message: Optional[str] = None

@dataclass
class CanvaAutofillJob:
    """Canva autofill job information"""
    id: str
    status: CanvaJobStatus
    brand_template_id: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    design_id: Optional[str] = None
    error_message: Optional[str] = None

@dataclass
class CanvaComment:
    """Canva comment information"""
    id: str
    content: str
    created_at: datetime
    updated_at: datetime
    author_id: str
    design_id: str
    page_id: Optional[str] = None
    parent_id: Optional[str] = None 