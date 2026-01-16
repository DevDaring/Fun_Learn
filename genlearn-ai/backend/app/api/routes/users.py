"""
User Routes - Profile, settings, and history management
"""

from fastapi import APIRouter, HTTPException, status, Depends

from app.api.dependencies import get_current_user
from app.database.csv_handler import CSVHandler
from app.models.user import User, UserUpdate, UserSettings
from app.models.session import LearningHistory

router = APIRouter()


@router.get("/profile", response_model=User, status_code=status.HTTP_200_OK)
async def get_profile(current_user: dict = Depends(get_current_user)):
    """
    Get current user's profile

    Args:
        current_user: Authenticated user

    Returns:
        User profile data
    """
    try:
        user_data = {k: v for k, v in current_user.items() if k != "password_hash"}
        return user_data

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching profile: {str(e)}"
        )


@router.put("/profile", response_model=User, status_code=status.HTTP_200_OK)
async def update_profile(
    profile_update: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update current user's profile

    Args:
        profile_update: Profile fields to update
        current_user: Authenticated user

    Returns:
        Updated user data
    """
    csv_handler = CSVHandler()

    try:
        # Get current user data
        user_id = current_user["user_id"]

        # Update only provided fields
        update_data = profile_update.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            current_user[key] = value

        # Save to database
        csv_handler.update("users", user_id, current_user, "user_id")

        # Return updated user without password hash
        user_data = {k: v for k, v in current_user.items() if k != "password_hash"}
        return user_data

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating profile: {str(e)}"
        )


@router.get("/history", response_model=list[LearningHistory], status_code=status.HTTP_200_OK)
async def get_learning_history(
    limit: int = 50,
    offset: int = 0,
    current_user: dict = Depends(get_current_user)
):
    """
    Get user's learning history

    Args:
        limit: Maximum number of records to return
        offset: Number of records to skip
        current_user: Authenticated user

    Returns:
        List of learning history entries
    """
    csv_handler = CSVHandler()

    try:
        user_id = current_user["user_id"]

        # Get all history records
        all_history = csv_handler.read_all("learning_history")

        # Filter by user and sort by viewed_at (most recent first)
        user_history = [
            h for h in all_history
            if h.get("user_id") == user_id
        ]

        # Sort by viewed_at descending
        user_history.sort(
            key=lambda x: x.get("viewed_at", ""),
            reverse=True
        )

        # Apply pagination
        paginated_history = user_history[offset:offset + limit]

        return paginated_history

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching learning history: {str(e)}"
        )


@router.put("/settings", response_model=UserSettings, status_code=status.HTTP_200_OK)
async def update_settings(
    settings_update: UserSettings,
    current_user: dict = Depends(get_current_user)
):
    """
    Update user settings

    Args:
        settings_update: New settings values
        current_user: Authenticated user

    Returns:
        Updated settings
    """
    csv_handler = CSVHandler()

    try:
        user_id = current_user["user_id"]

        # Update user settings fields
        current_user["language_preference"] = settings_update.language_preference
        current_user["voice_preference"] = settings_update.voice_preference
        current_user["full_vocal_mode"] = settings_update.full_vocal_mode

        # Save to database
        csv_handler.update("users", user_id, current_user, "user_id")

        return settings_update

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating settings: {str(e)}"
        )
