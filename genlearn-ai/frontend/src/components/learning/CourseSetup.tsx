import React, { useState } from 'react';
import { CourseConfig } from '../../types';
import { Button } from '../common/Button';
import { Dropdown } from '../common/Dropdown';
import { Slider } from '../common/Slider';
import { DIFFICULTY_LEVELS, DURATION_OPTIONS, VISUAL_STYLES, PLAY_MODES } from '../../utils/constants';

interface CourseSetupProps {
  onStart: (config: CourseConfig) => void;
}

export const CourseSetup: React.FC<CourseSetupProps> = ({ onStart }) => {
  const [config, setConfig] = useState<CourseConfig>({
    topic: '',
    difficulty_level: 5,
    duration_minutes: 15,
    visual_style: 'cartoon',
    play_mode: 'solo',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onStart(config);
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-lg p-8 max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Configure Your Learning Session</h2>

      <div className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Topic
          </label>
          <input
            type="text"
            value={config.topic}
            onChange={(e) => setConfig({ ...config, topic: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            placeholder="e.g., Photosynthesis, Python Basics, World War II"
            required
          />
        </div>

        <div>
          <Slider
            label="Difficulty Level"
            value={config.difficulty_level}
            onChange={(value) => setConfig({ ...config, difficulty_level: value })}
            min={1}
            max={10}
            step={1}
          />
          <p className="text-sm text-gray-500 mt-1">
            {DIFFICULTY_LEVELS.find(d => d.value === config.difficulty_level)?.label}
          </p>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Duration
          </label>
          <Dropdown
            options={DURATION_OPTIONS}
            value={config.duration_minutes}
            onChange={(value) => setConfig({ ...config, duration_minutes: Number(value) })}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Visual Style
          </label>
          <div className="grid grid-cols-2 gap-4">
            {VISUAL_STYLES.map((style) => (
              <button
                key={style.value}
                type="button"
                onClick={() => setConfig({ ...config, visual_style: style.value as any })}
                className={`p-4 border-2 rounded-lg transition-colors ${
                  config.visual_style === style.value
                    ? 'border-primary-600 bg-primary-50'
                    : 'border-gray-300 hover:border-gray-400'
                }`}
              >
                {style.label}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Play Mode
          </label>
          <div className="grid grid-cols-3 gap-4">
            {PLAY_MODES.map((mode) => (
              <button
                key={mode.value}
                type="button"
                onClick={() => setConfig({ ...config, play_mode: mode.value as any })}
                className={`p-4 border-2 rounded-lg transition-colors ${
                  config.play_mode === mode.value
                    ? 'border-primary-600 bg-primary-50'
                    : 'border-gray-300 hover:border-gray-400'
                }`}
              >
                <div className="text-2xl mb-2">{mode.icon}</div>
                <div className="text-sm font-medium">{mode.label}</div>
              </button>
            ))}
          </div>
        </div>

        <Button type="submit" variant="primary" size="lg" className="w-full">
          Start Learning Session
        </Button>
      </div>
    </form>
  );
};
