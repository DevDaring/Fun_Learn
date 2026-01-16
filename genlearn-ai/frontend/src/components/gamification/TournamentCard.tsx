import React from 'react';
import { Tournament } from '../../types';
import { formatDate, formatTime, timeRemaining, getDifficultyColor } from '../../utils/helpers';
import { Button } from '../common/Button';

interface TournamentCardProps {
  tournament: Tournament;
  onJoin?: () => void;
  onView?: () => void;
}

export const TournamentCard: React.FC<TournamentCardProps> = ({ tournament, onJoin, onView }) => {
  const getStatusColor = () => {
    switch (tournament.status) {
      case 'active':
        return 'bg-green-100 text-green-800';
      case 'upcoming':
        return 'bg-blue-100 text-blue-800';
      case 'completed':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const isFull = tournament.current_participants >= tournament.max_participants;
  const canJoin = tournament.status === 'upcoming' && !isFull;

  return (
    <div className="bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-indigo-600 p-6 text-white">
        <div className="flex justify-between items-start mb-3">
          <h3 className="text-xl font-bold">{tournament.name}</h3>
          <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor()}`}>
            {tournament.status}
          </span>
        </div>
        <p className="text-purple-100 text-sm">{tournament.topic}</p>
      </div>

      {/* Content */}
      <div className="p-6 space-y-4">
        {/* Details */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-xs text-gray-500 mb-1">Start Date</p>
            <p className="text-sm font-semibold text-gray-900">
              {formatDate(tournament.start_datetime)}
            </p>
            <p className="text-xs text-gray-600">{formatTime(tournament.start_datetime)}</p>
          </div>
          <div>
            <p className="text-xs text-gray-500 mb-1">Duration</p>
            <p className="text-sm font-semibold text-gray-900">{tournament.duration_minutes} min</p>
          </div>
        </div>

        {/* Difficulty */}
        <div>
          <p className="text-xs text-gray-500 mb-1">Difficulty</p>
          <span className={`inline-block px-3 py-1 rounded-full text-xs font-semibold ${getDifficultyColor(tournament.difficulty_level)}`}>
            Level {tournament.difficulty_level}
          </span>
        </div>

        {/* Participants */}
        <div>
          <p className="text-xs text-gray-500 mb-2">Participants</p>
          <div className="flex items-center gap-2">
            <div className="flex-1 bg-gray-200 rounded-full h-2 overflow-hidden">
              <div
                className="bg-primary-600 h-full transition-all"
                style={{ width: `${(tournament.current_participants / tournament.max_participants) * 100}%` }}
              />
            </div>
            <span className="text-sm font-medium text-gray-700">
              {tournament.current_participants} / {tournament.max_participants}
            </span>
          </div>
        </div>

        {/* Prizes */}
        {tournament.prizes && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
            <p className="text-xs font-semibold text-yellow-900 mb-2">Prizes</p>
            <div className="space-y-1 text-xs text-yellow-800">
              <p>🥇 1st: {tournament.prizes.first}</p>
              <p>🥈 2nd: {tournament.prizes.second}</p>
              <p>🥉 3rd: {tournament.prizes.third}</p>
            </div>
          </div>
        )}

        {/* Time Remaining */}
        {tournament.status === 'upcoming' && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 text-center">
            <p className="text-xs text-blue-700">Starts in</p>
            <p className="text-lg font-bold text-blue-900">{timeRemaining(tournament.start_datetime)}</p>
          </div>
        )}

        {tournament.status === 'active' && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-3 text-center">
            <p className="text-xs text-green-700">Ends in</p>
            <p className="text-lg font-bold text-green-900">{timeRemaining(tournament.end_datetime)}</p>
          </div>
        )}

        {/* Actions */}
        <div className="flex gap-2 pt-2">
          {onView && (
            <Button onClick={onView} variant="outline" className="flex-1" size="sm">
              View Details
            </Button>
          )}
          {onJoin && canJoin && (
            <Button onClick={onJoin} variant="primary" className="flex-1" size="sm">
              Join Tournament
            </Button>
          )}
          {isFull && tournament.status === 'upcoming' && (
            <div className="flex-1 px-3 py-2 bg-gray-200 text-gray-600 rounded-lg text-center text-sm font-medium">
              Full
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
