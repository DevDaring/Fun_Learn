"""
Google Cloud Platform Speech-to-Text Provider Implementation
Uses Application Default Credentials (ADC) for authentication
"""

import os
import httpx
import base64
from typing import Optional
from google.auth import default
from google.auth.transport.requests import Request
from .base import BaseSTTProvider


class GCPSTTProvider(BaseSTTProvider):
    """GCP Speech-to-Text implementation using OAuth2 tokens."""

    def __init__(self):
        self.project_id = os.getenv("GCP_PROJECT_ID", "gen-lang-client-0639252091")
        self.base_url = "https://speech.googleapis.com/v1"
        
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

    def _get_access_token(self) -> str:
        """Get OAuth2 access token using google-auth."""
        if not self.credentials.valid:
            self.credentials.refresh(Request())
        return self.credentials.token

    async def transcribe_audio(
        self,
        audio_data: bytes,
        language: str = "en",
        audio_format: str = "wav"
    ) -> str:
        """
        Convert speech audio to text using GCP Speech-to-Text.

        Args:
            audio_data: Audio data bytes
            language: Language code (en, hi, bn, etc.)
            audio_format: Audio format (wav, mp3, etc.)

        Returns:
            Transcribed text
        """
        url = f"{self.base_url}/speech:recognize"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._get_access_token()}"
        }

        # Convert audio to base64
        audio_content = base64.b64encode(audio_data).decode('utf-8')

        # Determine encoding
        encoding = self._get_encoding(audio_format)

        payload = {
            "config": {
                "encoding": encoding,
                "sampleRateHertz": 16000,  # Standard sample rate
                "languageCode": self._get_language_code(language),
                "enableAutomaticPunctuation": True,
                "model": "default",
                "useEnhanced": True
            },
            "audio": {
                "content": audio_content
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

            # Extract transcription
            if "results" in data and len(data["results"]) > 0:
                alternatives = data["results"][0].get("alternatives", [])
                if alternatives:
                    return alternatives[0].get("transcript", "")

            return ""

    def _get_encoding(self, audio_format: str) -> str:
        """Get GCP encoding type from audio format."""
        format_map = {
            "wav": "LINEAR16",
            "mp3": "MP3",
            "flac": "FLAC",
            "ogg": "OGG_OPUS",
            "webm": "WEBM_OPUS"
        }
        return format_map.get(audio_format.lower(), "LINEAR16")

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
            "zh": "cmn-Hans-CN"
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
        """Check if GCP STT API is accessible."""
        try:
            # Simple check - verify we can get an access token
            token = self._get_access_token()
            return token is not None and len(token) > 0
        except Exception:
            return False
