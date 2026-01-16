import React, { useState } from 'react';
import { Button } from '../common/Button';
import { Slider } from '../common/Slider';
import api from '../../services/api';

interface TournamentCreatorProps {
  onSuccess?: () => void;
  onCancel?: () => void;
}

export const TournamentCreator: React.FC<TournamentCreatorProps> = ({ onSuccess, onCancel }) => {
  const [formData, setFormData] = useState({
    name: '',
    topic: '',
    difficulty_level: 5,
    start_datetime: '',
    duration_minutes: 30,
    max_participants: 50,
    entry_type: 'free' as 'free' | 'invite_only',
    prizes: {
      first: '',
      second: '',
      third: ''
    }
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);

    try {
      await api.createTournament(formData);
      if (onSuccess) onSuccess();
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to create tournament');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 max-w-3xl mx-auto">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Create Tournament</h2>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic Info */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Tournament Name *
            </label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              placeholder="e.g., Math Masters Championship"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Topic *
            </label>
            <input
              type="text"
              value={formData.topic}
              onChange={(e) => setFormData({ ...formData, topic: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              placeholder="e.g., Algebra, World History"
              required
            />
          </div>
        </div>

        {/* Difficulty */}
        <div>
          <Slider
            label="Difficulty Level"
            value={formData.difficulty_level}
            onChange={(value) => setFormData({ ...formData, difficulty_level: value })}
            min={1}
            max={10}
            step={1}
          />
        </div>

        {/* Date and Time */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Start Date & Time *
            </label>
            <input
              type="datetime-local"
              value={formData.start_datetime}
              onChange={(e) => setFormData({ ...formData, start_datetime: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Duration (minutes) *
            </label>
            <input
              type="number"
              value={formData.duration_minutes}
              onChange={(e) => setFormData({ ...formData, duration_minutes: Number(e.target.value) })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              min="10"
              max="180"
              required
            />
          </div>
        </div>

        {/* Participants and Entry Type */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Max Participants *
            </label>
            <input
              type="number"
              value={formData.max_participants}
              onChange={(e) => setFormData({ ...formData, max_participants: Number(e.target.value) })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              min="2"
              max="1000"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Entry Type
            </label>
            <select
              value={formData.entry_type}
              onChange={(e) => setFormData({ ...formData, entry_type: e.target.value as any })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            >
              <option value="free">Free Entry</option>
              <option value="invite_only">Invite Only</option>
            </select>
          </div>
        </div>

        {/* Prizes */}
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-3">Prize Pool</h3>
          <div className="space-y-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                1st Place Prize
              </label>
              <input
                type="text"
                value={formData.prizes.first}
                onChange={(e) => setFormData({ ...formData, prizes: { ...formData.prizes, first: e.target.value } })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                placeholder="e.g., 1000 XP + Badge"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                2nd Place Prize
              </label>
              <input
                type="text"
                value={formData.prizes.second}
                onChange={(e) => setFormData({ ...formData, prizes: { ...formData.prizes, second: e.target.value } })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                placeholder="e.g., 500 XP + Badge"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                3rd Place Prize
              </label>
              <input
                type="text"
                value={formData.prizes.third}
                onChange={(e) => setFormData({ ...formData, prizes: { ...formData.prizes, third: e.target.value } })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                placeholder="e.g., 250 XP + Badge"
              />
            </div>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
            {error}
          </div>
        )}

        {/* Actions */}
        <div className="flex gap-3 pt-4">
          {onCancel && (
            <Button type="button" onClick={onCancel} variant="outline" className="flex-1">
              Cancel
            </Button>
          )}
          <Button
            type="submit"
            disabled={isSubmitting}
            isLoading={isSubmitting}
            variant="primary"
            className="flex-1"
          >
            Create Tournament
          </Button>
        </div>
      </form>
    </div>
  );
};
