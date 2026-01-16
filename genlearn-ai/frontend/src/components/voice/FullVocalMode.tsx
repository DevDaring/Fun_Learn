import React, { useState, useEffect } from 'react';

interface FullVocalModeProps {
  enabled: boolean;
  onToggle: (enabled: boolean) => void;
}

export const FullVocalMode: React.FC<FullVocalModeProps> = ({ enabled, onToggle }) => {
  const [isAnimating, setIsAnimating] = useState(false);

  const handleToggle = () => {
    setIsAnimating(true);
    onToggle(!enabled);
    setTimeout(() => setIsAnimating(false), 300);
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className={`w-12 h-12 rounded-full flex items-center justify-center transition-colors ${
            enabled ? 'bg-primary-600' : 'bg-gray-300'
          }`}>
            <svg className="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
            </svg>
          </div>
          <div>
            <h3 className="text-lg font-bold text-gray-900">Full Vocal Mode</h3>
            <p className="text-sm text-gray-600">
              {enabled ? 'Audio narration is active' : 'Enable audio narration for all content'}
            </p>
          </div>
        </div>

        {/* Toggle Switch */}
        <button
          onClick={handleToggle}
          className={`relative inline-flex h-8 w-14 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary-600 focus:ring-offset-2 ${
            enabled ? 'bg-primary-600' : 'bg-gray-300'
          }`}
          role="switch"
          aria-checked={enabled}
        >
          <span
            className={`pointer-events-none inline-block h-7 w-7 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
              enabled ? 'translate-x-6' : 'translate-x-0'
            } ${isAnimating ? 'scale-110' : ''}`}
          />
        </button>
      </div>

      {/* Status Indicator */}
      {enabled && (
        <div className="mt-4 bg-primary-50 border border-primary-200 rounded-lg p-3">
          <div className="flex items-start gap-2">
            <div className="flex gap-1 mt-1">
              <div className="w-1 h-3 bg-primary-600 rounded animate-pulse" style={{ animationDelay: '0ms' }}></div>
              <div className="w-1 h-4 bg-primary-600 rounded animate-pulse" style={{ animationDelay: '150ms' }}></div>
              <div className="w-1 h-3 bg-primary-600 rounded animate-pulse" style={{ animationDelay: '300ms' }}></div>
            </div>
            <div className="flex-1">
              <p className="text-sm font-medium text-primary-900">Vocal Mode Active</p>
              <p className="text-xs text-primary-700 mt-1">
                All learning content will include audio narration. You can still manually control playback.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Info Box */}
      {!enabled && (
        <div className="mt-4 bg-blue-50 border border-blue-200 rounded-lg p-3">
          <h4 className="text-sm font-semibold text-blue-900 mb-2 flex items-center">
            <svg className="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            About Full Vocal Mode
          </h4>
          <ul className="text-xs text-blue-800 space-y-1">
            <li>• Automatically narrates all learning content</li>
            <li>• Includes stories, questions, and explanations</li>
            <li>• Supports multiple languages</li>
            <li>• Great for accessibility and audio learners</li>
          </ul>
        </div>
      )}
    </div>
  );
};
