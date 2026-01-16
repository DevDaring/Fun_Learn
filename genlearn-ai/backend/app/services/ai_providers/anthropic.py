"""
Anthropic Claude Provider Implementation (Fallback)
"""

import os
import json
import httpx
from typing import Any, Optional
from .base import (
    BaseAIProvider,
    ContentGenerationRequest,
    QuestionGenerationRequest,
    AnswerEvaluationRequest
)


class AnthropicProvider(BaseAIProvider):
    """Anthropic Claude implementation of AI provider (fallback option)."""

    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
        self.base_url = "https://api.anthropic.com/v1"

        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    async def _call_api(self, prompt: str, system_instruction: str = "") -> str:
        """Make API call to Anthropic Claude."""
        url = f"{self.base_url}/messages"

        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01"
        }

        payload = {
            "model": self.model,
            "max_tokens": 8192,
            "temperature": 0.7,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        if system_instruction:
            payload["system"] = system_instruction

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=headers,
                json=payload,
                timeout=60.0
            )
            response.raise_for_status()

            data = response.json()
            return data["content"][0]["text"]

    async def generate_content(
        self,
        request: ContentGenerationRequest
    ) -> dict[str, Any]:
        """Generate learning content with story narratives."""

        system_instruction = """You are an expert educational content creator.
        Create engaging, age-appropriate learning content with storytelling elements.
        Always respond with valid JSON only, no markdown formatting."""

        avatar_context = ""
        if request.avatar_description:
            avatar_context = f"Include a character named after the learner's avatar: {request.avatar_description}. "

        character_context = ""
        if request.character_descriptions:
            chars = ", ".join(request.character_descriptions)
            character_context = f"Also include these characters in the story: {chars}. "

        prompt = f"""Create educational content about "{request.topic}" for difficulty level {request.difficulty_level}/10.

{avatar_context}{character_context}

Generate exactly {request.num_images} story segments in {request.visual_style} style.

Respond with ONLY this JSON structure (no markdown, no code blocks):
{{
    "story_segments": [
        {{
            "segment_number": 1,
            "narrative": "A short engaging story paragraph (2-3 sentences)",
            "facts": ["Fact 1 about the topic", "Fact 2 about the topic"],
            "image_prompt": "Detailed prompt for {request.visual_style} style image generation including characters and scene"
        }}
    ],
    "topic_summary": "Brief summary of what was covered"
}}"""

        response_text = await self._call_api(prompt, system_instruction)

        # Clean response and parse JSON
        response_text = response_text.strip()
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]

        return json.loads(response_text)

    async def generate_mcq_questions(
        self,
        request: QuestionGenerationRequest
    ) -> list[dict[str, Any]]:
        """Generate MCQ questions based on content."""

        system_instruction = """You are an expert quiz creator.
        Create challenging but fair multiple choice questions.
        Always respond with valid JSON only, no markdown formatting."""

        prompt = f"""Based on this learning content about "{request.topic}":

{request.content_context}

Create exactly {request.num_mcq} multiple choice questions at difficulty level {request.difficulty_level}/10.

Respond with ONLY this JSON array (no markdown, no code blocks):
[
    {{
        "question": "Clear question text?",
        "options": {{
            "A": "First option",
            "B": "Second option",
            "C": "Third option",
            "D": "Fourth option"
        }},
        "correct_answer": "B",
        "explanation": "Why B is correct and others are wrong"
    }}
]"""

        response_text = await self._call_api(prompt, system_instruction)

        response_text = response_text.strip()
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]

        return json.loads(response_text)

    async def generate_descriptive_questions(
        self,
        request: QuestionGenerationRequest
    ) -> list[dict[str, Any]]:
        """Generate descriptive questions."""

        system_instruction = """You are an expert assessment creator.
        Create open-ended questions that test deep understanding.
        Always respond with valid JSON only, no markdown formatting."""

        prompt = f"""Based on this learning content about "{request.topic}":

{request.content_context}

Create exactly {request.num_descriptive} descriptive questions at difficulty level {request.difficulty_level}/10.

Respond with ONLY this JSON array (no markdown, no code blocks):
[
    {{
        "question": "Open-ended question requiring explanation?",
        "model_answer": "Comprehensive model answer (3-5 sentences)",
        "keywords": ["key", "terms", "expected", "in", "answer"],
        "max_score": 10
    }}
]"""

        response_text = await self._call_api(prompt, system_instruction)

        response_text = response_text.strip()
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]

        return json.loads(response_text)

    async def evaluate_answer(
        self,
        request: AnswerEvaluationRequest
    ) -> dict[str, Any]:
        """Evaluate a descriptive answer using AI."""

        system_instruction = """You are an expert educational evaluator.
        Provide fair, constructive feedback on student answers.
        Always respond with valid JSON only, no markdown formatting."""

        prompt = f"""Evaluate this student answer:

Question: {request.question}

Model Answer: {request.model_answer}

Expected Keywords: {', '.join(request.keywords)}

Student's Answer: {request.user_answer}

Maximum Score: {request.max_score}

Evaluate fairly and respond with ONLY this JSON (no markdown, no code blocks):
{{
    "score": <number between 0 and {request.max_score}>,
    "max_score": {request.max_score},
    "feedback": {{
        "correct_points": ["Points the student got right"],
        "improvements": ["Areas that could be improved"],
        "explanation": "Detailed explanation of the score"
    }}
}}"""

        response_text = await self._call_api(prompt, system_instruction)

        response_text = response_text.strip()
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]

        return json.loads(response_text)

    async def chat(
        self,
        message: str,
        context: Optional[str] = None,
        language: str = "en"
    ) -> str:
        """General chat capability."""

        language_instruction = ""
        if language != "en":
            language_instruction = f"Respond in the language with code: {language}. "

        system_instruction = f"""You are a helpful AI learning assistant.
        {language_instruction}
        Be encouraging, clear, and educational in your responses."""

        prompt = message
        if context:
            prompt = f"Context: {context}\n\nUser message: {message}"

        return await self._call_api(prompt, system_instruction)

    async def health_check(self) -> bool:
        """Check if Anthropic API is accessible."""
        try:
            await self._call_api("Say 'OK' if you can read this.")
            return True
        except Exception:
            return False
