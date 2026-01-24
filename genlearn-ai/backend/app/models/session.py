"""
Learning Session Models - Pydantic models for learning sessions
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class PlayMode(str, Enum):
    """Play mode options"""
    SOLO = "solo"
    TEAM = "team"
    TOURNAMENT = "tournament"


class SessionStatus(str, Enum):
    """Session status options"""
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class VisualStyle(str, Enum):
    """Visual style options"""
    CARTOON = "cartoon"
    REALISTIC = "realistic"


class StoryStyle(str, Enum):
    """Story narrative style options"""
    THRILLER = "thriller"
    FUN = "fun"
    NOSTALGIC = "nostalgic"
    ADVENTURE = "adventure"
    MYSTERY = "mystery"
    SCIFI = "scifi"


class SessionCreate(BaseModel):
    """Model for creating a new learning session"""
    topic: str = Field(..., min_length=1, max_length=200)
    difficulty_level: int = Field(..., ge=1, le=10)
    duration_minutes: int = Field(..., ge=5, le=120)
    visual_style: VisualStyle = VisualStyle.CARTOON
    story_style: StoryStyle = StoryStyle.FUN
    play_mode: PlayMode = PlayMode.SOLO
    team_id: Optional[str] = None
    tournament_id: Optional[str] = None
    avatar_id: Optional[str] = None
    character_ids: Optional[list[str]] = None

    class Config:
        use_enum_values = True


class LearningSession(BaseModel):
    """Complete learning session model"""
    session_id: str
    user_id: str
    topic: str
    difficulty_level: int = Field(ge=1, le=10)
    duration_minutes: int = Field(ge=5, le=120)
    visual_style: str
    story_style: str = "fun"
    play_mode: str
    avatar_id: Optional[str] = None
    character_ids: Optional[list[str]] = None
    team_id: Optional[str] = None
    tournament_id: Optional[str] = None
    status: str = "in_progress"
    current_cycle: int = Field(default=0, ge=0)
    total_cycles: int = Field(default=3, ge=1)
    score: int = Field(default=0, ge=0)
    started_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SessionProgress(BaseModel):
    """Model for updating session progress"""
    current_cycle: int = Field(..., ge=0)
    score: Optional[int] = Field(None, ge=0)
    time_spent_seconds: Optional[int] = Field(None, ge=0)


class SessionEnd(BaseModel):
    """Model for ending a session"""
    final_score: int = Field(..., ge=0)
    total_time_seconds: int = Field(..., ge=0)
    completed: bool = True


class TextOverlay(BaseModel):
    """Text to overlay on scene image"""
    text: str
    position: str = "bottom"  # "top", "center", "bottom"
    style: str = "caption"  # "speech_bubble", "caption", "dramatic"


class QuizOption(BaseModel):
    """Single quiz option"""
    key: str  # A, B, C, D
    text: str
    is_correct: bool = False


class QuizQuestion(BaseModel):
    """Quiz question with options"""
    question_id: str
    question_text: str
    options: list[QuizOption]
    correct_answers: list[str]  # List of correct option keys
    explanation: str
    is_multi_select: bool = False
    points: int = 10


class StorySegment(BaseModel):
    """Story segment within a learning session"""
    segment_number: int = Field(..., ge=1)
    narrative: str
    facts: list[str] = []
    image_prompt: str
    image_url: Optional[str] = None
    audio_url: Optional[str] = None


class EnhancedStorySegment(BaseModel):
    """Enhanced story segment with text overlay and quiz"""
    segment_number: int = Field(..., ge=1)
    narrative: str
    scene_description: str
    scene_image_url: Optional[str] = None
    text_overlay: TextOverlay
    audio_url: Optional[str] = None
    quiz: QuizQuestion


class SessionContent(BaseModel):
    """Complete content for a learning session"""
    session_id: str
    topic: str
    story_segments: list[StorySegment]
    topic_summary: str
    total_cycles: int


class SessionSummary(BaseModel):
    """Summary of a completed session"""
    session_id: str
    topic: str
    difficulty_level: int
    duration_minutes: int
    score: int
    total_questions: int
    correct_answers: int
    accuracy_rate: float
    xp_earned: int
    time_spent_seconds: int
    completed_at: datetime


class LearningHistory(BaseModel):
    """Learning history entry"""
    history_id: str
    user_id: str
    session_id: str
    content_type: str  # 'image', 'video', 'quiz'
    content_id: str
    content_path: Optional[str] = None
    topic: str
    viewed_at: datetime

    class Config:
        from_attributes = True
