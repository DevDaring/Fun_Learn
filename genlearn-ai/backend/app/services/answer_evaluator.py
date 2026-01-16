"""
Answer Evaluator Service
Uses AI provider to evaluate descriptive answers and scores MCQ answers
"""

from typing import Any, Optional
from datetime import datetime

from app.services.provider_factory import ProviderFactory
from app.services.ai_providers.base import AnswerEvaluationRequest
from app.database.csv_handler import (
    get_scores_handler,
    get_mcq_questions_handler,
    get_descriptive_questions_handler,
    get_sessions_handler
)
from app.models.quiz import (
    MCQAnswerResult,
    DescriptiveAnswerResult,
    AnswerFeedback
)


class AnswerEvaluator:
    """
    Service for evaluating quiz answers.

    Responsibilities:
    - Evaluate MCQ answers (simple matching)
    - Evaluate descriptive answers using AI
    - Calculate points earned
    - Save answer records to CSV
    - Track answer statistics
    """

    def __init__(self):
        """Initialize the answer evaluator service."""
        self.ai_provider = ProviderFactory.get_ai_provider()
        self.scores_handler = get_scores_handler()
        self.mcq_handler = get_mcq_questions_handler()
        self.descriptive_handler = get_descriptive_questions_handler()
        self.sessions_handler = get_sessions_handler()

    async def evaluate_mcq_answer(
        self,
        session_id: str,
        user_id: str,
        question_id: str,
        selected_answer: str,
        time_taken_seconds: int
    ) -> MCQAnswerResult:
        """
        Evaluate an MCQ answer.

        Args:
            session_id: Session identifier
            user_id: User identifier
            question_id: Question identifier
            selected_answer: Selected option (A, B, C, or D)
            time_taken_seconds: Time taken to answer

        Returns:
            MCQ answer result with evaluation

        Raises:
            ValueError: If question not found
        """
        # Get question details
        question = self.mcq_handler.find_one({"question_id": question_id})
        if not question:
            raise ValueError(f"Question {question_id} not found")

        correct_answer = question.get("correct_answer", "A")
        is_correct = selected_answer.upper() == correct_answer.upper()

        # Calculate points (full points if correct, partial for participation)
        base_points = 10
        points_earned = base_points if is_correct else 2

        # Time bonus (up to 20% extra for quick answers)
        if is_correct and time_taken_seconds < 30:
            time_bonus = int(base_points * 0.2)
            points_earned += time_bonus

        # Save answer to scores CSV
        score_id = self.scores_handler.generate_id("SCR", "score_id")

        score_data = {
            "score_id": score_id,
            "user_id": user_id,
            "session_id": session_id,
            "question_id": question_id,
            "question_type": "mcq",
            "user_answer": selected_answer,
            "is_correct": is_correct,
            "points_earned": points_earned,
            "time_taken_seconds": time_taken_seconds,
            "evaluated_at": datetime.now().isoformat()
        }

        self.scores_handler.append(score_data)

        # Update session score
        self._update_session_score(session_id, points_earned)

        # Return result
        return MCQAnswerResult(
            question_id=question_id,
            selected_answer=selected_answer,
            correct_answer=correct_answer,
            is_correct=is_correct,
            explanation=question.get("explanation", ""),
            points_earned=points_earned,
            time_taken_seconds=time_taken_seconds
        )

    async def evaluate_descriptive_answer(
        self,
        session_id: str,
        user_id: str,
        question_id: str,
        user_answer: str,
        time_taken_seconds: int
    ) -> DescriptiveAnswerResult:
        """
        Evaluate a descriptive answer using AI.

        Args:
            session_id: Session identifier
            user_id: User identifier
            question_id: Question identifier
            user_answer: User's answer text
            time_taken_seconds: Time taken to answer

        Returns:
            Descriptive answer result with AI evaluation

        Raises:
            ValueError: If question not found
            Exception: If AI evaluation fails
        """
        # Get question details
        question = self.descriptive_handler.find_one({"question_id": question_id})
        if not question:
            raise ValueError(f"Question {question_id} not found")

        question_text = question.get("question_text", "")
        model_answer = question.get("model_answer", "")
        keywords_str = question.get("keywords", "")
        max_score = question.get("max_score", 10)

        # Parse keywords
        keywords = [k.strip() for k in keywords_str.split(",") if k.strip()]

        try:
            # Create evaluation request
            request = AnswerEvaluationRequest(
                question=question_text,
                model_answer=model_answer,
                user_answer=user_answer,
                keywords=keywords,
                max_score=max_score
            )

            # Get AI evaluation
            evaluation = await self.ai_provider.evaluate_answer(request)

            score = evaluation.get("score", 0)
            feedback_data = evaluation.get("feedback", {})

            # Calculate points earned (convert score to points)
            points_earned = score

            # Determine if answer is "correct" (scored above 50%)
            is_correct = score >= (max_score * 0.5)

            # Save answer to scores CSV
            score_id = self.scores_handler.generate_id("SCR", "score_id")

            score_data = {
                "score_id": score_id,
                "user_id": user_id,
                "session_id": session_id,
                "question_id": question_id,
                "question_type": "descriptive",
                "user_answer": user_answer,
                "is_correct": is_correct,
                "points_earned": points_earned,
                "time_taken_seconds": time_taken_seconds,
                "evaluated_at": datetime.now().isoformat(),
                "ai_score": score,
                "ai_feedback": str(feedback_data)
            }

            self.scores_handler.append(score_data)

            # Update session score
            self._update_session_score(session_id, points_earned)

            # Create feedback object
            feedback = AnswerFeedback(
                correct_points=feedback_data.get("correct_points", []),
                improvements=feedback_data.get("improvements", []),
                explanation=feedback_data.get("explanation", "")
            )

            return DescriptiveAnswerResult(
                question_id=question_id,
                user_answer=user_answer,
                score=score,
                max_score=max_score,
                feedback=feedback,
                points_earned=points_earned,
                time_taken_seconds=time_taken_seconds
            )

        except Exception as e:
            # Fallback: keyword-based evaluation if AI fails
            print(f"AI evaluation failed, using fallback: {e}")
            return await self._fallback_evaluation(
                session_id=session_id,
                user_id=user_id,
                question_id=question_id,
                question_text=question_text,
                user_answer=user_answer,
                keywords=keywords,
                max_score=max_score,
                time_taken_seconds=time_taken_seconds
            )

    async def _fallback_evaluation(
        self,
        session_id: str,
        user_id: str,
        question_id: str,
        question_text: str,
        user_answer: str,
        keywords: list,
        max_score: int,
        time_taken_seconds: int
    ) -> DescriptiveAnswerResult:
        """
        Fallback keyword-based evaluation when AI fails.

        Args:
            Various parameters for evaluation

        Returns:
            Descriptive answer result
        """
        # Simple keyword matching
        user_answer_lower = user_answer.lower()
        keywords_found = sum(1 for keyword in keywords if keyword.lower() in user_answer_lower)

        # Score based on keyword coverage
        if len(keywords) > 0:
            score = int((keywords_found / len(keywords)) * max_score)
        else:
            score = int(max_score * 0.5)  # Give half credit if no keywords

        points_earned = score
        is_correct = score >= (max_score * 0.5)

        # Generate simple feedback
        feedback = AnswerFeedback(
            correct_points=[f"Found {keywords_found} relevant keywords"],
            improvements=["Try to include more key concepts from the lesson"],
            explanation=f"Your answer included {keywords_found} out of {len(keywords)} key concepts."
        )

        # Save to database
        score_id = self.scores_handler.generate_id("SCR", "score_id")

        score_data = {
            "score_id": score_id,
            "user_id": user_id,
            "session_id": session_id,
            "question_id": question_id,
            "question_type": "descriptive",
            "user_answer": user_answer,
            "is_correct": is_correct,
            "points_earned": points_earned,
            "time_taken_seconds": time_taken_seconds,
            "evaluated_at": datetime.now().isoformat(),
            "ai_score": score,
            "ai_feedback": "Keyword-based evaluation (fallback)"
        }

        self.scores_handler.append(score_data)
        self._update_session_score(session_id, points_earned)

        return DescriptiveAnswerResult(
            question_id=question_id,
            user_answer=user_answer,
            score=score,
            max_score=max_score,
            feedback=feedback,
            points_earned=points_earned,
            time_taken_seconds=time_taken_seconds
        )

    async def evaluate_answer(
        self,
        question: str,
        model_answer: str,
        user_answer: str,
        keywords: list,
        max_score: int
    ) -> dict[str, Any]:
        """
        Evaluate a descriptive answer (route-compatible method).

        Args:
            question: Question text
            model_answer: Model answer
            user_answer: User's answer
            keywords: Expected keywords
            max_score: Maximum score

        Returns:
            Dictionary with score and feedback
        """
        try:
            request = AnswerEvaluationRequest(
                question=question,
                model_answer=model_answer,
                user_answer=user_answer,
                keywords=keywords,
                max_score=max_score
            )

            evaluation = await self.ai_provider.evaluate_answer(request)

            return {
                "score": evaluation.get("score", 0),
                "max_score": max_score,
                "feedback": evaluation.get("feedback", {
                    "correct_points": [],
                    "improvements": [],
                    "explanation": ""
                })
            }

        except Exception as e:
            # Fallback keyword-based evaluation
            user_answer_lower = user_answer.lower()
            keywords_found = sum(1 for keyword in keywords if keyword.lower() in user_answer_lower)

            if len(keywords) > 0:
                score = int((keywords_found / len(keywords)) * max_score)
            else:
                score = int(max_score * 0.5)

            return {
                "score": score,
                "max_score": max_score,
                "feedback": {
                    "correct_points": [f"Found {keywords_found} relevant keywords"],
                    "improvements": ["Try to include more key concepts"],
                    "explanation": f"Your answer included {keywords_found} key concepts."
                }
            }

    def _update_session_score(self, session_id: str, points: int) -> bool:
        """
        Update session total score.

        Args:
            session_id: Session identifier
            points: Points to add

        Returns:
            Success status
        """
        try:
            session = self.sessions_handler.find_one({"session_id": session_id})
            if session:
                current_score = session.get("score", 0)
                new_score = current_score + points

                return self.sessions_handler.update(
                    {"session_id": session_id},
                    {"score": new_score}
                )
            return False

        except Exception as e:
            print(f"Error updating session score: {e}")
            return False

    def get_session_answers(
        self,
        session_id: str
    ) -> dict[str, Any]:
        """
        Get all answers for a session.

        Args:
            session_id: Session identifier

        Returns:
            Dictionary with answer statistics
        """
        try:
            answers = self.scores_handler.find({"session_id": session_id})

            total_questions = len(answers)
            correct_answers = sum(1 for a in answers if a.get("is_correct", False))
            total_points = sum(a.get("points_earned", 0) for a in answers)

            mcq_answers = [a for a in answers if a.get("question_type") == "mcq"]
            descriptive_answers = [a for a in answers if a.get("question_type") == "descriptive"]

            return {
                "session_id": session_id,
                "total_questions": total_questions,
                "correct_answers": correct_answers,
                "total_points": total_points,
                "accuracy_rate": (correct_answers / total_questions * 100) if total_questions > 0 else 0,
                "mcq_count": len(mcq_answers),
                "descriptive_count": len(descriptive_answers),
                "answers": answers
            }

        except Exception as e:
            print(f"Error getting session answers: {e}")
            return {
                "session_id": session_id,
                "total_questions": 0,
                "correct_answers": 0,
                "total_points": 0,
                "accuracy_rate": 0,
                "mcq_count": 0,
                "descriptive_count": 0,
                "answers": []
            }

    def get_user_answer_history(
        self,
        user_id: str,
        limit: int = 50
    ) -> list:
        """
        Get answer history for a user.

        Args:
            user_id: User identifier
            limit: Maximum number of answers to return

        Returns:
            List of answer records
        """
        try:
            answers = self.scores_handler.find({"user_id": user_id})

            # Sort by evaluated_at (most recent first)
            answers.sort(key=lambda x: x.get("evaluated_at", ""), reverse=True)

            return answers[:limit]

        except Exception as e:
            print(f"Error getting answer history: {e}")
            return []

    async def health_check(self) -> dict[str, Any]:
        """
        Check health of answer evaluator service.

        Returns:
            Health status dictionary
        """
        try:
            ai_healthy = await self.ai_provider.health_check()

            return {
                "service": "AnswerEvaluator",
                "status": "healthy" if ai_healthy else "degraded",
                "ai_provider": "healthy" if ai_healthy else "unhealthy",
                "fallback": "keyword-based evaluation available"
            }
        except Exception as e:
            return {
                "service": "AnswerEvaluator",
                "status": "unhealthy",
                "error": str(e)
            }
