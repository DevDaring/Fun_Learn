"""
Voice Routes - Text-to-Speech and Speech-to-Text
"""

from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form
from fastapi.responses import Response
from pydantic import BaseModel

from app.api.dependencies import get_current_user
from app.services.provider_factory import ProviderFactory

router = APIRouter()


class TTSRequest(BaseModel):
    """Text-to-Speech request model"""
    text: str
    language: str = "en"
    voice_type: str = "female"
    speed: float = 1.0


class STTResponse(BaseModel):
    """Speech-to-Text response model"""
    transcribed_text: str
    language: str


@router.post("/tts", status_code=status.HTTP_200_OK)
async def text_to_speech(
    tts_request: TTSRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Convert text to speech audio

    Args:
        tts_request: Text and voice preferences
        current_user: Authenticated user

    Returns:
        Audio file (MP3)
    """
    try:
        # Get TTS provider
        tts_provider = ProviderFactory.get_tts_provider()

        # Generate speech
        audio_data = await tts_provider.synthesize_speech(
            text=tts_request.text,
            language=tts_request.language,
            voice_type=tts_request.voice_type,
            speed=tts_request.speed
        )

        # Return audio as response
        return Response(
            content=audio_data,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "attachment; filename=speech.mp3"
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating speech: {str(e)}"
        )


@router.post("/stt", response_model=STTResponse, status_code=status.HTTP_200_OK)
async def speech_to_text(
    audio: UploadFile = File(...),
    language: str = Form("en"),
    current_user: dict = Depends(get_current_user)
):
    """
    Convert speech audio to text

    Args:
        audio: Audio file
        language: Language code
        current_user: Authenticated user

    Returns:
        Transcribed text
    """
    try:
        # Read audio file
        audio_data = await audio.read()

        # Get STT provider
        stt_provider = ProviderFactory.get_stt_provider()

        # Transcribe audio
        transcribed_text = await stt_provider.transcribe_audio(
            audio_data=audio_data,
            language=language,
            audio_format="wav"  # Assume WAV format, can be made dynamic
        )

        return {
            "transcribed_text": transcribed_text,
            "language": language
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error transcribing audio: {str(e)}"
        )
