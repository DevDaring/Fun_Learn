import React, { useState, useEffect } from 'react';
import { StorySegment } from '../../types';
import { ImageCard } from './ImageCard';

interface ImageCarouselProps {
  segments: StorySegment[];
  onComplete?: () => void;
  onAudioPlay?: (audioUrl: string) => void;
}

export const ImageCarousel: React.FC<ImageCarouselProps> = ({ segments, onComplete, onAudioPlay }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [autoPlayEnabled, setAutoPlayEnabled] = useState(false);

  useEffect(() => {
    if (!autoPlayEnabled) return;

    const timer = setTimeout(() => {
      if (currentIndex < segments.length - 1) {
        setCurrentIndex(currentIndex + 1);
      } else {
        setAutoPlayEnabled(false);
        if (onComplete) {
          onComplete();
        }
      }
    }, 10000); // 10 seconds per slide

    return () => clearTimeout(timer);
  }, [currentIndex, autoPlayEnabled, segments.length, onComplete]);

  const goToNext = () => {
    if (currentIndex < segments.length - 1) {
      setCurrentIndex(currentIndex + 1);
    } else if (onComplete) {
      onComplete();
    }
  };

  const goToPrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  const goToSlide = (index: number) => {
    setCurrentIndex(index);
  };

  const toggleAutoPlay = () => {
    setAutoPlayEnabled(!autoPlayEnabled);
  };

  if (segments.length === 0) {
    return (
      <div className="flex items-center justify-center h-96 bg-gray-100 rounded-lg">
        <p className="text-gray-500">No content available</p>
      </div>
    );
  }

  return (
    <div className="relative">
      {/* Main Carousel Content */}
      <div className="relative overflow-hidden">
        <ImageCard segment={segments[currentIndex]} onAudioPlay={onAudioPlay} />
      </div>

      {/* Navigation Controls */}
      <div className="mt-6 flex items-center justify-between">
        {/* Previous Button */}
        <button
          onClick={goToPrevious}
          disabled={currentIndex === 0}
          className="flex items-center gap-2 px-4 py-2 bg-white border-2 border-gray-300 rounded-lg font-medium transition-colors hover:border-primary-600 hover:text-primary-600 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:border-gray-300 disabled:hover:text-gray-900"
          aria-label="Previous segment"
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Previous
        </button>

        {/* Slide Indicators */}
        <div className="flex items-center gap-3">
          {segments.map((_, index) => (
            <button
              key={index}
              onClick={() => goToSlide(index)}
              className={`transition-all duration-300 rounded-full ${
                index === currentIndex
                  ? 'w-12 h-3 bg-primary-600'
                  : 'w-3 h-3 bg-gray-300 hover:bg-gray-400'
              }`}
              aria-label={`Go to segment ${index + 1}`}
            />
          ))}
        </div>

        {/* Next Button */}
        <button
          onClick={goToNext}
          className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg font-medium transition-colors hover:bg-primary-700"
          aria-label="Next segment"
        >
          {currentIndex === segments.length - 1 ? 'Complete' : 'Next'}
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>

      {/* Progress Bar */}
      <div className="mt-4">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm text-gray-600 font-medium">
            Segment {currentIndex + 1} of {segments.length}
          </span>
          <button
            onClick={toggleAutoPlay}
            className="text-sm text-primary-600 hover:text-primary-700 font-medium flex items-center gap-1"
          >
            {autoPlayEnabled ? (
              <>
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Pause Auto-play
              </>
            ) : (
              <>
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Enable Auto-play
              </>
            )}
          </button>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
          <div
            className="bg-primary-600 h-full transition-all duration-300 rounded-full"
            style={{ width: `${((currentIndex + 1) / segments.length) * 100}%` }}
          />
        </div>
      </div>

      {/* Keyboard Navigation Hint */}
      <div className="mt-4 text-center text-xs text-gray-500">
        <p>Tip: Use arrow keys to navigate</p>
      </div>

      {/* Keyboard Navigation */}
      <div className="sr-only">
        <button
          onKeyDown={(e) => {
            if (e.key === 'ArrowLeft') goToPrevious();
            if (e.key === 'ArrowRight') goToNext();
          }}
          aria-label="Keyboard navigation"
        />
      </div>
    </div>
  );
};
