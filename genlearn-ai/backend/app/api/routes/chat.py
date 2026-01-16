"""
Chat Routes - AI chat functionality
"""

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional

from app.api.dependencies import get_current_user
from app.services.provider_factory import ProviderFactory

router = APIRouter()


class ChatRequest(BaseModel):
    """Chat request model"""
    message: str
    context: Optional[str] = None
    language: Optional[str] = "en"


class ChatResponse(BaseModel):
    """Chat response model"""
    message: str
    language: str


@router.post("/message", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def send_chat_message(
    chat_request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Send a chat message and get AI response

    Args:
        chat_request: Chat message and optional context
        current_user: Authenticated user

    Returns:
        AI-generated response
    """
    try:
        # Get AI provider
        ai_provider = ProviderFactory.get_ai_provider()

        # Get response from AI
        response_text = await ai_provider.chat(
            message=chat_request.message,
            context=chat_request.context,
            language=chat_request.language or "en"
        )

        return {
            "message": response_text,
            "language": chat_request.language or "en"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat message: {str(e)}"
        )
