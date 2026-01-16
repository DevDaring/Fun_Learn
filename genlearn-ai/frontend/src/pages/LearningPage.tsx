import React, { useState } from 'react';
import { CourseSetup } from '../components/learning/CourseSetup';
import { useLearningSession } from '../hooks/useLearningSession';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { CourseConfig } from '../types';

export const LearningPage: React.FC = () => {
  const [started, setStarted] = useState(false);
  const { startNewSession, isLoading, error, currentSession } = useLearningSession();

  const handleStart = async (config: CourseConfig) => {
    try {
      await startNewSession(config);
      setStarted(true);
    } catch (err) {
      console.error('Failed to start session:', err);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <LoadingSpinner size="lg" text="Generating your personalized learning content..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-red-900 mb-2">Error</h3>
        <p className="text-red-700">{error}</p>
      </div>
    );
  }

  if (!started || !currentSession) {
    return <CourseSetup onStart={handleStart} />;
  }

  return (
    <div className="bg-white rounded-lg p-8 shadow-md">
      <h2 className="text-2xl font-bold mb-4">Learning Session: {currentSession.topic}</h2>
      <p className="text-gray-600">Session content will appear here...</p>
      <div className="mt-8 text-center text-gray-500">
        <p>The full learning session UI with image carousel, quizzes, and videos</p>
        <p>will be implemented here based on the content from the backend.</p>
      </div>
    </div>
  );
};
