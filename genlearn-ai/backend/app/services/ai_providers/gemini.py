"""
Google Gemini AI Provider Implementation
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


class GeminiProvider(BaseAIProvider):
    """Gemini 3 Pro Preview implementation of AI provider using latest models."""

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        # Use Gemini 3 Pro Preview - the latest model
        self.model = os.getenv("GEMINI_MODEL", "gemini-3-pro-preview")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")

    async def _call_api(self, prompt: str, system_instruction: str = "") -> str:
        """Make API call to Gemini."""
        url = f"{self.base_url}/models/{self.model}:generateContent"

        headers = {
            "Content-Type": "application/json",
        }

        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 8192,
            }
        }

        if system_instruction:
            payload["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
            }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{url}?key={self.api_key}",
                headers=headers,
                json=payload,
                timeout=60.0
            )
            response.raise_for_status()

            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]

    async def generate_content_with_image(self, prompt: str, image_base64: str) -> dict:
        """Generate content from prompt + image using Gemini's multimodal capabilities."""
        url = f"{self.base_url}/models/{self.model}:generateContent"

        headers = {
            "Content-Type": "application/json",
        }

        # Multimodal payload with text and image
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": image_base64
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 8192,
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{url}?key={self.api_key}",
                headers=headers,
                json=payload,
                timeout=90.0  # Longer timeout for image processing
            )
            response.raise_for_status()

            data = response.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return {"text": text}

    async def generate_text(self, prompt: str) -> dict:
        """Simple text generation from a prompt string. Returns dict with 'text' key."""
        try:
            text = await self._call_api(prompt)
            return {"text": text}
        except Exception as e:
            raise Exception(f"Gemini text generation failed: {str(e)}")

    async def generate_content(
        self,
        request: ContentGenerationRequest
    ) -> dict[str, Any]:
        """Generate learning content with story narratives and quizzes."""

        # Story style descriptions for prompt engineering
        story_style_prompts = {
            "thriller": "Write in a suspenseful, edge-of-your-seat style with dramatic tension, cliffhangers, and mysterious elements. Build anticipation and keep the reader hooked.",
            "fun": "Write in a light-hearted, entertaining style with humor, playful language, and positive energy. Make learning feel like a fun adventure.",
            "nostalgic": "Write in a warm, classic storytelling style evoking memories and timeless wisdom. Use gentle, comforting language like a beloved storybook.",
            "adventure": "Write in an epic, journey-focused style with exploration, discoveries, and heroic moments. Make the learner feel like they're on an exciting quest.",
            "mystery": "Write in an investigative style with clues, puzzles, and revelations. Build curiosity and encourage the learner to piece together information.",
            "scifi": "Write in a futuristic, technological style with innovation, space themes, and scientific wonder. Make concepts feel cutting-edge and revolutionary."
        }

        story_style_instruction = story_style_prompts.get(
            request.story_style, 
            story_style_prompts["fun"]
        )

        system_instruction = f"""You are an expert educational content creator who writes engaging stories.
        {story_style_instruction}
        Create age-appropriate learning content that incorporates educational facts naturally into the narrative.
        Always respond with valid JSON only, no markdown formatting."""

        avatar_context = ""
        if request.avatar_description:
            avatar_context = f"The main protagonist is the learner's avatar: {request.avatar_description}. "

        character_context = ""
        if request.character_descriptions:
            chars = ", ".join(request.character_descriptions)
            character_context = f"Include these supporting characters in the story: {chars}. "

        prompt = f"""Create an educational {request.story_style} story about "{request.topic}" for difficulty level {request.difficulty_level}/10.

{avatar_context}{character_context}

Generate exactly {request.num_images} story segments. Each segment should:
1. Tell part of an engaging {request.story_style} narrative
2. Teach something important about {request.topic}
3. Include a scene description for {request.visual_style} style image generation (NO TEXT IN IMAGE)
4. Have a text overlay (dialogue or caption) to show ON the image
5. End with a quiz question about what was taught

CRITICAL: Image prompts must NOT include any text, letters, or words. Text will be overlaid separately.

Respond with ONLY this JSON structure (no markdown, no code blocks):
{{
    "story_segments": [
        {{
            "segment_number": 1,
            "narrative": "The engaging story paragraph (3-5 sentences) teaching about the topic in {request.story_style} style",
            "scene_description": "Detailed visual scene description for {request.visual_style} image. Include characters, setting, action. NO TEXT OR WORDS in the image.",
            "text_overlay": {{
                "text": "Short dialogue or caption text (max 15 words) to display on the image",
                "position": "bottom",
                "style": "caption"
            }},
            "quiz": {{
                "question_text": "A question testing what was taught in this segment?",
                "options": [
                    {{"key": "A", "text": "First option"}},
                    {{"key": "B", "text": "Second option (correct)"}},
                    {{"key": "C", "text": "Third option"}},
                    {{"key": "D", "text": "Fourth option"}}
                ],
                "correct_answers": ["B"],
                "explanation": "Why B is correct - what the learner should understand",
                "is_multi_select": false,
                "points": 10
            }}
        }}
    ],
    "topic_summary": "Brief summary of what was covered across all segments"
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
        """Check if Gemini API is accessible."""
        try:
            await self._call_api("Say 'OK' if you can read this.")
            return True
        except Exception:
            return False
