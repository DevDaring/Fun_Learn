"""
Question Generator Service
Uses AI provider to generate MCQ and descriptive questions
"""

from typing import Any, Optional
from datetime import datetime

from app.services.provider_factory import ProviderFactory
from app.services.ai_providers.base import QuestionGenerationRequest
from app.database.csv_handler import (
    get_sessions_handler,
    get_mcq_questions_handler,
    get_descriptive_questions_handler
)
from app.models.quiz import (
    MCQQuestion,
    MCQQuestionCreate,
    DescriptiveQuestion,
    DescriptiveQuestionCreate
)


class QuestionGenerator:
    """
    Service for generating quiz questions using AI.

    Responsibilities:
    - Generate MCQ questions based on learning content
    - Generate descriptive questions based on learning content
    - Save generated questions to CSV database
    - Retrieve questions for sessions
    """

    def __init__(self):
        """Initialize the question generator service."""
        self.ai_provider = ProviderFactory.get_ai_provider()
        self.sessions_handler = get_sessions_handler()
        self.mcq_handler = get_mcq_questions_handler()
        self.descriptive_handler = get_descriptive_questions_handler()

    async def generate_questions_for_session(
        self,
        session_id: str,
        content_context: str,
        num_mcq: int = 3,
        num_descriptive: int = 3
    ) -> dict[str, Any]:
        """
        Generate both MCQ and descriptive questions for a session.

        Args:
            session_id: Session identifier
            content_context: The learning content/story that was presented
            num_mcq: Number of MCQ questions to generate
            num_descriptive: Number of descriptive questions to generate

        Returns:
            Dictionary with generated questions

        Raises:
            Exception: If question generation fails
        """
        try:
            # Get session details
            session = self.sessions_handler.find_one({"session_id": session_id})
            if not session:
                raise ValueError(f"Session {session_id} not found")

            topic = session.get("topic", "")
            difficulty_level = session.get("difficulty_level", 5)
            user_id = session.get("user_id", "system")

            # Create request for AI provider
            request = QuestionGenerationRequest(
                topic=topic,
                difficulty_level=difficulty_level,
                content_context=content_context,
                num_mcq=num_mcq,
                num_descriptive=num_descriptive
            )

            # Generate MCQ questions
            mcq_questions = await self._generate_mcq_questions(
                request=request,
                session_id=session_id,
                user_id=user_id
            )

            # Generate descriptive questions
            descriptive_questions = await self._generate_descriptive_questions(
                request=request,
                session_id=session_id,
                user_id=user_id
            )

            return {
                "session_id": session_id,
                "mcq_questions": mcq_questions,
                "descriptive_questions": descriptive_questions,
                "total_questions": len(mcq_questions) + len(descriptive_questions)
            }

        except Exception as e:
            raise Exception(f"Failed to generate questions: {str(e)}")

    async def _generate_mcq_questions(
        self,
        request: QuestionGenerationRequest,
        session_id: str,
        user_id: str
    ) -> list[dict[str, Any]]:
        """
        Generate and save MCQ questions.

        Args:
            request: Question generation request
            session_id: Session identifier
            user_id: User identifier

        Returns:
            List of generated MCQ questions
        """
        try:
            # Generate questions using AI
            mcq_data = await self.ai_provider.generate_mcq_questions(request)

            saved_questions = []

            for question_data in mcq_data:
                # Generate unique question ID
                question_id = self.mcq_handler.generate_id("MCQ", "question_id")

                # Prepare question data for CSV
                question_csv = {
                    "question_id": question_id,
                    "topic": request.topic,
                    "difficulty_level": request.difficulty_level,
                    "question_text": question_data.get("question", ""),
                    "option_a": question_data.get("options", {}).get("A", ""),
                    "option_b": question_data.get("options", {}).get("B", ""),
                    "option_c": question_data.get("options", {}).get("C", ""),
                    "option_d": question_data.get("options", {}).get("D", ""),
                    "correct_answer": question_data.get("correct_answer", "A"),
                    "explanation": question_data.get("explanation", ""),
                    "created_by": user_id,
                    "is_ai_generated": True,
                    "created_at": datetime.now().isoformat(),
                    "session_id": session_id  # Link to session
                }

                # Save to CSV
                if self.mcq_handler.append(question_csv):
                    saved_questions.append({
                        "question_id": question_id,
                        "question_text": question_data.get("question", ""),
                        "options": question_data.get("options", {}),
                        "correct_answer": question_data.get("correct_answer", "A"),
                        "explanation": question_data.get("explanation", "")
                    })

            return saved_questions

        except Exception as e:
            print(f"Error generating MCQ questions: {e}")
            return []

    async def _generate_descriptive_questions(
        self,
        request: QuestionGenerationRequest,
        session_id: str,
        user_id: str
    ) -> list[dict[str, Any]]:
        """
        Generate and save descriptive questions.

        Args:
            request: Question generation request
            session_id: Session identifier
            user_id: User identifier

        Returns:
            List of generated descriptive questions
        """
        try:
            # Generate questions using AI
            descriptive_data = await self.ai_provider.generate_descriptive_questions(request)

            saved_questions = []

            for question_data in descriptive_data:
                # Generate unique question ID
                question_id = self.descriptive_handler.generate_id("DSC", "question_id")

                # Convert keywords list to comma-separated string
                keywords = question_data.get("keywords", [])
                keywords_str = ",".join(keywords) if isinstance(keywords, list) else keywords

                # Prepare question data for CSV
                question_csv = {
                    "question_id": question_id,
                    "topic": request.topic,
                    "difficulty_level": request.difficulty_level,
                    "question_text": question_data.get("question", ""),
                    "model_answer": question_data.get("model_answer", ""),
                    "keywords": keywords_str,
                    "max_score": question_data.get("max_score", 10),
                    "created_by": user_id,
                    "is_ai_generated": True,
                    "created_at": datetime.now().isoformat(),
                    "session_id": session_id  # Link to session
                }

                # Save to CSV
                if self.descriptive_handler.append(question_csv):
                    saved_questions.append({
                        "question_id": question_id,
                        "question_text": question_data.get("question", ""),
                        "model_answer": question_data.get("model_answer", ""),
                        "keywords": keywords,
                        "max_score": question_data.get("max_score", 10)
                    })

            return saved_questions

        except Exception as e:
            print(f"Error generating descriptive questions: {e}")
            return []

    async def generate_mcq_questions(
        self,
        topic: str,
        difficulty_level: int,
        content_context: str,
        num_questions: int = 3
    ) -> list[dict[str, Any]]:
        """
        Generate MCQ questions (route-compatible method).

        Args:
            topic: Topic for questions
            difficulty_level: Difficulty level (1-10)
            content_context: Context for questions
            num_questions: Number of questions to generate

        Returns:
            List of MCQ questions
        """
        request = QuestionGenerationRequest(
            topic=topic,
            difficulty_level=difficulty_level,
            content_context=content_context,
            num_mcq=num_questions,
            num_descriptive=0
        )

        return await self._generate_mcq_questions(
            request=request,
            session_id="temp",
            user_id="system"
        )

    async def generate_descriptive_questions(
        self,
        topic: str,
        difficulty_level: int,
        content_context: str,
        num_questions: int = 3
    ) -> list[dict[str, Any]]:
        """
        Generate descriptive questions (route-compatible method).

        Args:
            topic: Topic for questions
            difficulty_level: Difficulty level (1-10)
            content_context: Context for questions
            num_questions: Number of questions to generate

        Returns:
            List of descriptive questions
        """
        request = QuestionGenerationRequest(
            topic=topic,
            difficulty_level=difficulty_level,
            content_context=content_context,
            num_mcq=0,
            num_descriptive=num_questions
        )

        return await self._generate_descriptive_questions(
            request=request,
            session_id="temp",
            user_id="system"
        )

    async def get_mcq_questions_for_session(
        self,
        session_id: str
    ) -> list[dict[str, Any]]:
        """
        Get MCQ questions for a session (without answers).

        Args:
            session_id: Session identifier

        Returns:
            List of MCQ questions for display
        """
        try:
            questions = self.mcq_handler.find({"session_id": session_id})

            # Format for display (hide correct answer)
            display_questions = []
            for q in questions:
                display_questions.append({
                    "question_id": q.get("question_id"),
                    "question_text": q.get("question_text"),
                    "options": {
                        "A": q.get("option_a"),
                        "B": q.get("option_b"),
                        "C": q.get("option_c"),
                        "D": q.get("option_d")
                    }
                })

            return display_questions

        except Exception as e:
            print(f"Error retrieving MCQ questions: {e}")
            return []

    async def get_descriptive_questions_for_session(
        self,
        session_id: str
    ) -> list[dict[str, Any]]:
        """
        Get descriptive questions for a session.

        Args:
            session_id: Session identifier

        Returns:
            List of descriptive questions for display
        """
        try:
            questions = self.descriptive_handler.find({"session_id": session_id})

            # Format for display
            display_questions = []
            for q in questions:
                display_questions.append({
                    "question_id": q.get("question_id"),
                    "question_text": q.get("question_text"),
                    "max_score": q.get("max_score", 10)
                })

            return display_questions

        except Exception as e:
            print(f"Error retrieving descriptive questions: {e}")
            return []

    def get_mcq_question_by_id(self, question_id: str) -> Optional[dict[str, Any]]:
        """
        Get a specific MCQ question by ID.

        Args:
            question_id: Question identifier

        Returns:
            Question data or None
        """
        return self.mcq_handler.find_one({"question_id": question_id})

    def get_descriptive_question_by_id(self, question_id: str) -> Optional[dict[str, Any]]:
        """
        Get a specific descriptive question by ID.

        Args:
            question_id: Question identifier

        Returns:
            Question data or None
        """
        question = self.descriptive_handler.find_one({"question_id": question_id})

        if question and "keywords" in question:
            # Convert comma-separated keywords back to list
            keywords_str = question.get("keywords", "")
            question["keywords"] = [k.strip() for k in keywords_str.split(",") if k.strip()]

        return question

    async def upload_mcq_questions(
        self,
        questions: list[MCQQuestionCreate],
        created_by: str
    ) -> dict[str, Any]:
        """
        Upload pre-created MCQ questions (admin function).

        Args:
            questions: List of MCQ questions to upload
            created_by: User ID of uploader

        Returns:
            Upload result summary
        """
        try:
            uploaded_count = 0

            for question in questions:
                question_id = self.mcq_handler.generate_id("MCQ", "question_id")

                question_data = {
                    "question_id": question_id,
                    "topic": question.topic,
                    "difficulty_level": question.difficulty_level,
                    "question_text": question.question_text,
                    "option_a": question.option_a,
                    "option_b": question.option_b,
                    "option_c": question.option_c,
                    "option_d": question.option_d,
                    "correct_answer": question.correct_answer,
                    "explanation": question.explanation,
                    "created_by": created_by,
                    "is_ai_generated": False,
                    "created_at": datetime.now().isoformat()
                }

                if self.mcq_handler.append(question_data):
                    uploaded_count += 1

            return {
                "success": True,
                "uploaded": uploaded_count,
                "total": len(questions)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "uploaded": 0,
                "total": len(questions)
            }

    async def upload_descriptive_questions(
        self,
        questions: list[DescriptiveQuestionCreate],
        created_by: str
    ) -> dict[str, Any]:
        """
        Upload pre-created descriptive questions (admin function).

        Args:
            questions: List of descriptive questions to upload
            created_by: User ID of uploader

        Returns:
            Upload result summary
        """
        try:
            uploaded_count = 0

            for question in questions:
                question_id = self.descriptive_handler.generate_id("DSC", "question_id")

                # Convert keywords list to string
                keywords_str = ",".join(question.keywords) if isinstance(question.keywords, list) else question.keywords

                question_data = {
                    "question_id": question_id,
                    "topic": question.topic,
                    "difficulty_level": question.difficulty_level,
                    "question_text": question.question_text,
                    "model_answer": question.model_answer,
                    "keywords": keywords_str,
                    "max_score": question.max_score,
                    "created_by": created_by,
                    "is_ai_generated": False,
                    "created_at": datetime.now().isoformat()
                }

                if self.descriptive_handler.append(question_data):
                    uploaded_count += 1

            return {
                "success": True,
                "uploaded": uploaded_count,
                "total": len(questions)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "uploaded": 0,
                "total": len(questions)
            }

    async def health_check(self) -> dict[str, Any]:
        """
        Check health of question generator service.

        Returns:
            Health status dictionary
        """
        try:
            ai_healthy = await self.ai_provider.health_check()

            return {
                "service": "QuestionGenerator",
                "status": "healthy" if ai_healthy else "degraded",
                "ai_provider": "healthy" if ai_healthy else "unhealthy"
            }
        except Exception as e:
            return {
                "service": "QuestionGenerator",
                "status": "unhealthy",
                "error": str(e)
            }
