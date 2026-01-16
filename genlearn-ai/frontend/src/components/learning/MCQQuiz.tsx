import React, { useState, useEffect } from 'react';
import { MCQQuestion, MCQAnswer } from '../../types';
import { Button } from '../common/Button';
import api from '../../services/api';

interface MCQQuizProps {
  sessionId: string;
  onComplete: (totalScore: number) => void;
}

export const MCQQuiz: React.FC<MCQQuizProps> = ({ sessionId, onComplete }) => {
  const [questions, setQuestions] = useState<MCQQuestion[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [answer, setAnswer] = useState<MCQAnswer | null>(null);
  const [totalScore, setTotalScore] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadQuestions();
  }, [sessionId]);

  const loadQuestions = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getMCQQuestions(sessionId);
      // Handle both {questions: [...]} and direct array response formats
      setQuestions(Array.isArray(data) ? data : (data.questions || []));
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to load questions');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitAnswer = async () => {
    if (!selectedAnswer) return;

    setIsSubmitting(true);
    try {
      const currentQuestion = questions[currentQuestionIndex];
      const result = await api.submitMCQAnswer(sessionId, currentQuestion.question_id, selectedAnswer);
      setAnswer(result);
      setTotalScore(totalScore + result.points_earned);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to submit answer');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleNextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      setSelectedAnswer(null);
      setAnswer(null);
    } else {
      onComplete(totalScore);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96 bg-white rounded-lg shadow-lg">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-4 border-primary-600 border-t-transparent mx-auto mb-4"></div>
          <p className="text-gray-600">Loading quiz questions...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <div className="flex items-center gap-3">
          <svg className="w-6 h-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div>
            <h3 className="font-semibold text-red-900">Error</h3>
            <p className="text-red-700">{error}</p>
          </div>
        </div>
        <Button onClick={loadQuestions} variant="danger" className="mt-4">
          Try Again
        </Button>
      </div>
    );
  }

  if (questions.length === 0) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 text-center">
        <p className="text-yellow-800">No questions available for this session.</p>
      </div>
    );
  }

  const currentQuestion = questions[currentQuestionIndex];
  const options = ['A', 'B', 'C', 'D'];

  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-700 text-white p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold">Multiple Choice Quiz</h2>
          <div className="bg-white/20 backdrop-blur-sm px-4 py-2 rounded-lg">
            <span className="font-semibold">Score: {totalScore}</span>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-sm opacity-90">Question {currentQuestionIndex + 1} of {questions.length}</span>
          <div className="flex-1 bg-white/20 rounded-full h-2 overflow-hidden">
            <div
              className="bg-white h-full transition-all duration-300"
              style={{ width: `${((currentQuestionIndex + 1) / questions.length) * 100}%` }}
            />
          </div>
        </div>
      </div>

      {/* Question Content */}
      <div className="p-6">
        {/* Question Image */}
        {currentQuestion.image_url && (
          <div className="mb-6 rounded-lg overflow-hidden">
            <img
              src={currentQuestion.image_url}
              alt="Question illustration"
              className="w-full max-h-64 object-contain bg-gray-50"
            />
          </div>
        )}

        {/* Question Text */}
        <div className="mb-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">{currentQuestion.question_text}</h3>
        </div>

        {/* Options */}
        <div className="space-y-3 mb-6">
          {options.map((option) => {
            const optionText = currentQuestion.options[option as keyof typeof currentQuestion.options];
            const isSelected = selectedAnswer === option;
            const isCorrect = answer?.correct_answer === option;
            const isWrong = answer && selectedAnswer === option && !answer.is_correct;

            let buttonClass = 'w-full p-4 text-left border-2 rounded-lg transition-all ';
            if (answer) {
              if (isCorrect) {
                buttonClass += 'border-green-500 bg-green-50 text-green-900';
              } else if (isWrong) {
                buttonClass += 'border-red-500 bg-red-50 text-red-900';
              } else {
                buttonClass += 'border-gray-200 bg-gray-50 text-gray-500';
              }
            } else if (isSelected) {
              buttonClass += 'border-primary-600 bg-primary-50 text-primary-900';
            } else {
              buttonClass += 'border-gray-300 hover:border-primary-400 hover:bg-primary-50';
            }

            return (
              <button
                key={option}
                onClick={() => !answer && setSelectedAnswer(option)}
                disabled={!!answer}
                className={buttonClass}
              >
                <div className="flex items-center">
                  <span className="flex-shrink-0 w-8 h-8 rounded-full border-2 flex items-center justify-center font-bold mr-4">
                    {option}
                  </span>
                  <span className="flex-1">{optionText}</span>
                  {answer && isCorrect && (
                    <svg className="w-6 h-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  )}
                  {isWrong && (
                    <svg className="w-6 h-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  )}
                </div>
              </button>
            );
          })}
        </div>

        {/* Answer Feedback */}
        {answer && (
          <div className={`p-4 rounded-lg mb-6 ${answer.is_correct ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
            <div className="flex items-start gap-3">
              {answer.is_correct ? (
                <svg className="w-6 h-6 text-green-600 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              ) : (
                <svg className="w-6 h-6 text-red-600 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              )}
              <div className="flex-1">
                <h4 className={`font-semibold mb-2 ${answer.is_correct ? 'text-green-900' : 'text-red-900'}`}>
                  {answer.is_correct ? 'Correct!' : 'Incorrect'}
                </h4>
                <p className={answer.is_correct ? 'text-green-800' : 'text-red-800'}>{answer.explanation}</p>
                <p className={`mt-2 font-medium ${answer.is_correct ? 'text-green-900' : 'text-red-900'}`}>
                  Points earned: {answer.points_earned}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex justify-end gap-3">
          {!answer ? (
            <Button
              onClick={handleSubmitAnswer}
              disabled={!selectedAnswer || isSubmitting}
              isLoading={isSubmitting}
              variant="primary"
              size="lg"
            >
              Submit Answer
            </Button>
          ) : (
            <Button onClick={handleNextQuestion} variant="primary" size="lg">
              {currentQuestionIndex < questions.length - 1 ? 'Next Question' : 'Complete Quiz'}
            </Button>
          )}
        </div>
      </div>
    </div>
  );
};
