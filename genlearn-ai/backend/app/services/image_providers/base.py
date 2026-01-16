"""
Base Image Provider Interface
"""

from abc import ABC, abstractmethod
from typing import Optional
from pydantic import BaseModel


class ImageGenerationRequest(BaseModel):
    prompt: str
    style: str = "cartoon"  # "cartoon" or "realistic"
    width: int = 1024
    height: int = 576  # 16:9 aspect ratio
    avatar_image_path: Optional[str] = None
    character_image_paths: Optional[list[str]] = None


class BaseImageProvider(ABC):
    """Abstract base class for Image providers."""

    @abstractmethod
    async def generate_image(
        self,
        request: ImageGenerationRequest
    ) -> bytes:
        """
        Generate an image based on prompt.

        Returns:
            Image bytes (PNG format)
        """
        pass

    @abstractmethod
    async def generate_avatar(
        self,
        source_image: bytes,
        style: str = "cartoon",
        custom_prompt: str = ""
    ) -> bytes:
        """
        Generate avatar from source image (upload or drawing).

        Args:
            source_image: Source image bytes (from upload or drawing)
            style: Avatar style (cartoon or realistic)
            custom_prompt: Optional custom instructions from user

        Returns:
            Avatar image bytes
        """
        pass

    @abstractmethod
    async def stylize_character(
        self,
        source_image: bytes,
        style: str = "cartoon"
    ) -> bytes:
        """
        Convert uploaded image or drawing to character.

        Returns:
            Stylized character image bytes
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the provider is accessible."""
        pass
