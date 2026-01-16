"""
Quiz Models - Pydantic models for questions and answers
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MCQOptions(BaseModel):
    """Multiple choice question options"""
    A: str
    B: str
    C: str
    D: str


class MCQQuestionBase(BaseModel):
    """Base MCQ question model"""
    topic: str = Field(..., min_length=1, max_length=200)
    difficulty_level: int = Field(..., ge=1, le=10)
    question_text: str = Field(..., min_length=10)
    option_a: str = Field(..., min_length=1)
    option_b: str = Field(..., min_length=1)
    option_c: str = Field(..., min_length=1)
    option_d: str = Field(..., min_length=1)
    correct_answer: str = Field(..., pattern="^[A-D]$")
    explanation: str = Field(..., min_length=10)


class MCQQuestionCreate(MCQQuestionBase):
    """Model for creating MCQ question"""
    created_by: str
    is_ai_generated: bool = False


class MCQQuestion(MCQQuestionBase):
    """Complete MCQ question model"""
    question_id: str
    created_by: str
    is_ai_generated: bool = False
    created_at: datetime
    image_url: Optional[str] = None

    class Config:
        from_attributes = True


class MCQQuestionDisplay(BaseModel):
    """MCQ question for display to users (without answer)"""
    question_id: str
    question_text: str
    options: MCQOptions
    image_url: Optional[str] = None


class MCQAnswerSubmit(BaseModel):
    """Model for submitting MCQ answer"""
    question_id: str
    selected_answer: str = Field(..., pattern="^[A-D]$")


class MCQAnswerResult(BaseModel):
    """Result of MCQ answer evaluation"""
    question_id: str
    selected_answer: str
    correct_answer: str
    is_correct: bool
    explanation: str
    points_earned: int
    time_taken_seconds: int


class DescriptiveQuestionBase(BaseModel):
    """Base descriptive question model"""
    topic: str = Field(..., min_length=1, max_length=200)
    difficulty_level: int = Field(..., ge=1, le=10)
    question_text: str = Field(..., min_length=10)
    model_answer: str = Field(..., min_length=20)
    keywords: list[str] = Field(..., min_items=1)
    max_score: int = Field(default=10, ge=1, le=100)


class DescriptiveQuestionCreate(DescriptiveQuestionBase):
    """Model for creating descriptive question"""
    created_by: str
    is_ai_generated: bool = False


class DescriptiveQuestion(DescriptiveQuestionBase):
    """Complete descriptive question model"""
    question_id: str
    created_by: str
    is_ai_generated: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


class DescriptiveQuestionDisplay(BaseModel):
    """Descriptive question for display to users"""
    question_id: str
    question_text: str
    max_score: int


class DescriptiveAnswerSubmit(BaseModel):
    """Model for submitting descriptive answer"""
    question_id: str
    answer_text: str = Field(..., min_length=10)


class AnswerFeedback(BaseModel):
    """Feedback for descriptive answer"""
    correct_points: list[str] = []
    improvements: list[str] = []
    explanation: str


class DescriptiveAnswerResult(BaseModel):
    """Result of descriptive answer evaluation"""
    question_id: str
    user_answer: str
    score: int
    max_score: int
    feedback: AnswerFeedback
    points_earned: int
    time_taken_seconds: int


class Answer(BaseModel):
    """Generic answer record"""
    score_id: str
    user_id: str
    session_id: str
    question_id: str
    question_type: str  # 'mcq' or 'descriptive'
    user_answer: str
    is_correct: bool
    points_earned: int
    time_taken_seconds: int
    evaluated_at: datetime

    class Config:
        from_attributes = True


class QuizResults(BaseModel):
    """Overall quiz results for a session"""
    session_id: str
    total_questions: int
    answered_questions: int
    correct_answers: int
    total_score: int
    max_possible_score: int
    accuracy_rate: float
    average_time_per_question: float
    mcq_results: list[MCQAnswerResult] = []
    descriptive_results: list[DescriptiveAnswerResult] = []
