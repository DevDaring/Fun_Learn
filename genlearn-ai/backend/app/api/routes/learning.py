"""
Learning Routes - Session management and content delivery
"""

import logging
from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
from typing import Optional

from app.api.dependencies import get_current_user
from app.database.csv_handler import CSVHandler
from app.database.file_handler import FileHandler
from app.models.session import (
    SessionCreate,
    LearningSession,
    SessionContent,
    SessionProgress,
    SessionEnd,
    SessionSummary,
    StorySegment
)
from app.services.content_generator import ContentGenerator
from app.utils.helpers import generate_unique_id
from app.utils.error_handler import handle_error, ErrorMessages

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/start", response_model=LearningSession, status_code=status.HTTP_201_CREATED)
async def start_learning_session(
    session_config: SessionCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Start a new learning session

    Args:
        session_config: Session configuration (topic, difficulty, etc.)
        current_user: Authenticated user

    Returns:
        Created learning session data
    """
    csv_handler = CSVHandler()
    content_generator = ContentGenerator()

    try:
        # Generate session ID
        session_id = generate_unique_id("SES")
        user_id = current_user["user_id"]

        # Calculate number of cycles based on duration
        # Rule: 5 minutes = 1 cycle, 15 minutes = 3 cycles, etc.
        total_cycles = max(1, session_config.duration_minutes // 5)

        # Create session record
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "topic": session_config.topic,
            "difficulty_level": session_config.difficulty_level,
            "duration_minutes": session_config.duration_minutes,
            "visual_style": session_config.visual_style,
            "play_mode": session_config.play_mode,
            "team_id": session_config.team_id or "",
            "tournament_id": session_config.tournament_id or "",
            "status": "in_progress",
            "current_cycle": 0,
            "total_cycles": total_cycles,
            "score": 0,
            "started_at": datetime.now().isoformat(),
            "completed_at": ""
        }

        # Save session to database
        csv_handler.create("sessions", session_data)

        return session_data

    except HTTPException:
        raise
    except Exception as e:
        raise handle_error(
            e,
            "starting learning session",
            public_message=ErrorMessages.SESSION_ERROR,
            log_context={"user_id": current_user.get("user_id")}
        )


@router.get("/session/{session_id}/content", response_model=SessionContent, status_code=status.HTTP_200_OK)
async def get_session_content(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get learning content for a session

    Args:
        session_id: Session identifier
        current_user: Authenticated user

    Returns:
        Generated learning content with story segments and images
    """
    csv_handler = CSVHandler()
    content_generator = ContentGenerator()
    file_handler = FileHandler()

    try:
        # Get session
        session = csv_handler.read_by_id("sessions", session_id, "session_id")
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )

        # Verify user owns this session
        if session.get("user_id") != current_user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this session"
            )

        # Get user's avatar and characters if available
        avatar_description = None
        if current_user.get("avatar_id"):
            avatar = csv_handler.read_by_id("avatars", current_user["avatar_id"], "avatar_id")
            if avatar:
                avatar_description = avatar.get("name", "")

        character_descriptions = []
        characters = csv_handler.read_all("characters")
        user_characters = [c for c in characters if c.get("user_id") == current_user["user_id"]]
        character_descriptions = [c.get("description", c.get("name", "")) for c in user_characters[:3]]

        # Generate content
        content = await content_generator.generate_learning_content(
            topic=session["topic"],
            difficulty_level=session["difficulty_level"],
            visual_style=session["visual_style"],
            num_segments=session["total_cycles"],
            avatar_description=avatar_description,
            character_descriptions=character_descriptions if character_descriptions else None
        )

        # Save images and create URLs
        story_segments = []
        for idx, segment in enumerate(content["story_segments"]):
            # Generate image
            image_data = await content_generator.generate_image(
                prompt=segment["image_prompt"],
                style=session["visual_style"]
            )

            # Save image
            image_filename = f"ses_{session_id}_img_{idx + 1}.png"
            image_path = file_handler.save_image(
                image_data,
                "generated_images",
                image_filename
            )

            # Create history record
            history_data = {
                "history_id": generate_unique_id("HIS"),
                "user_id": current_user["user_id"],
                "session_id": session_id,
                "content_type": "image",
                "content_id": f"IMG{idx + 1:03d}",
                "content_path": image_path,
                "topic": session["topic"],
                "viewed_at": datetime.now().isoformat()
            }
            csv_handler.create("learning_history", history_data)

            # Create story segment with image URL
            story_segments.append({
                "segment_number": segment["segment_number"],
                "narrative": segment["narrative"],
                "facts": segment["facts"],
                "image_prompt": segment["image_prompt"],
                "image_url": f"/media/{image_path}",
                "audio_url": None  # Will be generated on demand
            })

        return {
            "session_id": session_id,
            "topic": session["topic"],
            "story_segments": story_segments,
            "topic_summary": content.get("topic_summary", ""),
            "total_cycles": session["total_cycles"]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise handle_error(
            e,
            "generating content",
            public_message=ErrorMessages.CONTENT_GENERATION_ERROR,
            log_context={"session_id": session_id}
        )


@router.post("/session/{session_id}/progress", status_code=status.HTTP_200_OK)
async def update_session_progress(
    session_id: str,
    progress: SessionProgress,
    current_user: dict = Depends(get_current_user)
):
    """
    Update session progress

    Args:
        session_id: Session identifier
        progress: Progress update data
        current_user: Authenticated user

    Returns:
        Success message
    """
    csv_handler = CSVHandler()

    try:
        # Get session
        session = csv_handler.read_by_id("sessions", session_id, "session_id")
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )

        # Verify user owns this session
        if session.get("user_id") != current_user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this session"
            )

        # Update progress
        session["current_cycle"] = progress.current_cycle
        if progress.score is not None:
            session["score"] = progress.score

        # Save to database
        csv_handler.update("sessions", session_id, session, "session_id")

        return {"message": "Progress updated successfully", "session": session}

    except HTTPException:
        raise
    except Exception as e:
        raise handle_error(
            e,
            "updating session progress",
            public_message=ErrorMessages.SESSION_ERROR,
            log_context={"session_id": session_id}
        )


@router.post("/session/{session_id}/end", response_model=SessionSummary, status_code=status.HTTP_200_OK)
async def end_learning_session(
    session_id: str,
    session_end: SessionEnd,
    current_user: dict = Depends(get_current_user)
):
    """
    End a learning session and calculate final results

    Args:
        session_id: Session identifier
        session_end: Final session data
        current_user: Authenticated user

    Returns:
        Session summary with statistics
    """
    csv_handler = CSVHandler()

    try:
        # Get session
        session = csv_handler.read_by_id("sessions", session_id, "session_id")
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )

        # Verify user owns this session
        if session.get("user_id") != current_user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this session"
            )

        # Update session
        session["status"] = "completed" if session_end.completed else "abandoned"
        session["score"] = session_end.final_score
        session["completed_at"] = datetime.now().isoformat()

        csv_handler.update("sessions", session_id, session, "session_id")

        # Get all answers for this session
        all_scores = csv_handler.read_all("scores")
        session_scores = [s for s in all_scores if s.get("session_id") == session_id]

        total_questions = len(session_scores)
        correct_answers = sum(1 for s in session_scores if s.get("is_correct") == "true")
        accuracy_rate = (correct_answers / total_questions * 100) if total_questions > 0 else 0.0

        # Calculate XP earned (base on score and difficulty)
        xp_earned = session_end.final_score * session["difficulty_level"]

        # Update user XP
        current_user["xp_points"] = int(current_user.get("xp_points", 0)) + xp_earned
        current_user["level"] = max(1, int(current_user["xp_points"]) // 500 + 1)
        csv_handler.update("users", current_user["user_id"], current_user, "user_id")

        return {
            "session_id": session_id,
            "topic": session["topic"],
            "difficulty_level": session["difficulty_level"],
            "duration_minutes": session["duration_minutes"],
            "score": session_end.final_score,
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "accuracy_rate": round(accuracy_rate, 2),
            "xp_earned": xp_earned,
            "time_spent_seconds": session_end.total_time_seconds,
            "completed_at": session["completed_at"]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise handle_error(
            e,
            "ending learning session",
            public_message=ErrorMessages.SESSION_ERROR,
            log_context={"session_id": session_id}
        )
