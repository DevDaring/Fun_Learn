"""
Avatar and Character Models - Pydantic models for avatar and character management
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class CreationMethod(str, Enum):
    """Avatar/Character creation method options"""
    DRAW = "draw"
    UPLOAD = "upload"
    GALLERY = "gallery"
    AI_GENERATED = "ai_generated"


class AvatarStyle(str, Enum):
    """Avatar style options"""
    CARTOON = "cartoon"
    REALISTIC = "realistic"
    ANIME = "anime"
    PIXEL = "pixel"


class AvatarCreate(BaseModel):
    """Model for creating a new avatar"""
    name: str = Field(..., min_length=1, max_length=100)
    style: AvatarStyle = AvatarStyle.CARTOON
    creation_method: CreationMethod = CreationMethod.GALLERY
    source_image_data: Optional[str] = None  # Base64 encoded image or file path
    description: Optional[str] = Field(None, max_length=500)

    class Config:
        use_enum_values = True


class Avatar(BaseModel):
    """Complete avatar model"""
    avatar_id: str
    user_id: str
    name: str
    image_path: str
    image_url: Optional[str] = None
    creation_method: str
    style: str
    description: Optional[str] = None
    created_at: datetime
    is_active: bool = Field(default=True)

    class Config:
        from_attributes = True


class AvatarUpdate(BaseModel):
    """Model for updating avatar"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None


class AvatarDisplay(BaseModel):
    """Avatar information for display"""
    avatar_id: str
    name: str
    image_url: str
    style: str
    creation_method: str
    is_active: bool


class CharacterCreate(BaseModel):
    """Model for creating a new character"""
    name: str = Field(..., min_length=1, max_length=100)
    creation_method: CreationMethod = CreationMethod.GALLERY
    description: str = Field(..., min_length=1, max_length=500)
    source_image_data: Optional[str] = None  # Base64 encoded image or file path
    personality_traits: Optional[list[str]] = None
    role: Optional[str] = Field(None, max_length=100)  # e.g., "teacher", "companion", "guide"

    class Config:
        use_enum_values = True


class Character(BaseModel):
    """Complete character model"""
    character_id: str
    user_id: str
    name: str
    image_path: str
    image_url: Optional[str] = None
    creation_method: str
    description: str
    personality_traits: Optional[list[str]] = None
    role: Optional[str] = None
    created_at: datetime
    is_active: bool = Field(default=True)
    usage_count: int = Field(default=0, ge=0)

    class Config:
        from_attributes = True


class CharacterUpdate(BaseModel):
    """Model for updating character"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    personality_traits: Optional[list[str]] = None
    role: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None


class CharacterDisplay(BaseModel):
    """Character information for display"""
    character_id: str
    name: str
    image_url: str
    description: str
    role: Optional[str] = None
    is_active: bool
    usage_count: int


class DrawingData(BaseModel):
    """Model for canvas drawing data"""
    drawing_base64: str = Field(..., description="Base64 encoded image data from canvas")
    width: int = Field(default=512, ge=100, le=2048)
    height: int = Field(default=512, ge=100, le=2048)


class ImageUpload(BaseModel):
    """Model for image upload metadata"""
    filename: str
    content_type: str
    size_bytes: int
