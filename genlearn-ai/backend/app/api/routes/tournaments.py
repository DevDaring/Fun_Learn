"""
Tournament Routes - Tournament management and leaderboards
"""

from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
from pydantic import BaseModel

from app.api.dependencies import get_current_user
from app.database.csv_handler import CSVHandler
from app.models.tournament import Tournament

router = APIRouter()


class TournamentJoinRequest(BaseModel):
    """Request to join a tournament"""
    team_id: Optional[str] = None


class LeaderboardEntry(BaseModel):
    """Leaderboard entry model"""
    rank: int
    user_id: Optional[str] = None
    team_id: Optional[str] = None
    display_name: str
    score: int
    avatar_url: Optional[str] = None


@router.get("/list", response_model=list[Tournament], status_code=status.HTTP_200_OK)
async def get_tournaments(
    status_filter: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Get list of tournaments

    Args:
        status_filter: Filter by status (upcoming/active/completed)
        current_user: Authenticated user

    Returns:
        List of tournaments
    """
    csv_handler = CSVHandler()

    try:
        # Get all tournaments
        all_tournaments = csv_handler.read_all("tournaments")

        # Filter by status if provided
        if status_filter:
            all_tournaments = [
                t for t in all_tournaments
                if t.get("status") == status_filter
            ]

        # Count participants for each tournament
        all_sessions = csv_handler.read_all("sessions")
        for tournament in all_tournaments:
            tournament_sessions = [
                s for s in all_sessions
                if s.get("tournament_id") == tournament["tournament_id"]
            ]
            # Get unique participants
            participants = set(s.get("user_id") for s in tournament_sessions)
            tournament["current_participants"] = len(participants)

        return all_tournaments

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching tournaments: {str(e)}"
        )


@router.post("/{tournament_id}/join", status_code=status.HTTP_200_OK)
async def join_tournament(
    tournament_id: str,
    join_request: TournamentJoinRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Join a tournament

    Args:
        tournament_id: Tournament identifier
        join_request: Team information (optional)
        current_user: Authenticated user

    Returns:
        Success message
    """
    csv_handler = CSVHandler()

    try:
        # Get tournament
        tournament = csv_handler.read_by_id("tournaments", tournament_id, "tournament_id")
        if not tournament:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tournament not found"
            )

        # Check if tournament is active
        if tournament.get("status") != "active":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tournament is not active"
            )

        # Check if user already joined
        all_sessions = csv_handler.read_all("sessions")
        user_tournament_sessions = [
            s for s in all_sessions
            if s.get("tournament_id") == tournament_id and s.get("user_id") == current_user["user_id"]
        ]

        if user_tournament_sessions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already joined this tournament"
            )

        # If team_id provided, verify team exists
        if join_request.team_id:
            team = csv_handler.read_by_id("teams", join_request.team_id, "team_id")
            if not team:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Team not found"
                )

            # Check if user is member of this team
            all_members = csv_handler.read_all("team_members")
            is_member = any(
                m.get("team_id") == join_request.team_id and m.get("user_id") == current_user["user_id"]
                for m in all_members
            )

            if not is_member:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not a member of this team"
                )

        return {
            "message": "Successfully joined tournament",
            "tournament_id": tournament_id,
            "team_id": join_request.team_id
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error joining tournament: {str(e)}"
        )


@router.get("/leaderboard", response_model=list[LeaderboardEntry], status_code=status.HTTP_200_OK)
async def get_leaderboard(
    scope: str = "global",
    tournament_id: Optional[str] = None,
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    """
    Get leaderboard

    Args:
        scope: Leaderboard scope (global/tournament)
        tournament_id: Tournament ID if scope is tournament
        limit: Maximum number of entries
        current_user: Authenticated user

    Returns:
        Leaderboard entries
    """
    csv_handler = CSVHandler()

    try:
        if scope == "tournament":
            if not tournament_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Tournament ID required for tournament leaderboard"
                )

            # Get tournament sessions
            all_sessions = csv_handler.read_all("sessions")
            tournament_sessions = [
                s for s in all_sessions
                if s.get("tournament_id") == tournament_id
            ]

            # Aggregate scores by user
            user_scores = {}
            for session in tournament_sessions:
                user_id = session.get("user_id")
                score = int(session.get("score", 0))
                if user_id in user_scores:
                    user_scores[user_id] += score
                else:
                    user_scores[user_id] = score

            # Get user details
            all_users = csv_handler.read_all("users")
            user_map = {u["user_id"]: u for u in all_users}

            # Create leaderboard entries
            leaderboard = []
            for user_id, score in user_scores.items():
                user = user_map.get(user_id, {})
                leaderboard.append({
                    "user_id": user_id,
                    "display_name": user.get("display_name", "Unknown"),
                    "score": score,
                    "avatar_url": f"/media/avatars/{user.get('avatar_id')}.png" if user.get("avatar_id") else None
                })

            # Sort by score descending
            leaderboard.sort(key=lambda x: x["score"], reverse=True)

            # Add ranks
            for idx, entry in enumerate(leaderboard[:limit]):
                entry["rank"] = idx + 1

            return leaderboard[:limit]

        else:  # global leaderboard
            # Get all users sorted by XP
            all_users = csv_handler.read_all("users")

            # Sort by XP points descending
            sorted_users = sorted(
                all_users,
                key=lambda u: int(u.get("xp_points", 0)),
                reverse=True
            )

            # Create leaderboard entries
            leaderboard = []
            for idx, user in enumerate(sorted_users[:limit]):
                leaderboard.append({
                    "rank": idx + 1,
                    "user_id": user["user_id"],
                    "display_name": user.get("display_name", "Unknown"),
                    "score": int(user.get("xp_points", 0)),
                    "avatar_url": f"/media/avatars/{user.get('avatar_id')}.png" if user.get("avatar_id") else None
                })

            return leaderboard

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching leaderboard: {str(e)}"
        )
