"""
Avatar Service
Creates avatars and characters from uploads/drawings using image provider
"""

import base64
from typing import Any, Optional
from datetime import datetime
from io import BytesIO
from pathlib import Path

from app.services.provider_factory import ProviderFactory
from app.database.csv_handler import (
    get_avatars_handler,
    get_characters_handler,
    get_users_handler
)
from app.database.file_handler import (
    save_avatar,
    save_character,
    FileHandler
)
from app.models.avatar import (
    Avatar,
    AvatarCreate,
    Character,
    CharacterCreate,
    AvatarDisplay,
    CharacterDisplay
)


class AvatarService:
    """
    Service for managing avatars and characters.

    Responsibilities:
    - Create avatars from uploaded images
    - Create avatars from canvas drawings
    - Create characters from uploads/drawings
    - Stylize images using AI image provider
    - Manage avatar and character galleries
    """

    def __init__(self):
        """Initialize the avatar service."""
        self.image_provider = ProviderFactory.get_image_provider()
        self.avatars_handler = get_avatars_handler()
        self.characters_handler = get_characters_handler()
        self.users_handler = get_users_handler()

    async def create_avatar_from_upload(
        self,
        user_id: str,
        name: str,
        image_data: bytes,
        style: str = "cartoon",
        filename: str = "avatar.png"
    ) -> dict[str, Any]:
        """
        Create avatar from uploaded image.

        Args:
            user_id: User identifier
            name: Avatar name
            image_data: Image file bytes
            style: Style to apply (cartoon/realistic)
            filename: Original filename

        Returns:
            Created avatar information

        Raises:
            Exception: If avatar creation fails
        """
        try:
            # Stylize image using image provider
            stylized_image = await self.image_provider.generate_avatar(
                source_image=image_data,
                style=style
            )

            # Generate unique avatar ID
            avatar_id = self.avatars_handler.generate_id("AVT", "avatar_id")

            # Save avatar image
            extension = Path(filename).suffix or ".png"
            success, image_path = save_avatar(
                file_data=stylized_image,
                user_id=user_id,
                extension=extension
            )

            if not success:
                raise Exception("Failed to save avatar image")

            # Create avatar record
            avatar_data = {
                "avatar_id": avatar_id,
                "user_id": user_id,
                "name": name,
                "image_path": image_path,
                "creation_method": "upload",
                "style": style,
                "created_at": datetime.now().isoformat()
            }

            # Save to CSV
            if not self.avatars_handler.append(avatar_data):
                raise Exception("Failed to save avatar record")

            # Update user's avatar
            self.users_handler.update(
                {"user_id": user_id},
                {"avatar_id": avatar_id}
            )

            return {
                "avatar_id": avatar_id,
                "name": name,
                "image_url": f"/media/{image_path}",
                "style": style,
                "creation_method": "upload"
            }

        except Exception as e:
            raise Exception(f"Failed to create avatar from upload: {str(e)}")

    async def create_avatar_from_drawing(
        self,
        user_id: str,
        name: str,
        drawing_base64: str,
        style: str = "cartoon"
    ) -> dict[str, Any]:
        """
        Create avatar from canvas drawing.

        Args:
            user_id: User identifier
            name: Avatar name
            drawing_base64: Base64 encoded drawing data
            style: Style to apply

        Returns:
            Created avatar information

        Raises:
            Exception: If avatar creation fails
        """
        try:
            # Decode base64 image
            if "," in drawing_base64:
                # Remove data:image/png;base64, prefix if present
                drawing_base64 = drawing_base64.split(",")[1]

            image_data = base64.b64decode(drawing_base64)

            # Stylize drawing using image provider
            stylized_image = await self.image_provider.generate_avatar(
                source_image=image_data,
                style=style
            )

            # Generate unique avatar ID
            avatar_id = self.avatars_handler.generate_id("AVT", "avatar_id")

            # Save avatar image
            success, image_path = save_avatar(
                file_data=stylized_image,
                user_id=user_id,
                extension=".png"
            )

            if not success:
                raise Exception("Failed to save avatar image")

            # Create avatar record
            avatar_data = {
                "avatar_id": avatar_id,
                "user_id": user_id,
                "name": name,
                "image_path": image_path,
                "creation_method": "draw",
                "style": style,
                "created_at": datetime.now().isoformat()
            }

            # Save to CSV
            if not self.avatars_handler.append(avatar_data):
                raise Exception("Failed to save avatar record")

            # Update user's avatar
            self.users_handler.update(
                {"user_id": user_id},
                {"avatar_id": avatar_id}
            )

            return {
                "avatar_id": avatar_id,
                "name": name,
                "image_url": f"/media/{image_path}",
                "style": style,
                "creation_method": "draw"
            }

        except Exception as e:
            raise Exception(f"Failed to create avatar from drawing: {str(e)}")

    async def create_avatar_from_gallery(
        self,
        user_id: str,
        name: str,
        gallery_image_id: str
    ) -> dict[str, Any]:
        """
        Select avatar from pre-made gallery.

        Args:
            user_id: User identifier
            name: Avatar name
            gallery_image_id: ID of gallery image

        Returns:
            Created avatar information

        Raises:
            Exception: If avatar creation fails
        """
        try:
            # In a real implementation, this would copy from a gallery folder
            # For now, we'll create a placeholder

            avatar_id = self.avatars_handler.generate_id("AVT", "avatar_id")

            # Placeholder image path (in production, copy from gallery)
            image_path = f"avatars/gallery_{gallery_image_id}.png"

            avatar_data = {
                "avatar_id": avatar_id,
                "user_id": user_id,
                "name": name,
                "image_path": image_path,
                "creation_method": "gallery",
                "style": "cartoon",
                "created_at": datetime.now().isoformat()
            }

            if not self.avatars_handler.append(avatar_data):
                raise Exception("Failed to save avatar record")

            self.users_handler.update(
                {"user_id": user_id},
                {"avatar_id": avatar_id}
            )

            return {
                "avatar_id": avatar_id,
                "name": name,
                "image_url": f"/media/{image_path}",
                "style": "cartoon",
                "creation_method": "gallery"
            }

        except Exception as e:
            raise Exception(f"Failed to create avatar from gallery: {str(e)}")

    async def create_character_from_upload(
        self,
        user_id: str,
        name: str,
        description: str,
        image_data: bytes,
        filename: str = "character.png"
    ) -> dict[str, Any]:
        """
        Create character from uploaded image.

        Args:
            user_id: User identifier
            name: Character name
            description: Character description
            image_data: Image file bytes
            filename: Original filename

        Returns:
            Created character information

        Raises:
            Exception: If character creation fails
        """
        try:
            # Stylize character image
            stylized_image = await self.image_provider.stylize_character(
                source_image=image_data,
                style="cartoon"
            )

            # Generate unique character ID
            character_id = self.characters_handler.generate_id("CHR", "character_id")

            # Save character image
            extension = Path(filename).suffix or ".png"
            success, image_path = save_character(
                file_data=stylized_image,
                character_id=character_id,
                extension=extension
            )

            if not success:
                raise Exception("Failed to save character image")

            # Create character record
            character_data = {
                "character_id": character_id,
                "user_id": user_id,
                "name": name,
                "image_path": image_path,
                "creation_method": "upload",
                "description": description,
                "created_at": datetime.now().isoformat()
            }

            # Save to CSV
            if not self.characters_handler.append(character_data):
                raise Exception("Failed to save character record")

            return {
                "character_id": character_id,
                "name": name,
                "description": description,
                "image_url": f"/media/{image_path}",
                "creation_method": "upload"
            }

        except Exception as e:
            raise Exception(f"Failed to create character from upload: {str(e)}")

    async def create_character_from_drawing(
        self,
        user_id: str,
        name: str,
        description: str,
        drawing_base64: str
    ) -> dict[str, Any]:
        """
        Create character from canvas drawing.

        Args:
            user_id: User identifier
            name: Character name
            description: Character description
            drawing_base64: Base64 encoded drawing

        Returns:
            Created character information

        Raises:
            Exception: If character creation fails
        """
        try:
            # Decode base64 image
            if "," in drawing_base64:
                drawing_base64 = drawing_base64.split(",")[1]

            image_data = base64.b64decode(drawing_base64)

            # Stylize drawing
            stylized_image = await self.image_provider.stylize_character(
                source_image=image_data,
                style="cartoon"
            )

            # Generate unique character ID
            character_id = self.characters_handler.generate_id("CHR", "character_id")

            # Save character image
            success, image_path = save_character(
                file_data=stylized_image,
                character_id=character_id,
                extension=".png"
            )

            if not success:
                raise Exception("Failed to save character image")

            # Create character record
            character_data = {
                "character_id": character_id,
                "user_id": user_id,
                "name": name,
                "image_path": image_path,
                "creation_method": "draw",
                "description": description,
                "created_at": datetime.now().isoformat()
            }

            # Save to CSV
            if not self.characters_handler.append(character_data):
                raise Exception("Failed to save character record")

            return {
                "character_id": character_id,
                "name": name,
                "description": description,
                "image_url": f"/media/{image_path}",
                "creation_method": "draw"
            }

        except Exception as e:
            raise Exception(f"Failed to create character from drawing: {str(e)}")

    def get_user_avatars(self, user_id: str) -> list[AvatarDisplay]:
        """
        Get all avatars for a user.

        Args:
            user_id: User identifier

        Returns:
            List of avatar displays
        """
        try:
            avatars = self.avatars_handler.find({"user_id": user_id})

            return [
                AvatarDisplay(
                    avatar_id=a.get("avatar_id", ""),
                    name=a.get("name", ""),
                    image_url=f"/media/{a.get('image_path', '')}",
                    style=a.get("style", "cartoon"),
                    creation_method=a.get("creation_method", "upload"),
                    is_active=True
                )
                for a in avatars
            ]

        except Exception as e:
            print(f"Error getting user avatars: {e}")
            return []

    def get_user_characters(self, user_id: str) -> list[CharacterDisplay]:
        """
        Get all characters for a user.

        Args:
            user_id: User identifier

        Returns:
            List of character displays
        """
        try:
            characters = self.characters_handler.find({"user_id": user_id})

            return [
                CharacterDisplay(
                    character_id=c.get("character_id", ""),
                    name=c.get("name", ""),
                    image_url=f"/media/{c.get('image_path', '')}",
                    description=c.get("description", ""),
                    role=c.get("role"),
                    is_active=True,
                    usage_count=c.get("usage_count", 0)
                )
                for c in characters
            ]

        except Exception as e:
            print(f"Error getting user characters: {e}")
            return []

    def get_avatar_by_id(self, avatar_id: str) -> Optional[dict[str, Any]]:
        """
        Get avatar by ID.

        Args:
            avatar_id: Avatar identifier

        Returns:
            Avatar data or None
        """
        avatar = self.avatars_handler.find_one({"avatar_id": avatar_id})
        if avatar:
            avatar["image_url"] = f"/media/{avatar.get('image_path', '')}"
        return avatar

    def get_character_by_id(self, character_id: str) -> Optional[dict[str, Any]]:
        """
        Get character by ID.

        Args:
            character_id: Character identifier

        Returns:
            Character data or None
        """
        character = self.characters_handler.find_one({"character_id": character_id})
        if character:
            character["image_url"] = f"/media/{character.get('image_path', '')}"
        return character

    def delete_avatar(self, user_id: str, avatar_id: str) -> bool:
        """
        Delete avatar (soft delete).

        Args:
            user_id: User identifier
            avatar_id: Avatar identifier

        Returns:
            Success status
        """
        try:
            avatar = self.avatars_handler.find_one({
                "avatar_id": avatar_id,
                "user_id": user_id
            })

            if not avatar:
                return False

            # Don't actually delete, just mark as inactive
            # Or delete from CSV if preferred
            return self.avatars_handler.delete({
                "avatar_id": avatar_id,
                "user_id": user_id
            })

        except Exception as e:
            print(f"Error deleting avatar: {e}")
            return False

    async def generate_avatar_from_prompt(
        self,
        prompt: str,
        style: str = "cartoon"
    ) -> bytes:
        """
        Generate avatar image from text prompt using AI.

        Args:
            prompt: Text description of the avatar
            style: Visual style (cartoon/realistic)

        Returns:
            Generated image bytes

        Raises:
            Exception: If generation fails
        """
        try:
            from app.services.image_providers.base import ImageGenerationRequest

            # Enhance prompt for avatar generation
            style_suffix = ""
            if style == "cartoon":
                style_suffix = ", cute cartoon style, friendly expression, colorful, digital art, high quality avatar"
            elif style == "realistic":
                style_suffix = ", realistic portrait style, professional quality, detailed, high resolution"

            enhanced_prompt = f"Avatar portrait: {prompt}{style_suffix}"

            request = ImageGenerationRequest(
                prompt=enhanced_prompt,
                style=style,
                width=512,
                height=512
            )

            image_bytes = await self.image_provider.generate_image(request)
            return image_bytes

        except Exception as e:
            raise Exception(f"Failed to generate avatar from prompt: {str(e)}")

    async def generate_avatar(
        self,
        source_image: bytes,
        style: str = "cartoon",
        custom_prompt: str = ""
    ) -> bytes:
        """
        Generate avatar from source image (upload or drawing) with optional prompt.

        Uses vision to understand the source image and generates a styled avatar.

        Args:
            source_image: Source image bytes (from upload or drawing)
            style: Visual style (cartoon/realistic)
            custom_prompt: Optional custom instructions from user

        Returns:
            Generated avatar image bytes

        Raises:
            Exception: If generation fails
        """
        try:
            image_bytes = await self.image_provider.generate_avatar(
                source_image=source_image,
                style=style,
                custom_prompt=custom_prompt
            )
            return image_bytes

        except Exception as e:
            raise Exception(f"Failed to generate avatar: {str(e)}")

    async def generate_character_from_prompt(
        self,
        prompt: str,
        style: str = "cartoon"
    ) -> bytes:
        """
        Generate character image from text prompt using AI.

        Args:
            prompt: Text description of the character
            style: Visual style (cartoon/realistic)

        Returns:
            Generated image bytes

        Raises:
            Exception: If generation fails
        """
        try:
            from app.services.image_providers.base import ImageGenerationRequest

            # Enhance prompt for character generation
            style_suffix = ""
            if style == "cartoon":
                style_suffix = ", cute cartoon character, full body, friendly expression, colorful background, digital art, story book illustration style"
            elif style == "realistic":
                style_suffix = ", realistic character illustration, full body portrait, detailed, high quality"

            enhanced_prompt = f"Character illustration: {prompt}{style_suffix}"

            request = ImageGenerationRequest(
                prompt=enhanced_prompt,
                style=style,
                width=512,
                height=512
            )

            image_bytes = await self.image_provider.generate_image(request)
            return image_bytes

        except Exception as e:
            raise Exception(f"Failed to generate character from prompt: {str(e)}")

    def delete_character(self, user_id: str, character_id: str) -> bool:
        """
        Delete character.

        Args:
            user_id: User identifier
            character_id: Character identifier

        Returns:
            Success status
        """
        try:
            return self.characters_handler.delete({
                "character_id": character_id,
                "user_id": user_id
            })

        except Exception as e:
            print(f"Error deleting character: {e}")
            return False

    async def health_check(self) -> dict[str, Any]:
        """
        Check health of avatar service.

        Returns:
            Health status dictionary
        """
        try:
            image_healthy = await self.image_provider.health_check()

            return {
                "service": "AvatarService",
                "status": "healthy" if image_healthy else "degraded",
                "image_provider": "healthy" if image_healthy else "unhealthy"
            }

        except Exception as e:
            return {
                "service": "AvatarService",
                "status": "unhealthy",
                "error": str(e)
            }
