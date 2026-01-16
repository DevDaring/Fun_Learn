"""
Azure Voice Services Provider Implementation (Fallback)
"""

import os
import httpx
from typing import Optional
from .base import BaseTTSProvider, BaseSTTProvider


class AzureTTSProvider(BaseTTSProvider):
    """Azure Text-to-Speech implementation (fallback option)."""

    def __init__(self):
        self.api_key = os.getenv("AZURE_SPEECH_KEY")
        self.region = os.getenv("AZURE_SPEECH_REGION", "eastus")
        self.base_url = f"https://{self.region}.tts.speech.microsoft.com"

        if not self.api_key:
            raise ValueError("AZURE_SPEECH_KEY environment variable not set")

        # Voice mappings for different languages and genders
        self.voice_map = {
            "en": {
                "female": "en-US-JennyNeural",
                "male": "en-US-GuyNeural"
            },
            "hi": {
                "female": "hi-IN-SwaraNeural",
                "male": "hi-IN-MadhurNeural"
            },
            "bn": {
                "female": "bn-IN-TanishaaNeural",
                "male": "bn-IN-BashkarNeural"
            },
            "es": {
                "female": "es-US-PalomaNeural",
                "male": "es-US-AlonsoNeural"
            },
            "fr": {
                "female": "fr-FR-DeniseNeural",
                "male": "fr-FR-HenriNeural"
            },
            "de": {
                "female": "de-DE-KatjaNeural",
                "male": "de-DE-ConradNeural"
            },
            "ja": {
                "female": "ja-JP-NanamiNeural",
                "male": "ja-JP-KeitaNeural"
            },
            "zh": {
                "female": "zh-CN-XiaoxiaoNeural",
                "male": "zh-CN-YunxiNeural"
            }
        }

    async def synthesize_speech(
        self,
        text: str,
        language: str = "en",
        voice_type: str = "female",
        speed: float = 1.0
    ) -> bytes:
        """
        Convert text to speech using Azure TTS.

        Args:
            text: Text to convert to speech
            language: Language code (en, hi, bn, etc.)
            voice_type: Voice type (male or female)
            speed: Speech speed (0.5 to 2.0)

        Returns:
            Audio bytes (MP3 format)
        """
        url = f"{self.base_url}/cognitiveservices/v1"

        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3"
        }

        # Get voice name for language and gender
        voice_name = self._get_voice_name(language, voice_type)

        # Create SSML
        rate_percent = int((speed - 1.0) * 100)
        rate_str = f"+{rate_percent}%" if rate_percent >= 0 else f"{rate_percent}%"

        ssml = f"""<speak version='1.0' xml:lang='{self._get_language_code(language)}'>
    <voice name='{voice_name}'>
        <prosody rate='{rate_str}'>
            {text}
        </prosody>
    </voice>
</speak>"""

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=headers,
                content=ssml.encode('utf-8'),
                timeout=60.0
            )
            response.raise_for_status()

            return response.content

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
            "zh": "zh-CN"
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
        """Check if Azure TTS API is accessible."""
        try:
            await self.synthesize_speech("Hello", "en", "female", 1.0)
            return True
        except Exception:
            return False


class AzureSTTProvider(BaseSTTProvider):
    """Azure Speech-to-Text implementation (fallback option)."""

    def __init__(self):
        self.api_key = os.getenv("AZURE_SPEECH_KEY")
        self.region = os.getenv("AZURE_SPEECH_REGION", "eastus")
        self.base_url = f"https://{self.region}.stt.speech.microsoft.com"

        if not self.api_key:
            raise ValueError("AZURE_SPEECH_KEY environment variable not set")

    async def transcribe_audio(
        self,
        audio_data: bytes,
        language: str = "en",
        audio_format: str = "wav"
    ) -> str:
        """
        Convert speech audio to text using Azure STT.

        Args:
            audio_data: Audio data bytes
            language: Language code (en, hi, bn, etc.)
            audio_format: Audio format (wav, mp3, etc.)

        Returns:
            Transcribed text
        """
        url = f"{self.base_url}/speech/recognition/conversation/cognitiveservices/v1"

        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Content-Type": self._get_content_type(audio_format),
            "Accept": "application/json"
        }

        params = {
            "language": self._get_language_code(language),
            "format": "detailed"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=headers,
                params=params,
                content=audio_data,
                timeout=60.0
            )
            response.raise_for_status()

            data = response.json()

            # Extract transcription
            if data.get("RecognitionStatus") == "Success":
                return data.get("DisplayText", "")

            return ""

    def _get_content_type(self, audio_format: str) -> str:
        """Get content type from audio format."""
        format_map = {
            "wav": "audio/wav",
            "mp3": "audio/mp3",
            "ogg": "audio/ogg",
            "webm": "audio/webm"
        }
        return format_map.get(audio_format.lower(), "audio/wav")

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
            "zh": "zh-CN"
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
        """Check if Azure STT API is accessible."""
        try:
            # Create a minimal valid audio sample
            import struct
            sample_rate = 16000
            duration = 1
            num_samples = sample_rate * duration
            silence = struct.pack('<' + 'h' * num_samples, *([0] * num_samples))

            # WAV header
            wav_header = struct.pack(
                '<4sI4s4sIHHIIHH4sI',
                b'RIFF',
                36 + len(silence),
                b'WAVE',
                b'fmt ',
                16,
                1,
                1,
                sample_rate,
                sample_rate * 2,
                2,
                16,
                b'data',
                len(silence)
            )

            test_audio = wav_header + silence

            # Try to transcribe
            await self.transcribe_audio(test_audio, "en", "wav")
            return True
        except Exception:
            return False
