import React, { useState, useEffect } from 'react';
import { DescriptiveQuestion as DescriptiveQuestionType, DescriptiveAnswer } from '../../types';
import { Button } from '../common/Button';
import api from '../../services/api';

interface DescriptiveQuestionProps {
  sessionId: string;
  onComplete: (totalScore: number) => void;
}

export const DescriptiveQuestion: React.FC<DescriptiveQuestionProps> = ({ sessionId, onComplete }) => {
  const [questions, setQuestions] = useState<DescriptiveQuestionType[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answer, setAnswer] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [feedback, setFeedback] = useState<DescriptiveAnswer | null>(null);
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
      const data = await api.getDescriptiveQuestions(sessionId);
      // Handle both {questions: [...]} and direct array response formats
      setQuestions(Array.isArray(data) ? data : (data.questions || []));
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to load questions');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitAnswer = async () => {
    if (!answer.trim()) return;

    setIsSubmitting(true);
    try {
      const currentQuestion = questions[currentQuestionIndex];
      const result = await api.submitDescriptiveAnswer(sessionId, currentQuestion.question_id, answer);
      setFeedback(result);
      setTotalScore(totalScore + result.score);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to submit answer');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleNextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      setAnswer('');
      setFeedback(null);
    } else {
      onComplete(totalScore);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96 bg-white rounded-lg shadow-lg">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-4 border-primary-600 border-t-transparent mx-auto mb-4"></div>
          <p className="text-gray-600">Loading questions...</p>
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
  const wordCount = answer.trim().split(/\s+/).filter(w => w.length > 0).length;

  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-purple-700 text-white p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold">Descriptive Questions</h2>
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
        {/* Question Text */}
        <div className="mb-6">
          <div className="flex items-start gap-3 mb-4">
            <div className="flex-shrink-0 w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center">
              <svg className="w-6 h-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
              </svg>
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-semibold text-gray-900 mb-2">{currentQuestion.question_text}</h3>
              <p className="text-sm text-gray-600">Maximum score: {currentQuestion.max_score} points</p>
            </div>
          </div>
        </div>

        {/* Answer Input */}
        {!feedback ? (
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Your Answer
            </label>
            <textarea
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none transition-colors"
              rows={8}
              placeholder="Write your detailed answer here..."
              disabled={!!feedback}
            />
            <div className="flex justify-between items-center mt-2">
              <p className="text-sm text-gray-500">
                Word count: <span className="font-medium">{wordCount}</span>
              </p>
              {wordCount < 20 && (
                <p className="text-sm text-amber-600">
                  Tip: Write at least 20 words for a detailed answer
                </p>
              )}
            </div>
          </div>
        ) : (
          <div className="mb-6">
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
              <h4 className="text-sm font-medium text-gray-700 mb-2">Your Answer:</h4>
              <p className="text-gray-900 whitespace-pre-wrap">{answer}</p>
            </div>
          </div>
        )}

        {/* Feedback */}
        {feedback && (
          <div className="space-y-4 mb-6">
            {/* Score */}
            <div className="bg-gradient-to-r from-purple-50 to-blue-50 border border-purple-200 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <span className="text-lg font-semibold text-gray-900">Your Score:</span>
                <span className="text-3xl font-bold text-purple-600">
                  {feedback.score} / {feedback.max_score}
                </span>
              </div>
            </div>

            {/* Correct Points */}
            {feedback.feedback.correct_points.length > 0 && (
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <h4 className="font-semibold text-green-900 mb-3 flex items-center">
                  <svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  What You Got Right
                </h4>
                <ul className="space-y-2">
                  {feedback.feedback.correct_points.map((point, index) => (
                    <li key={index} className="flex items-start">
                      <span className="flex-shrink-0 w-5 h-5 bg-green-200 text-green-800 rounded-full flex items-center justify-center text-xs font-bold mr-2 mt-0.5">
                        {index + 1}
                      </span>
                      <span className="text-green-800">{point}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Areas for Improvement */}
            {feedback.feedback.improvements.length > 0 && (
              <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
                <h4 className="font-semibold text-amber-900 mb-3 flex items-center">
                  <svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Areas for Improvement
                </h4>
                <ul className="space-y-2">
                  {feedback.feedback.improvements.map((point, index) => (
                    <li key={index} className="flex items-start">
                      <span className="flex-shrink-0 w-5 h-5 bg-amber-200 text-amber-800 rounded-full flex items-center justify-center text-xs font-bold mr-2 mt-0.5">
                        {index + 1}
                      </span>
                      <span className="text-amber-800">{point}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Explanation */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h4 className="font-semibold text-blue-900 mb-3 flex items-center">
                <svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
                Detailed Explanation
              </h4>
              <p className="text-blue-900 leading-relaxed">{feedback.feedback.explanation}</p>
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex justify-end gap-3">
          {!feedback ? (
            <Button
              onClick={handleSubmitAnswer}
              disabled={!answer.trim() || isSubmitting}
              isLoading={isSubmitting}
              variant="primary"
              size="lg"
            >
              Submit Answer
            </Button>
          ) : (
            <Button onClick={handleNextQuestion} variant="primary" size="lg">
              {currentQuestionIndex < questions.length - 1 ? 'Next Question' : 'Complete'}
            </Button>
          )}
        </div>
      </div>
    </div>
  );
};
