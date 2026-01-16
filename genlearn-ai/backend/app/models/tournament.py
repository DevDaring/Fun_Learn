"""
Tournament Models - Pydantic models for tournament management
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class TournamentStatus(str, Enum):
    """Tournament status options"""
    UPCOMING = "upcoming"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class EntryType(str, Enum):
    """Tournament entry type options"""
    FREE = "free"
    INVITE_ONLY = "invite_only"


class TournamentCreate(BaseModel):
    """Model for creating a new tournament"""
    name: str = Field(..., min_length=3, max_length=100)
    topic: str = Field(..., min_length=1, max_length=200)
    difficulty_level: int = Field(..., ge=1, le=10)
    start_datetime: datetime
    end_datetime: datetime
    duration_minutes: int = Field(..., ge=10, le=180)
    max_participants: int = Field(default=100, ge=1, le=1000)
    team_size_min: int = Field(default=1, ge=1, le=10)
    team_size_max: int = Field(default=5, ge=1, le=10)
    entry_type: EntryType = EntryType.FREE
    prize_1st: Optional[str] = None
    prize_2nd: Optional[str] = None
    prize_3rd: Optional[str] = None
    description: Optional[str] = None
    rules: Optional[str] = None

    class Config:
        use_enum_values = True


class TournamentUpdate(BaseModel):
    """Model for updating tournament information"""
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
    max_participants: Optional[int] = Field(None, ge=1, le=1000)
    status: Optional[TournamentStatus] = None
    prize_1st: Optional[str] = None
    prize_2nd: Optional[str] = None
    prize_3rd: Optional[str] = None
    description: Optional[str] = None
    rules: Optional[str] = None


class Tournament(BaseModel):
    """Complete tournament model"""
    tournament_id: str
    name: str
    topic: str
    difficulty_level: int = Field(ge=1, le=10)
    start_datetime: datetime
    end_datetime: datetime
    duration_minutes: int
    max_participants: int
    current_participants: int = 0
    team_size_min: int
    team_size_max: int
    entry_type: str
    status: str = "upcoming"
    prize_1st: Optional[str] = None
    prize_2nd: Optional[str] = None
    prize_3rd: Optional[str] = None
    description: Optional[str] = None
    rules: Optional[str] = None
    created_by: str
    created_at: datetime

    class Config:
        from_attributes = True


class TournamentParticipant(BaseModel):
    """Tournament participant information"""
    tournament_id: str
    user_id: str
    team_id: Optional[str] = None
    joined_at: datetime
    score: int = 0
    rank: Optional[int] = None


class TournamentJoin(BaseModel):
    """Model for joining a tournament"""
    team_id: Optional[str] = None


class TournamentLeaderboard(BaseModel):
    """Tournament leaderboard entry"""
    rank: int
    participant_id: str  # user_id or team_id
    participant_name: str
    participant_type: str  # 'user' or 'team'
    score: int
    sessions_completed: int
    avatar_url: Optional[str] = None


class TournamentResults(BaseModel):
    """Final tournament results"""
    tournament_id: str
    tournament_name: str
    topic: str
    total_participants: int
    leaderboard: list[TournamentLeaderboard]
    winners: dict[str, TournamentLeaderboard] = {}  # '1st', '2nd', '3rd'
    completed_at: datetime


class TournamentStats(BaseModel):
    """Tournament statistics"""
    tournament_id: str
    total_participants: int
    active_participants: int
    completed_sessions: int
    average_score: float
    highest_score: int
    lowest_score: int
