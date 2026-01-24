import React, { useState } from 'react';
import { CourseSetup } from '../components/learning/CourseSetup';
import { StoryPlayer } from '../components/learning/StoryPlayer';
import { ResultsSummary } from '../components/learning/ResultsSummary';
import { useLearningSession } from '../hooks/useLearningSession';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { CourseConfig } from '../types';

interface SessionResults {
  totalScore: number;
  correctAnswers: number;
  totalQuestions: number;
  xpEarned: number;
  timeSpent: number;
  longestStreak: number;
}

export const LearningPage: React.FC = () => {
  const [phase, setPhase] = useState<'setup' | 'playing' | 'complete'>('setup');
  const [sessionResults, setSessionResults] = useState<SessionResults | null>(null);
  const { startNewSession, isLoading, error, currentSession, endCurrentSession } = useLearningSession();

  const handleStart = async (config: CourseConfig) => {
    try {
      await startNewSession(config);
      setPhase('playing');
    } catch (err) {
      console.error('Failed to start session:', err);
    }
  };

  const handleComplete = async (results: SessionResults) => {
    setSessionResults(results);

    // End session on backend
    if (currentSession) {
      try {
        await endCurrentSession(results.totalScore, true);
      } catch (err) {
        console.error('Failed to end session:', err);
      }
    }

    setPhase('complete');
  };

  const handlePlayAgain = () => {
    setPhase('setup');
    setSessionResults(null);
  };

  const handleGoHome = () => {
    window.location.href = '/';
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <LoadingSpinner size="lg" text="Starting your learning adventure..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border-2 border-red-300 rounded-xl p-8 max-w-lg mx-auto text-center">
        <div className="text-4xl mb-4">😔</div>
        <h3 className="text-xl font-bold text-red-800 mb-2">Error</h3>
        <p className="text-red-700 mb-4">{error}</p>
        <button
          onClick={() => setPhase('setup')}
          className="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
        >
          Try Again
        </button>
      </div>
    );
  }

  // Setup phase
  if (phase === 'setup') {
    return <CourseSetup onStart={handleStart} />;
  }

  // Playing phase
  if (phase === 'playing' && currentSession) {
    return (
      <div className="py-4">
        <StoryPlayer
          session={currentSession}
          onComplete={handleComplete}
        />
      </div>
    );
  }

  // Complete phase
  if (phase === 'complete' && sessionResults) {
    return (
      <div className="py-8">
        <ResultsSummary
          topic={currentSession?.topic || 'Learning Session'}
          totalQuestions={sessionResults.totalQuestions}
          correctAnswers={sessionResults.correctAnswers}
          totalScore={sessionResults.totalScore}
          xpEarned={sessionResults.xpEarned}
          timeSpent={sessionResults.timeSpent}
          longestStreak={sessionResults.longestStreak}
          onPlayAgain={handlePlayAgain}
          onGoHome={handleGoHome}
        />
      </div>
    );
  }

  return (
    <div className="text-center py-12">
      <p className="text-gray-600">Loading...</p>
    </div>
  );
};
