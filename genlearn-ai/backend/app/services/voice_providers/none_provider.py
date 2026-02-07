"""
None/Disabled Provider Implementations

These are placeholder providers that do nothing - used when voice features
are disabled via VOICE_TTS_PROVIDER=none or VOICE_STT_PROVIDER=none
"""

from .base import BaseTTSProvider, BaseSTTProvider


class NoneTTSProvider(BaseTTSProvider):
    """Disabled TTS provider - returns empty audio."""

    async def synthesize_speech(
        self,
        text: str,
        language: str = "en",
        voice_type: str = "female",
        speed: float = 1.0
    ) -> bytes:
        """Return empty audio bytes (voice feature disabled)."""
        return b""

    def get_supported_languages(self) -> list:
        """Return empty list - no languages supported."""
        return []

    async def health_check(self) -> bool:
        """Always healthy since it's intentionally disabled."""
        return True


class NoneSTTProvider(BaseSTTProvider):
    """Disabled STT provider - returns empty transcription."""

    async def transcribe_audio(
        self,
        audio_data: bytes,
        language: str = "en",
        audio_format: str = "wav"
    ) -> str:
        """Return empty string (voice feature disabled)."""
        return ""

    def get_supported_languages(self) -> list:
        """Return empty list - no languages supported."""
        return []

    async def health_check(self) -> bool:
        """Always healthy since it's intentionally disabled."""
        return True
