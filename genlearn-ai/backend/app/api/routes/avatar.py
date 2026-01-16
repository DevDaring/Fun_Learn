"""
Avatar Routes - Avatar creation and management
"""

from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form
from datetime import datetime
from pydantic import BaseModel
import base64

from app.api.dependencies import get_current_user
from app.database.csv_handler import CSVHandler
from app.database.file_handler import FileHandler
from app.models.avatar import Avatar
from app.services.avatar_service import AvatarService
from app.utils.helpers import generate_unique_id

router = APIRouter()


class DrawingAvatarRequest(BaseModel):
    """Request model for avatar from drawing"""
    drawing_data: str  # Base64 encoded image
    name: str
    style: str = "cartoon"
    custom_prompt: str = ""  # Optional custom prompt


@router.get("/list", response_model=list[Avatar], status_code=status.HTTP_200_OK)
async def get_avatars(current_user: dict = Depends(get_current_user)):
    """
    Get list of user's avatars

    Args:
        current_user: Authenticated user

    Returns:
        List of user's avatars
    """
    csv_handler = CSVHandler()

    try:
        # Get all avatars for this user
        all_avatars = csv_handler.read_all("avatars")
        user_avatars = [
            {
                **avatar,
                "image_url": f"/media/{avatar['image_path']}"
            }
            for avatar in all_avatars
            if avatar.get("user_id") == current_user["user_id"]
        ]

        return user_avatars

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching avatars: {str(e)}"
        )


@router.post("/upload", response_model=Avatar, status_code=status.HTTP_201_CREATED)
async def create_avatar_from_upload(
    file: UploadFile = File(...),
    name: str = Form(...),
    style: str = Form("cartoon"),
    custom_prompt: str = Form(""),
    current_user: dict = Depends(get_current_user)
):
    """
    Create avatar from uploaded image

    Args:
        file: Uploaded image file
        name: Avatar name
        style: Avatar style (cartoon/realistic)
        custom_prompt: Optional custom prompt for avatar generation
        current_user: Authenticated user

    Returns:
        Created avatar data
    """
    csv_handler = CSVHandler()
    file_handler = FileHandler()
    avatar_service = AvatarService()

    try:
        # Read uploaded file
        image_data = await file.read()

        # Generate avatar using AI with vision + optional prompt
        avatar_image = await avatar_service.generate_avatar(image_data, style, custom_prompt)

        # Save avatar image
        avatar_id = generate_unique_id("AVT")
        filename = f"avatar_{avatar_id}.png"
        image_path = file_handler.save_image(avatar_image, "avatars", filename)

        # Create avatar record
        avatar_data = {
            "avatar_id": avatar_id,
            "user_id": current_user["user_id"],
            "name": name,
            "image_path": image_path,
            "creation_method": "upload",
            "style": style,
            "created_at": datetime.now().isoformat()
        }

        csv_handler.create("avatars", avatar_data)

        return {
            **avatar_data,
            "image_url": f"/media/{image_path}"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating avatar from upload: {str(e)}"
        )


@router.post("/draw", response_model=Avatar, status_code=status.HTTP_201_CREATED)
async def create_avatar_from_drawing(
    drawing: DrawingAvatarRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Create avatar from drawing canvas data

    Args:
        drawing: Drawing data and avatar info
        current_user: Authenticated user

    Returns:
        Created avatar data
    """
    csv_handler = CSVHandler()
    file_handler = FileHandler()
    avatar_service = AvatarService()

    try:
        # Decode base64 drawing data
        image_data = base64.b64decode(drawing.drawing_data.split(',')[1] if ',' in drawing.drawing_data else drawing.drawing_data)

        # Generate avatar using AI with vision + optional prompt
        avatar_image = await avatar_service.generate_avatar(image_data, drawing.style, drawing.custom_prompt)

        # Save avatar image
        avatar_id = generate_unique_id("AVT")
        filename = f"avatar_{avatar_id}.png"
        image_path = file_handler.save_image(avatar_image, "avatars", filename)

        # Create avatar record
        avatar_data = {
            "avatar_id": avatar_id,
            "user_id": current_user["user_id"],
            "name": drawing.name,
            "image_path": image_path,
            "creation_method": "draw",
            "style": drawing.style,
            "created_at": datetime.now().isoformat()
        }

        csv_handler.create("avatars", avatar_data)

        return {
            **avatar_data,
            "image_url": f"/media/{image_path}"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating avatar from drawing: {str(e)}"
        )


class GenerateAvatarRequest(BaseModel):
    """Request model for AI-generated avatar"""
    name: str
    prompt: str
    style: str = "cartoon"


@router.post("/generate", response_model=Avatar, status_code=status.HTTP_201_CREATED)
async def generate_avatar_from_prompt(
    request: GenerateAvatarRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Generate avatar from text prompt using AI image generation

    Args:
        request: Avatar generation request with prompt
        current_user: Authenticated user

    Returns:
        Created avatar data
    """
    csv_handler = CSVHandler()
    file_handler = FileHandler()
    avatar_service = AvatarService()

    try:
        # Generate avatar using AI with the prompt
        avatar_image = await avatar_service.generate_avatar_from_prompt(
            request.prompt,
            request.style
        )

        # Save avatar image
        avatar_id = generate_unique_id("AVT")
        filename = f"avatar_{avatar_id}.png"
        image_path = file_handler.save_image(avatar_image, "avatars", filename)

        # Create avatar record
        avatar_data = {
            "avatar_id": avatar_id,
            "user_id": current_user["user_id"],
            "name": request.name,
            "image_path": image_path,
            "creation_method": "ai_generated",
            "style": request.style,
            "created_at": datetime.now().isoformat()
        }

        csv_handler.create("avatars", avatar_data)

        return {
            **avatar_data,
            "image_url": f"/media/{image_path}"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating avatar: {str(e)}"
        )


class SetActiveAvatarRequest(BaseModel):
    """Request model for setting active avatar"""
    avatar_id: str


@router.post("/set-active", status_code=status.HTTP_200_OK)
async def set_active_avatar(
    request: SetActiveAvatarRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Set avatar as active for user profile

    Args:
        request: Avatar ID to set as active
        current_user: Authenticated user

    Returns:
        Success message
    """
    csv_handler = CSVHandler()

    try:
        # Verify avatar belongs to user
        avatars = csv_handler.read_all("avatars")
        avatar = None
        for a in avatars:
            if a.get("avatar_id") == request.avatar_id and a.get("user_id") == current_user["user_id"]:
                avatar = a
                break

        if not avatar:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Avatar not found or access denied"
            )

        # Update user's active avatar
        csv_handler.update(
            "users",
            current_user["user_id"],
            {"avatar_id": request.avatar_id},
            "user_id"
        )

        return {"message": "Avatar set as active", "avatar_id": request.avatar_id}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error setting active avatar: {str(e)}"
        )


@router.delete("/{avatar_id}", status_code=status.HTTP_200_OK)
async def delete_avatar(
    avatar_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete an avatar

    Args:
        avatar_id: Avatar identifier
        current_user: Authenticated user

    Returns:
        Success message
    """
    csv_handler = CSVHandler()

    try:
        # Verify avatar belongs to user
        avatars = csv_handler.read_all("avatars")
        avatar = None
        for a in avatars:
            if a.get("avatar_id") == avatar_id and a.get("user_id") == current_user["user_id"]:
                avatar = a
                break

        if not avatar:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Avatar not found or access denied"
            )

        # Delete avatar record using the correct method
        deleted = csv_handler.delete_by_id("avatars", avatar_id, "avatar_id")
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete avatar from database"
            )

        return {"message": "Avatar deleted successfully", "avatar_id": avatar_id}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting avatar: {str(e)}"
        )


@router.get("/gallery", response_model=list[dict], status_code=status.HTTP_200_OK)
async def get_avatar_gallery(current_user: dict = Depends(get_current_user)):
    """
    Get gallery of default avatars (pre-made options)

    Args:
        current_user: Authenticated user

    Returns:
        List of default avatar options
    """
    try:
        # Return list of default avatars
        # In production, these would be pre-generated and stored
        default_avatars = [
            {
                "avatar_id": "DEFAULT_001",
                "name": "Explorer",
                "image_url": "/media/default-avatars/explorer.png",
                "style": "cartoon"
            },
            {
                "avatar_id": "DEFAULT_002",
                "name": "Scientist",
                "image_url": "/media/default-avatars/scientist.png",
                "style": "cartoon"
            },
            {
                "avatar_id": "DEFAULT_003",
                "name": "Artist",
                "image_url": "/media/default-avatars/artist.png",
                "style": "cartoon"
            },
            {
                "avatar_id": "DEFAULT_004",
                "name": "Wizard",
                "image_url": "/media/default-avatars/wizard.png",
                "style": "cartoon"
            },
            {
                "avatar_id": "DEFAULT_005",
                "name": "Astronaut",
                "image_url": "/media/default-avatars/astronaut.png",
                "style": "realistic"
            }
        ]

        return default_avatars

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching avatar gallery: {str(e)}"
        )
