"""
Team Models - Pydantic models for team management
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class MemberRole(str, Enum):
    """Team member role options"""
    LEADER = "leader"
    MEMBER = "member"


class TeamCreate(BaseModel):
    """Model for creating a new team"""
    team_name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    max_members: int = Field(default=5, ge=2, le=10)
    is_private: bool = Field(default=False)


class TeamUpdate(BaseModel):
    """Model for updating team information"""
    team_name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    max_members: Optional[int] = Field(None, ge=2, le=10)
    is_private: Optional[bool] = None


class Team(BaseModel):
    """Complete team model"""
    team_id: str
    team_name: str
    created_by: str
    tournament_id: Optional[str] = None
    total_score: int = Field(default=0, ge=0)
    rank: Optional[int] = None
    description: Optional[str] = None
    max_members: int = Field(default=5)
    current_members: int = Field(default=1)
    is_private: bool = Field(default=False)
    created_at: datetime

    class Config:
        from_attributes = True


class TeamMemberBase(BaseModel):
    """Base team member model"""
    team_id: str
    user_id: str
    role: MemberRole = MemberRole.MEMBER

    class Config:
        use_enum_values = True


class TeamMemberCreate(TeamMemberBase):
    """Model for adding team member"""
    pass


class TeamMember(TeamMemberBase):
    """Complete team member model"""
    membership_id: str
    joined_at: datetime

    class Config:
        from_attributes = True


class TeamMemberInfo(BaseModel):
    """Team member information with user details"""
    membership_id: str
    user_id: str
    username: str
    display_name: str
    role: str
    avatar_id: Optional[str] = None
    xp_points: int
    level: int
    joined_at: datetime


class TeamInvite(BaseModel):
    """Model for team invitation"""
    team_id: str
    invited_user_id: str
    message: Optional[str] = None


class TeamJoinRequest(BaseModel):
    """Model for requesting to join a team"""
    team_id: str
    message: Optional[str] = None


class TeamDetails(BaseModel):
    """Detailed team information"""
    team_id: str
    team_name: str
    created_by: str
    tournament_id: Optional[str] = None
    total_score: int
    rank: Optional[int] = None
    description: Optional[str] = None
    max_members: int
    current_members: int
    is_private: bool
    created_at: datetime
    members: list[TeamMemberInfo] = []
    leader: Optional[TeamMemberInfo] = None


class TeamStats(BaseModel):
    """Team statistics"""
    team_id: str
    team_name: str
    total_score: int
    total_sessions: int
    completed_sessions: int
    average_score_per_session: float
    total_members: int
    active_members: int
    total_xp: int
    rank: Optional[int] = None


class TeamLeaderboard(BaseModel):
    """Team leaderboard entry"""
    rank: int
    team_id: str
    team_name: str
    total_score: int
    members_count: int
    average_score: float
    sessions_completed: int
    leader_name: str
