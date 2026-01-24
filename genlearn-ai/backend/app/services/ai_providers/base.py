"""
Base AI Provider Interface

All AI providers must implement this interface.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional
from pydantic import BaseModel


class ContentGenerationRequest(BaseModel):
    topic: str
    difficulty_level: int  # 1-10
    visual_style: str  # "cartoon" or "realistic"
    story_style: str = "fun"  # "thriller", "fun", "nostalgic", "adventure", "mystery", "scifi"
    num_images: int = 3
    avatar_description: Optional[str] = None
    character_descriptions: Optional[list[str]] = None


class QuestionGenerationRequest(BaseModel):
    topic: str
    difficulty_level: int
    content_context: str  # The story/content that was shown
    num_mcq: int = 3
    num_descriptive: int = 3


class AnswerEvaluationRequest(BaseModel):
    question: str
    model_answer: str
    user_answer: str
    keywords: list[str]
    max_score: int = 10


class BaseAIProvider(ABC):
    """Abstract base class for AI providers."""

    @abstractmethod
    async def generate_content(
        self,
        request: ContentGenerationRequest
    ) -> dict[str, Any]:
        """
        Generate learning content including story narratives and facts.

        Returns:
            {
                "story_segments": [
                    {"narrative": "...", "facts": ["...", "..."], "image_prompt": "..."},
                    ...
                ],
                "topic_summary": "..."
            }
        """
        pass

    @abstractmethod
    async def generate_mcq_questions(
        self,
        request: QuestionGenerationRequest
    ) -> list[dict[str, Any]]:
        """
        Generate multiple choice questions.

        Returns:
            [
                {
                    "question": "...",
                    "options": {"A": "...", "B": "...", "C": "...", "D": "..."},
                    "correct_answer": "B",
                    "explanation": "..."
                },
                ...
            ]
        """
        pass

    @abstractmethod
    async def generate_descriptive_questions(
        self,
        request: QuestionGenerationRequest
    ) -> list[dict[str, Any]]:
        """
        Generate descriptive/open-ended questions.

        Returns:
            [
                {
                    "question": "...",
                    "model_answer": "...",
                    "keywords": ["...", "..."],
                    "max_score": 10
                },
                ...
            ]
        """
        pass

    @abstractmethod
    async def evaluate_answer(
        self,
        request: AnswerEvaluationRequest
    ) -> dict[str, Any]:
        """
        Evaluate a descriptive answer.

        Returns:
            {
                "score": 8,
                "max_score": 10,
                "feedback": {
                    "correct_points": ["...", "..."],
                    "improvements": ["...", "..."],
                    "explanation": "..."
                }
            }
        """
        pass

    @abstractmethod
    async def chat(
        self,
        message: str,
        context: Optional[str] = None,
        language: str = "en"
    ) -> str:
        """
        General chat/conversation capability.

        Returns:
            Response text
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the provider is accessible."""
        pass
