"""
Google Cloud Platform Text-to-Speech Provider Implementation
Uses Application Default Credentials (ADC) for authentication
"""

import os
import httpx
import base64
from typing import Optional
from google.auth import default
from google.auth.transport.requests import Request
from .base import BaseTTSProvider


class GCPTTSProvider(BaseTTSProvider):
    """GCP Text-to-Speech implementation using OAuth2 tokens."""

    def __init__(self):
        self.project_id = os.getenv("GCP_PROJECT_ID", "gen-lang-client-0639252091")
        self.base_url = "https://texttospeech.googleapis.com/v1"
        
        # Get credentials using ADC
        try:
            self.credentials, project = default()
            if not self.credentials.valid:
                self.credentials.refresh(Request())
        except Exception as e:
            raise ValueError(
                f"Cannot get GCP credentials. Please run: gcloud auth application-default login\n"
                f"Error: {e}"
            )

        # Voice mappings for different languages and genders
        self.voice_map = {
            "en": {
                "female": "en-US-Neural2-F",
                "male": "en-US-Neural2-D"
            },
            "hi": {
                "female": "hi-IN-Neural2-A",
                "male": "hi-IN-Neural2-B"
            },
            "bn": {
                "female": "bn-IN-Standard-A",
                "male": "bn-IN-Standard-B"
            },
            "es": {
                "female": "es-US-Neural2-A",
                "male": "es-US-Neural2-B"
            },
            "fr": {
                "female": "fr-FR-Neural2-A",
                "male": "fr-FR-Neural2-B"
            },
            "de": {
                "female": "de-DE-Neural2-F",
                "male": "de-DE-Neural2-D"
            },
            "ja": {
                "female": "ja-JP-Neural2-B",
                "male": "ja-JP-Neural2-C"
            },
            "zh": {
                "female": "cmn-CN-Standard-A",
                "male": "cmn-CN-Standard-B"
            }
        }

    def _get_access_token(self) -> str:
        """Get OAuth2 access token using google-auth."""
        if not self.credentials.valid:
            self.credentials.refresh(Request())
        return self.credentials.token

    async def synthesize_speech(
        self,
        text: str,
        language: str = "en",
        voice_type: str = "female",
        speed: float = 1.0
    ) -> bytes:
        """
        Convert text to speech using GCP Text-to-Speech.

        Args:
            text: Text to convert to speech
            language: Language code (en, hi, bn, etc.)
            voice_type: Voice type (male or female)
            speed: Speech speed (0.25 to 4.0)

        Returns:
            Audio bytes (MP3 format)
        """
        url = f"{self.base_url}/text:synthesize"
        
        # Get fresh access token
        access_token = self._get_access_token()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
            "x-goog-user-project": self.project_id
        }

        # Get voice name for language and gender
        voice_name = self._get_voice_name(language, voice_type)

        payload = {
            "input": {
                "text": text
            },
            "voice": {
                "languageCode": self._get_language_code(language),
                "name": voice_name
            },
            "audioConfig": {
                "audioEncoding": "MP3",
                "speakingRate": speed,
                "pitch": 0.0,
                "volumeGainDb": 0.0
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=headers,
                json=payload,
                timeout=60.0
            )
            response.raise_for_status()

            data = response.json()

            # GCP returns base64 encoded audio
            audio_content = data.get("audioContent")
            if not audio_content:
                raise ValueError("No audio content in GCP TTS response")

            return base64.b64decode(audio_content)

    def _get_voice_name(self, language: str, voice_type: str) -> str:
        """Get appropriate voice name for language and type."""
        lang_voices = self.voice_map.get(language, self.voice_map["en"])
        return lang_voices.get(voice_type, lang_voices["female"])

    def _get_language_code(self, language: str) -> str:
        """Convert short language code to full language code."""
        language_codes = {
            "en": "en-US",
            "hi": "hi-IN",
            "bn": "bn-IN",
            "es": "es-US",
            "fr": "fr-FR",
            "de": "de-DE",
            "ja": "ja-JP",
            "zh": "cmn-CN"
        }
        return language_codes.get(language, "en-US")

    def get_supported_languages(self) -> list:
        """Get list of supported language codes."""
        return [
            "en",  # English
            "hi",  # Hindi
            "bn",  # Bengali
            "es",  # Spanish
            "fr",  # French
            "de",  # German
            "ja",  # Japanese
            "zh",  # Chinese (Mandarin)
        ]

    async def health_check(self) -> bool:
        """Check if GCP TTS API is accessible."""
        try:
            # Try to synthesize a simple phrase
            await self.synthesize_speech("Hello", "en", "female", 1.0)
            return True
        except Exception:
            return False
