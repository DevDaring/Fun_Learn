"""
User Models - Pydantic models for user data
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user model with common fields"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    display_name: str = Field(..., min_length=1, max_length=100)
    language_preference: str = Field(default="en", max_length=10)
    voice_preference: str = Field(default="female", pattern="^(male|female)$")
    full_vocal_mode: bool = Field(default=False)


class UserCreate(UserBase):
    """Model for creating a new user"""
    password: str = Field(..., min_length=8, max_length=100)
    role: str = Field(default="user", pattern="^(admin|user)$")


class UserUpdate(BaseModel):
    """Model for updating user information"""
    email: Optional[EmailStr] = None
    display_name: Optional[str] = Field(None, min_length=1, max_length=100)
    avatar_id: Optional[str] = None
    language_preference: Optional[str] = Field(None, max_length=10)
    voice_preference: Optional[str] = Field(None, pattern="^(male|female)$")
    full_vocal_mode: Optional[bool] = None


class UserPasswordUpdate(BaseModel):
    """Model for updating user password"""
    current_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8, max_length=100)


class User(UserBase):
    """Complete user model"""
    user_id: str
    role: str
    avatar_id: Optional[str] = None
    xp_points: int = Field(default=0, ge=0)
    level: int = Field(default=1, ge=1, le=100)
    streak_days: int = Field(default=0, ge=0)
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserProfile(BaseModel):
    """User profile for public display"""
    user_id: str
    username: str
    display_name: str
    avatar_id: Optional[str] = None
    xp_points: int
    level: int
    streak_days: int


class UserStats(BaseModel):
    """User statistics"""
    user_id: str
    total_sessions: int = 0
    completed_sessions: int = 0
    total_questions_answered: int = 0
    correct_answers: int = 0
    accuracy_rate: float = 0.0
    total_time_minutes: int = 0
    favorite_topics: list[str] = []
    current_streak: int = 0
    longest_streak: int = 0
    xp_points: int = 0
    level: int = 1


class UserSettings(BaseModel):
    """User preferences and settings"""
    language_preference: str = "en"
    voice_preference: str = "female"
    full_vocal_mode: bool = False
    notifications_enabled: bool = True
    sound_enabled: bool = True
    auto_play_videos: bool = True
    theme: str = "light"
