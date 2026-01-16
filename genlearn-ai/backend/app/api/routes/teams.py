"""
Team Routes - Team management
"""

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from datetime import datetime

from app.api.dependencies import get_current_user
from app.database.csv_handler import CSVHandler
from app.models.team import Team, TeamMember
from app.utils.helpers import generate_unique_id

router = APIRouter()


class TeamCreateRequest(BaseModel):
    """Request to create a team"""
    name: str


@router.get("/list", response_model=list[Team], status_code=status.HTTP_200_OK)
async def get_teams(current_user: dict = Depends(get_current_user)):
    """
    Get list of all teams

    Args:
        current_user: Authenticated user

    Returns:
        List of teams with members
    """
    csv_handler = CSVHandler()

    try:
        # Get all teams
        all_teams = csv_handler.read_all("teams")

        # Get all team members
        all_members = csv_handler.read_all("team_members")

        # Get all users for display names
        all_users = csv_handler.read_all("users")
        user_map = {u["user_id"]: u for u in all_users}

        # Build team data with members
        teams_with_members = []
        for team in all_teams:
            team_id = team["team_id"]

            # Get members for this team
            team_members = [
                m for m in all_members
                if m.get("team_id") == team_id
            ]

            # Format members
            members = []
            for member in team_members:
                user = user_map.get(member["user_id"], {})
                members.append({
                    "user_id": member["user_id"],
                    "display_name": user.get("display_name", "Unknown"),
                    "role": member.get("role", "member"),
                    "avatar_url": f"/media/avatars/{user.get('avatar_id')}.png" if user.get("avatar_id") else None
                })

            teams_with_members.append({
                **team,
                "members": members
            })

        return teams_with_members

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching teams: {str(e)}"
        )


@router.post("/create", response_model=Team, status_code=status.HTTP_201_CREATED)
async def create_team(
    team_request: TeamCreateRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new team

    Args:
        team_request: Team creation data
        current_user: Authenticated user

    Returns:
        Created team data
    """
    csv_handler = CSVHandler()

    try:
        # Generate team ID
        team_id = generate_unique_id("TM")

        # Create team record
        team_data = {
            "team_id": team_id,
            "team_name": team_request.name,
            "created_by": current_user["user_id"],
            "tournament_id": "",
            "total_score": 0,
            "rank": 0,
            "created_at": datetime.now().isoformat()
        }

        csv_handler.create("teams", team_data)

        # Add creator as team leader
        membership_data = {
            "membership_id": f"{team_id}_{current_user['user_id']}",
            "team_id": team_id,
            "user_id": current_user["user_id"],
            "role": "leader",
            "joined_at": datetime.now().isoformat()
        }

        csv_handler.create("team_members", membership_data)

        # Return team with leader as member
        return {
            **team_data,
            "members": [{
                "user_id": current_user["user_id"],
                "display_name": current_user.get("display_name", "Unknown"),
                "role": "leader",
                "avatar_url": f"/media/avatars/{current_user.get('avatar_id')}.png" if current_user.get("avatar_id") else None
            }]
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating team: {str(e)}"
        )


@router.post("/{team_id}/join", status_code=status.HTTP_200_OK)
async def join_team(
    team_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Join an existing team

    Args:
        team_id: Team identifier
        current_user: Authenticated user

    Returns:
        Success message
    """
    csv_handler = CSVHandler()

    try:
        # Get team
        team = csv_handler.read_by_id("teams", team_id, "team_id")
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )

        # Check if user is already a member
        all_members = csv_handler.read_all("team_members")
        is_member = any(
            m.get("team_id") == team_id and m.get("user_id") == current_user["user_id"]
            for m in all_members
        )

        if is_member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already a member of this team"
            )

        # Add user to team
        membership_data = {
            "membership_id": f"{team_id}_{current_user['user_id']}",
            "team_id": team_id,
            "user_id": current_user["user_id"],
            "role": "member",
            "joined_at": datetime.now().isoformat()
        }

        csv_handler.create("team_members", membership_data)

        return {
            "message": "Successfully joined team",
            "team_id": team_id,
            "team_name": team.get("team_name")
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error joining team: {str(e)}"
        )


@router.get("/{team_id}", response_model=Team, status_code=status.HTTP_200_OK)
async def get_team(
    team_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get team details

    Args:
        team_id: Team identifier
        current_user: Authenticated user

    Returns:
        Team data with members
    """
    csv_handler = CSVHandler()

    try:
        # Get team
        team = csv_handler.read_by_id("teams", team_id, "team_id")
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )

        # Get team members
        all_members = csv_handler.read_all("team_members")
        team_members = [
            m for m in all_members
            if m.get("team_id") == team_id
        ]

        # Get all users for display names
        all_users = csv_handler.read_all("users")
        user_map = {u["user_id"]: u for u in all_users}

        # Format members
        members = []
        for member in team_members:
            user = user_map.get(member["user_id"], {})
            members.append({
                "user_id": member["user_id"],
                "display_name": user.get("display_name", "Unknown"),
                "role": member.get("role", "member"),
                "avatar_url": f"/media/avatars/{user.get('avatar_id')}.png" if user.get("avatar_id") else None
            })

        return {
            **team,
            "members": members
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching team: {str(e)}"
        )
