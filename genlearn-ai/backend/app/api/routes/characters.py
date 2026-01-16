"""
Characters Routes - Character creation and management
"""

from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form
from datetime import datetime
from pydantic import BaseModel
import base64

from app.api.dependencies import get_current_user
from app.database.csv_handler import CSVHandler
from app.database.file_handler import FileHandler
from app.models.avatar import Character
from app.services.avatar_service import AvatarService
from app.services.provider_factory import ProviderFactory
from app.utils.helpers import generate_unique_id

router = APIRouter()


class GenerateCharacterRequest(BaseModel):
    """Request model for AI-generated character from prompt"""
    name: str
    prompt: str
    description: str
    style: str = "cartoon"


class DrawingCharacterRequest(BaseModel):
    """Request model for character from drawing canvas"""
    drawing_data: str  # Base64 encoded image
    name: str
    description: str
    style: str = "cartoon"
    custom_prompt: str = ""  # Optional custom instructions


@router.get("/list", response_model=list[Character], status_code=status.HTTP_200_OK)
async def get_characters(current_user: dict = Depends(get_current_user)):
    """
    Get list of user's characters

    Args:
        current_user: Authenticated user

    Returns:
        List of user's characters
    """
    csv_handler = CSVHandler()

    try:
        # Get all characters for this user
        all_characters = csv_handler.read_all("characters")
        user_characters = [
            {
                **character,
                "image_url": f"/media/{character['image_path']}"
            }
            for character in all_characters
            if character.get("user_id") == current_user["user_id"]
        ]

        return user_characters

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching characters: {str(e)}"
        )


@router.post("/create", response_model=Character, status_code=status.HTTP_201_CREATED)
async def create_character(
    file: UploadFile = File(...),
    name: str = Form(...),
    description: str = Form(...),
    creation_method: str = Form("upload"),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new character from uploaded image or drawing

    Args:
        file: Image file
        name: Character name
        description: Character description
        creation_method: How character was created (upload/draw/gallery)
        current_user: Authenticated user

    Returns:
        Created character data
    """
    csv_handler = CSVHandler()
    file_handler = FileHandler()
    avatar_service = AvatarService()

    try:
        # Read uploaded file
        image_data = await file.read()

        # Stylize character using AI
        character_image = await avatar_service.stylize_character(image_data, "cartoon")

        # Save character image
        character_id = generate_unique_id("CHR")
        filename = f"character_{character_id}.png"
        image_path = file_handler.save_image(character_image, "characters", filename)

        # Create character record
        character_data = {
            "character_id": character_id,
            "user_id": current_user["user_id"],
            "name": name,
            "image_path": image_path,
            "creation_method": creation_method,
            "description": description,
            "created_at": datetime.now().isoformat()
        }

        csv_handler.create("characters", character_data)

        return {
            **character_data,
            "image_url": f"/media/{image_path}"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating character: {str(e)}"
        )


@router.post("/generate", response_model=Character, status_code=status.HTTP_201_CREATED)
async def generate_character_from_prompt(
    request: GenerateCharacterRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Generate character from text prompt using AI image generation

    Args:
        request: Character generation request with prompt
        current_user: Authenticated user

    Returns:
        Created character data
    """
    csv_handler = CSVHandler()
    file_handler = FileHandler()
    avatar_service = AvatarService()

    try:
        # Generate character using AI with the prompt
        character_image = await avatar_service.generate_character_from_prompt(
            request.prompt,
            request.style
        )

        # Save character image
        character_id = generate_unique_id("CHR")
        filename = f"character_{character_id}.png"
        image_path = file_handler.save_image(character_image, "characters", filename)

        # Create character record
        character_data = {
            "character_id": character_id,
            "user_id": current_user["user_id"],
            "name": request.name,
            "image_path": image_path,
            "creation_method": "ai_generated",
            "description": request.description,
            "created_at": datetime.now().isoformat()
        }

        csv_handler.create("characters", character_data)

        return {
            **character_data,
            "image_url": f"/media/{image_path}"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating character: {str(e)}"
        )


@router.post("/upload", response_model=Character, status_code=status.HTTP_201_CREATED)
async def create_character_from_upload(
    file: UploadFile = File(...),
    name: str = Form(...),
    description: str = Form(...),
    style: str = Form("cartoon"),
    custom_prompt: str = Form(""),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a full-body character from uploaded image using AI vision.
    
    The AI will analyze the uploaded image and create a story character
    with full body, dynamic pose, and contextual background.
    
    Args:
        file: Uploaded image file (photo, sketch, etc.)
        name: Character name
        description: Character description/role
        style: Visual style (cartoon/realistic)
        custom_prompt: Optional custom instructions
        current_user: Authenticated user
    
    Returns:
        Created character data
    """
    csv_handler = CSVHandler()
    file_handler = FileHandler()
    image_provider = ProviderFactory.get_image_provider()

    try:
        # Read uploaded file
        image_data = await file.read()

        # Generate full-body character using AI vision
        character_image = await image_provider.generate_character(
            source_image=image_data,
            style=style,
            custom_prompt=custom_prompt,
            character_name=name,
            character_description=description
        )

        # Save character image
        character_id = generate_unique_id("CHR")
        filename = f"character_{character_id}.png"
        image_path = file_handler.save_image(character_image, "characters", filename)

        # Create character record
        character_data = {
            "character_id": character_id,
            "user_id": current_user["user_id"],
            "name": name,
            "image_path": image_path,
            "creation_method": "upload",
            "description": description,
            "created_at": datetime.now().isoformat()
        }

        csv_handler.create("characters", character_data)

        return {
            **character_data,
            "image_url": f"/media/{image_path}"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating character from upload: {str(e)}"
        )


@router.post("/draw", response_model=Character, status_code=status.HTTP_201_CREATED)
async def create_character_from_drawing(
    drawing: DrawingCharacterRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a full-body character from drawing canvas data using AI.
    
    The AI will analyze the drawing and create a polished story character
    with full body, dynamic pose, and contextual background.
    
    Args:
        drawing: Drawing data and character info
        current_user: Authenticated user
    
    Returns:
        Created character data
    """
    csv_handler = CSVHandler()
    file_handler = FileHandler()
    image_provider = ProviderFactory.get_image_provider()

    try:
        # Decode base64 drawing data
        drawing_data = drawing.drawing_data
        if ',' in drawing_data:
            drawing_data = drawing_data.split(',')[1]
        image_data = base64.b64decode(drawing_data)

        # Generate full-body character using AI vision
        character_image = await image_provider.generate_character(
            source_image=image_data,
            style=drawing.style,
            custom_prompt=drawing.custom_prompt,
            character_name=drawing.name,
            character_description=drawing.description
        )

        # Save character image
        character_id = generate_unique_id("CHR")
        filename = f"character_{character_id}.png"
        image_path = file_handler.save_image(character_image, "characters", filename)

        # Create character record
        character_data = {
            "character_id": character_id,
            "user_id": current_user["user_id"],
            "name": drawing.name,
            "image_path": image_path,
            "creation_method": "draw",
            "description": drawing.description,
            "created_at": datetime.now().isoformat()
        }

        csv_handler.create("characters", character_data)

        return {
            **character_data,
            "image_url": f"/media/{image_path}"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating character from drawing: {str(e)}"
        )


@router.delete("/{character_id}", status_code=status.HTTP_200_OK)
async def delete_character(
    character_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a character

    Args:
        character_id: Character identifier
        current_user: Authenticated user

    Returns:
        Success message
    """
    csv_handler = CSVHandler()

    try:
        # Get character
        character = csv_handler.read_by_id("characters", character_id, "character_id")
        if not character:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Character not found"
            )

        # Verify user owns this character
        if character.get("user_id") != current_user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this character"
            )

        # Delete character using the correct method
        deleted = csv_handler.delete_by_id("characters", character_id, "character_id")
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete character from database"
            )

        return {"message": "Character deleted successfully", "character_id": character_id}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting character: {str(e)}"
        )
