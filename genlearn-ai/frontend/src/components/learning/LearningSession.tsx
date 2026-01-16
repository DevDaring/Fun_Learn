import React, { useState, useEffect } from 'react';
import { LearningSession as LearningSessionType, LearningContent, CourseConfig } from '../../types';
import { ImageCarousel } from './ImageCarousel';
import { VideoPlayer } from './VideoPlayer';
import { MCQQuiz } from './MCQQuiz';
import { DescriptiveQuestion } from './DescriptiveQuestion';
import { Button } from '../common/Button';
import { ProgressBar } from '../common/ProgressBar';
import api from '../../services/api';
import { playAudio } from '../../utils/helpers';

interface LearningSessionProps {
  config: CourseConfig;
  onComplete: (finalScore: number) => void;
  onCancel: () => void;
}

type Phase = 'loading' | 'images' | 'video' | 'mcq' | 'descriptive' | 'completed';

export const LearningSession: React.FC<LearningSessionProps> = ({ config, onComplete, onCancel }) => {
  const [session, setSession] = useState<LearningSessionType | null>(null);
  const [content, setContent] = useState<LearningContent | null>(null);
  const [currentPhase, setCurrentPhase] = useState<Phase>('loading');
  const [currentCycle, setCurrentCycle] = useState(1);
  const [totalScore, setTotalScore] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [isAudioPlaying, setIsAudioPlaying] = useState(false);

  useEffect(() => {
    startSession();
  }, []);

  const startSession = async () => {
    try {
      setError(null);
      const sessionData = await api.startSession(config);
      // Handle both {session: ...} and direct session data response formats
      const sessionObj = sessionData.session || sessionData;
      setSession(sessionObj);
      const contentData = await api.getSessionContent(sessionObj.session_id);
      setContent(contentData);
      setCurrentPhase('images');
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to start learning session');
    }
  };

  const handleAudioPlay = async (audioUrl: string) => {
    if (isAudioPlaying) return;

    try {
      setIsAudioPlaying(true);
      const response = await fetch(audioUrl);
      const audioBlob = await response.blob();
      await playAudio(audioBlob);
    } catch (err) {
      console.error('Failed to play audio:', err);
    } finally {
      setIsAudioPlaying(false);
    }
  };

  const handleImagesComplete = () => {
    setCurrentPhase('video');
  };

  const handleVideoComplete = () => {
    setCurrentPhase('mcq');
  };

  const handleMCQComplete = (score: number) => {
    setTotalScore(totalScore + score);
    setCurrentPhase('descriptive');
  };

  const handleDescriptiveComplete = (score: number) => {
    const newTotalScore = totalScore + score;
    setTotalScore(newTotalScore);

    if (session && currentCycle < session.total_cycles) {
      setCurrentCycle(currentCycle + 1);
      setCurrentPhase('images');
    } else {
      setCurrentPhase('completed');
      if (session) {
        api.endSession(session.session_id, newTotalScore, 0, true).catch(console.error);
      }
      onComplete(newTotalScore);
    }
  };

  const handleCancelSession = async () => {
    if (session) {
      try {
        await api.endSession(session.session_id, totalScore, 0, false);
      } catch (err) {
        console.error('Failed to end session:', err);
      }
    }
    onCancel();
  };

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <div className="bg-white rounded-lg shadow-lg p-8 max-w-md w-full">
          <div className="text-center">
            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Session Error</h3>
            <p className="text-gray-600 mb-6">{error}</p>
            <div className="flex gap-3 justify-center">
              <Button onClick={startSession} variant="primary">
                Try Again
              </Button>
              <Button onClick={onCancel} variant="outline">
                Go Back
              </Button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (currentPhase === 'loading' || !session || !content) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-4 border-primary-600 border-t-transparent mx-auto mb-4"></div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">Preparing Your Learning Session</h3>
          <p className="text-gray-600">Generating personalized content...</p>
        </div>
      </div>
    );
  }

  if (currentPhase === 'completed') {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <div className="bg-white rounded-lg shadow-lg p-8 max-w-2xl w-full text-center">
          <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg className="w-10 h-10 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h2 className="text-3xl font-bold text-gray-900 mb-4">Session Complete!</h2>
          <p className="text-gray-600 mb-8">Congratulations on completing your learning session!</p>

          <div className="bg-gradient-to-r from-primary-50 to-purple-50 rounded-lg p-6 mb-8">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Your Results</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-white rounded-lg p-4">
                <p className="text-sm text-gray-600 mb-1">Total Score</p>
                <p className="text-3xl font-bold text-primary-600">{totalScore}</p>
              </div>
              <div className="bg-white rounded-lg p-4">
                <p className="text-sm text-gray-600 mb-1">Cycles Completed</p>
                <p className="text-3xl font-bold text-purple-600">{session.total_cycles}</p>
              </div>
              <div className="bg-white rounded-lg p-4">
                <p className="text-sm text-gray-600 mb-1">Topic</p>
                <p className="text-lg font-semibold text-gray-900">{session.topic}</p>
              </div>
            </div>
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-8">
            <h4 className="font-semibold text-blue-900 mb-2">Topic Summary</h4>
            <p className="text-blue-800 leading-relaxed">{content.topic_summary}</p>
          </div>

          <Button onClick={onCancel} variant="primary" size="lg" className="w-full md:w-auto">
            Back to Dashboard
          </Button>
        </div>
      </div>
    );
  }

  const totalPhases = session.total_cycles * 4; // images, video, mcq, descriptive per cycle
  const completedPhases = (currentCycle - 1) * 4 + (['images', 'video', 'mcq', 'descriptive'].indexOf(currentPhase));
  const progress = (completedPhases / totalPhases) * 100;

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">{session.topic}</h1>
              <p className="text-gray-600">Cycle {currentCycle} of {session.total_cycles}</p>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-sm text-gray-600">Current Score</p>
                <p className="text-2xl font-bold text-primary-600">{totalScore}</p>
              </div>
              <Button onClick={handleCancelSession} variant="outline" size="sm">
                Exit Session
              </Button>
            </div>
          </div>

          {/* Progress Bar */}
          <div>
            <div className="flex justify-between text-sm text-gray-600 mb-2">
              <span>Overall Progress</span>
              <span>{Math.round(progress)}%</span>
            </div>
            <ProgressBar value={progress} />
          </div>
        </div>

        {/* Phase Indicators */}
        <div className="bg-white rounded-lg shadow-md p-4 mb-6">
          <div className="flex items-center justify-between">
            {['images', 'video', 'mcq', 'descriptive'].map((phase, index) => {
              const phaseLabels = {
                images: 'Story',
                video: 'Video',
                mcq: 'MCQ',
                descriptive: 'Written'
              };
              const isActive = currentPhase === phase;
              const isPast = ['images', 'video', 'mcq', 'descriptive'].indexOf(currentPhase) > index;

              return (
                <div key={phase} className="flex items-center flex-1">
                  <div className={`flex items-center justify-center w-10 h-10 rounded-full font-semibold transition-colors ${
                    isActive ? 'bg-primary-600 text-white' :
                    isPast ? 'bg-green-500 text-white' :
                    'bg-gray-200 text-gray-600'
                  }`}>
                    {isPast ? (
                      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    ) : (
                      index + 1
                    )}
                  </div>
                  <span className={`ml-2 text-sm font-medium ${isActive ? 'text-primary-600' : 'text-gray-600'}`}>
                    {phaseLabels[phase as keyof typeof phaseLabels]}
                  </span>
                  {index < 3 && (
                    <div className={`flex-1 h-1 mx-2 rounded ${isPast ? 'bg-green-500' : 'bg-gray-200'}`} />
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Main Content Area */}
        <div className="mb-6">
          {currentPhase === 'images' && (
            <ImageCarousel
              segments={content.story_segments}
              onComplete={handleImagesComplete}
              onAudioPlay={handleAudioPlay}
            />
          )}

          {currentPhase === 'video' && session && (
            <VideoPlayer
              sessionId={session.session_id}
              cycleNumber={currentCycle}
              onComplete={handleVideoComplete}
            />
          )}

          {currentPhase === 'mcq' && session && (
            <MCQQuiz
              sessionId={session.session_id}
              onComplete={handleMCQComplete}
            />
          )}

          {currentPhase === 'descriptive' && session && (
            <DescriptiveQuestion
              sessionId={session.session_id}
              onComplete={handleDescriptiveComplete}
            />
          )}
        </div>
      </div>
    </div>
  );
};
