"""
Content Generator Service
Uses AI provider to generate learning content with stories and image prompts
"""

import asyncio
from typing import Any, Optional
from datetime import datetime

from app.services.provider_factory import ProviderFactory
from app.services.ai_providers.base import ContentGenerationRequest
from app.services.image_providers.base import ImageGenerationRequest
from app.database.csv_handler import (
    get_sessions_handler,
    get_avatars_handler,
    get_characters_handler,
    get_learning_history_handler
)
from app.database.file_handler import save_generated_image
from app.config import settings


class ContentGenerator:
    """
    Service for generating learning content with AI.

    Responsibilities:
    - Generate story narratives based on topic and difficulty
    - Create image prompts for visual content
    - Generate images using image provider
    - Save content and track history
    """

    def __init__(self):
        """Initialize the content generator service."""
        self.ai_provider = ProviderFactory.get_ai_provider()
        self.image_provider = ProviderFactory.get_image_provider()
        self.sessions_handler = get_sessions_handler()
        self.avatars_handler = get_avatars_handler()
        self.characters_handler = get_characters_handler()
        self.history_handler = get_learning_history_handler()

    async def generate_session_content(
        self,
        session_id: str,
        topic: str,
        difficulty_level: int,
        duration_minutes: int,
        visual_style: str = "cartoon",
        avatar_id: Optional[str] = None,
        character_ids: Optional[list[str]] = None
    ) -> dict[str, Any]:
        """
        Generate complete learning content for a session.

        Args:
            session_id: Unique session identifier
            topic: Learning topic
            difficulty_level: Difficulty level (1-10)
            duration_minutes: Session duration
            visual_style: Visual style (cartoon/realistic)
            avatar_id: User's avatar ID (optional)
            character_ids: List of character IDs to include (optional)

        Returns:
            Dictionary containing story segments and summary

        Raises:
            Exception: If content generation fails
        """
        try:
            # Calculate number of images based on duration
            num_images = self._calculate_num_images(duration_minutes)

            # Get avatar and character descriptions
            avatar_description = None
            if avatar_id:
                avatar = self.avatars_handler.find_one({"avatar_id": avatar_id})
                if avatar:
                    avatar_description = avatar.get("name", "Your avatar")

            character_descriptions = []
            if character_ids:
                for char_id in character_ids:
                    character = self.characters_handler.find_one({"character_id": char_id})
                    if character:
                        char_desc = f"{character.get('name', 'Character')} - {character.get('description', '')}"
                        character_descriptions.append(char_desc)

            # Create content generation request
            request = ContentGenerationRequest(
                topic=topic,
                difficulty_level=difficulty_level,
                visual_style=visual_style,
                num_images=num_images,
                avatar_description=avatar_description,
                character_descriptions=character_descriptions if character_descriptions else None
            )

            # Generate content using AI provider
            content = await self.ai_provider.generate_content(request)

            # Generate images for each story segment
            story_segments = content.get("story_segments", [])

            # Process segments in parallel for speed
            tasks = []
            for segment in story_segments:
                task = self._generate_segment_image(
                    session_id=session_id,
                    segment=segment,
                    visual_style=visual_style,
                    avatar_id=avatar_id,
                    character_ids=character_ids
                )
                tasks.append(task)

            # Wait for all images to be generated
            segment_results = await asyncio.gather(*tasks, return_exceptions=True)

            # Update segments with image URLs
            for i, segment in enumerate(story_segments):
                if i < len(segment_results) and not isinstance(segment_results[i], Exception):
                    segment["image_url"] = segment_results[i]
                else:
                    segment["image_url"] = None

            # Save to learning history
            session = self.sessions_handler.find_one({"session_id": session_id})
            if session:
                user_id = session.get("user_id")
                for i, segment in enumerate(story_segments):
                    if segment.get("image_url"):
                        self._save_to_history(
                            user_id=user_id,
                            session_id=session_id,
                            content_type="image",
                            content_id=f"{session_id}_seg{i+1}",
                            content_path=segment["image_url"],
                            topic=topic
                        )

            return {
                "session_id": session_id,
                "topic": topic,
                "story_segments": story_segments,
                "topic_summary": content.get("topic_summary", ""),
                "total_cycles": len(story_segments)
            }

        except Exception as e:
            raise Exception(f"Failed to generate content: {str(e)}")

    async def _generate_segment_image(
        self,
        session_id: str,
        segment: dict[str, Any],
        visual_style: str,
        avatar_id: Optional[str] = None,
        character_ids: Optional[list[str]] = None
    ) -> Optional[str]:
        """
        Generate image for a single story segment.

        Args:
            session_id: Session identifier
            segment: Story segment with image prompt
            visual_style: Visual style
            avatar_id: Avatar ID (optional)
            character_ids: Character IDs (optional)

        Returns:
            Image URL or None if generation fails
        """
        try:
            image_prompt = segment.get("image_prompt", "")
            segment_number = segment.get("segment_number", 1)

            # Get avatar and character image paths
            avatar_image_path = None
            if avatar_id:
                avatar = self.avatars_handler.find_one({"avatar_id": avatar_id})
                if avatar:
                    avatar_image_path = avatar.get("image_path")

            character_image_paths = []
            if character_ids:
                for char_id in character_ids:
                    character = self.characters_handler.find_one({"character_id": char_id})
                    if character:
                        character_image_paths.append(character.get("image_path"))

            # Create image generation request
            request = ImageGenerationRequest(
                prompt=image_prompt,
                style=visual_style,
                width=1024,
                height=576,
                avatar_image_path=avatar_image_path,
                character_image_paths=character_image_paths if character_image_paths else None
            )

            # Generate image
            image_bytes = await self.image_provider.generate_image(request)

            # Save image
            success, image_path = save_generated_image(
                file_data=image_bytes,
                session_id=session_id,
                segment_number=segment_number
            )

            if success:
                # Return URL (relative path that frontend can access)
                return f"/media/{image_path}"

            return None

        except Exception as e:
            print(f"Error generating image for segment: {e}")
            return None

    def _calculate_num_images(self, duration_minutes: int) -> int:
        """
        Calculate number of images based on duration.

        Formula: 1 image per 5 minutes (minimum 2, maximum 8)

        Args:
            duration_minutes: Session duration in minutes

        Returns:
            Number of images to generate
        """
        num_images = max(2, min(8, duration_minutes // 5))
        return num_images

    def _save_to_history(
        self,
        user_id: str,
        session_id: str,
        content_type: str,
        content_id: str,
        content_path: str,
        topic: str
    ) -> bool:
        """
        Save content to learning history.

        Args:
            user_id: User identifier
            session_id: Session identifier
            content_type: Type of content (image/video/quiz)
            content_id: Content identifier
            content_path: Path to content
            topic: Learning topic

        Returns:
            Success status
        """
        try:
            history_id = self.history_handler.generate_id("HIS", "history_id")

            history_data = {
                "history_id": history_id,
                "user_id": user_id,
                "session_id": session_id,
                "content_type": content_type,
                "content_id": content_id,
                "content_path": content_path,
                "topic": topic,
                "viewed_at": datetime.now().isoformat()
            }

            return self.history_handler.append(history_data)

        except Exception as e:
            print(f"Error saving to history: {e}")
            return False

    async def regenerate_segment(
        self,
        session_id: str,
        segment_number: int,
        new_prompt: Optional[str] = None
    ) -> Optional[str]:
        """
        Regenerate a specific segment image.

        Args:
            session_id: Session identifier
            segment_number: Segment number to regenerate
            new_prompt: Optional new prompt (uses existing if None)

        Returns:
            New image URL or None if fails
        """
        try:
            session = self.sessions_handler.find_one({"session_id": session_id})
            if not session:
                raise ValueError("Session not found")

            visual_style = session.get("visual_style", "cartoon")

            # Use provided prompt or generate a generic one
            if not new_prompt:
                topic = session.get("topic", "learning")
                new_prompt = f"Educational illustration about {topic} in {visual_style} style"

            request = ImageGenerationRequest(
                prompt=new_prompt,
                style=visual_style,
                width=1024,
                height=576
            )

            image_bytes = await self.image_provider.generate_image(request)

            success, image_path = save_generated_image(
                file_data=image_bytes,
                session_id=session_id,
                segment_number=segment_number
            )

            if success:
                return f"/media/{image_path}"

            return None

        except Exception as e:
            print(f"Error regenerating segment: {e}")
            return None

    async def generate_learning_content(
        self,
        topic: str,
        difficulty_level: int,
        visual_style: str = "cartoon",
        story_style: str = "fun",
        num_segments: int = 3,
        avatar_description: Optional[str] = None,
        character_descriptions: Optional[list[str]] = None
    ) -> dict[str, Any]:
        """
        Generate learning content (alias for routes compatibility).

        Args:
            topic: Learning topic
            difficulty_level: Difficulty level (1-10)
            visual_style: Visual style (cartoon/realistic)
            story_style: Story narrative style (thriller/fun/nostalgic/adventure/mystery/scifi)
            num_segments: Number of story segments
            avatar_description: Avatar description
            character_descriptions: List of character descriptions

        Returns:
            Dictionary containing story segments and summary
        """
        request = ContentGenerationRequest(
            topic=topic,
            difficulty_level=difficulty_level,
            visual_style=visual_style,
            story_style=story_style,
            num_images=num_segments,
            avatar_description=avatar_description,
            character_descriptions=character_descriptions
        )

        # Generate content using AI provider
        content = await self.ai_provider.generate_content(request)

        return content

    async def generate_image(
        self,
        prompt: str,
        style: str = "cartoon"
    ) -> bytes:
        """
        Generate an image from a prompt.

        Args:
            prompt: Image generation prompt
            style: Visual style (cartoon/realistic)

        Returns:
            Image bytes
        """
        request = ImageGenerationRequest(
            prompt=prompt,
            style=style,
            width=1024,
            height=576
        )

        return await self.image_provider.generate_image(request)

    async def health_check(self) -> dict[str, Any]:
        """
        Check health of content generation service.

        Returns:
            Health status dictionary
        """
        try:
            ai_healthy = await self.ai_provider.health_check()
            image_healthy = await self.image_provider.health_check()

            return {
                "service": "ContentGenerator",
                "status": "healthy" if (ai_healthy and image_healthy) else "degraded",
                "ai_provider": "healthy" if ai_healthy else "unhealthy",
                "image_provider": "healthy" if image_healthy else "unhealthy"
            }
        except Exception as e:
            return {
                "service": "ContentGenerator",
                "status": "unhealthy",
                "error": str(e)
            }
