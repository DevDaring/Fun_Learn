"""
Base Voice Provider Interfaces
"""

from abc import ABC, abstractmethod
from typing import Optional


class BaseTTSProvider(ABC):
    """Abstract base class for Text-to-Speech providers."""

    @abstractmethod
    async def synthesize_speech(
        self,
        text: str,
        language: str = "en",
        voice_type: str = "female",  # "male" or "female"
        speed: float = 1.0
    ) -> bytes:
        """
        Convert text to speech audio.

        Returns:
            Audio bytes (MP3 format)
        """
        pass

    @abstractmethod
    def get_supported_languages(self) -> list:
        """Get list of supported language codes."""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the provider is accessible."""
        pass


class BaseSTTProvider(ABC):
    """Abstract base class for Speech-to-Text providers."""

    @abstractmethod
    async def transcribe_audio(
        self,
        audio_data: bytes,
        language: str = "en",
        audio_format: str = "wav"
    ) -> str:
        """
        Convert speech audio to text.

        Returns:
            Transcribed text
        """
        pass

    @abstractmethod
    def get_supported_languages(self) -> list:
        """Get list of supported language codes."""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the provider is accessible."""
        pass
