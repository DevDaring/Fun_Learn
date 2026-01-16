import React, { useState, useRef } from 'react';
import { Button } from '../common/Button';
import api from '../../services/api';
import { playAudio } from '../../utils/helpers';

interface VoiceOutputProps {
  text: string;
  language?: string;
  voiceType?: 'male' | 'female';
  autoPlay?: boolean;
}

export const VoiceOutput: React.FC<VoiceOutputProps> = ({
  text,
  language = 'en',
  voiceType = 'female',
  autoPlay = false
}) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  React.useEffect(() => {
    if (autoPlay && text) {
      handlePlay();
    }
  }, [text, autoPlay]);

  const handlePlay = async () => {
    if (isPlaying) {
      handleStop();
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const audioBlob = await api.textToSpeech(text, language, voiceType);
      await playAudio(audioBlob);
      setIsPlaying(true);

      // Reset playing state after audio ends
      setTimeout(() => {
        setIsPlaying(false);
      }, 100);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to generate speech');
      console.error('TTS error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleStop = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
    setIsPlaying(false);
  };

  return (
    <div className="space-y-3">
      {/* Play Button */}
      <div className="flex items-center gap-3">
        <Button
          onClick={handlePlay}
          disabled={isLoading || !text}
          isLoading={isLoading}
          variant={isPlaying ? 'danger' : 'primary'}
          size="sm"
        >
          {isPlaying ? (
            <>
              <svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 10a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" />
              </svg>
              Stop
            </>
          ) : (
            <>
              <svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
              </svg>
              Listen
            </>
          )}
        </Button>

        {isPlaying && (
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <div className="flex gap-1">
              <div className="w-1 h-4 bg-primary-600 rounded animate-pulse" style={{ animationDelay: '0ms' }}></div>
              <div className="w-1 h-6 bg-primary-600 rounded animate-pulse" style={{ animationDelay: '150ms' }}></div>
              <div className="w-1 h-4 bg-primary-600 rounded animate-pulse" style={{ animationDelay: '300ms' }}></div>
            </div>
            <span>Playing...</span>
          </div>
        )}
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-2 text-red-700 text-xs">
          {error}
        </div>
      )}
    </div>
  );
};
