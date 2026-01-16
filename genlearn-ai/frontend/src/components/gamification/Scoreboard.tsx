import React, { useState, useEffect } from 'react';
import { LeaderboardEntry } from '../../types';
import api from '../../services/api';
import { calculateLevel } from '../../utils/helpers';

interface ScoreboardProps {
  scope?: 'global' | 'tournament';
  tournamentId?: string;
}

export const Scoreboard: React.FC<ScoreboardProps> = ({ scope = 'global', tournamentId }) => {
  const [entries, setEntries] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadLeaderboard();
  }, [scope, tournamentId]);

  const loadLeaderboard = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getLeaderboard(scope, tournamentId);
      setEntries(data.leaderboard || []);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to load leaderboard');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-4 border-primary-600 border-t-transparent mx-auto mb-4"></div>
            <p className="text-gray-600">Loading leaderboard...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
          {error}
        </div>
      </div>
    );
  }

  const getRankColor = (rank: number) => {
    if (rank === 1) return 'bg-gradient-to-r from-yellow-400 to-yellow-600 text-white';
    if (rank === 2) return 'bg-gradient-to-r from-gray-300 to-gray-500 text-white';
    if (rank === 3) return 'bg-gradient-to-r from-orange-400 to-orange-600 text-white';
    return 'bg-gray-100 text-gray-700';
  };

  const getRankIcon = (rank: number) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return rank;
  };

  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary-600 to-purple-600 text-white p-6">
        <h2 className="text-2xl font-bold flex items-center">
          <svg className="w-8 h-8 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
          </svg>
          {scope === 'global' ? 'Global Leaderboard' : 'Tournament Leaderboard'}
        </h2>
        <p className="text-primary-100 mt-1">Top performers across the platform</p>
      </div>

      {/* Leaderboard List */}
      {entries.length === 0 ? (
        <div className="p-12 text-center text-gray-500">
          <svg className="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          <p>No entries yet</p>
        </div>
      ) : (
        <div className="divide-y divide-gray-200">
          {entries.map((entry, index) => (
            <div
              key={entry.user_id || entry.team_id || index}
              className={`flex items-center p-4 hover:bg-gray-50 transition-colors ${
                index < 3 ? 'bg-gradient-to-r from-primary-50/30 to-transparent' : ''
              }`}
            >
              {/* Rank */}
              <div className={`flex-shrink-0 w-16 h-16 rounded-full flex items-center justify-center font-bold text-xl mr-4 ${getRankColor(entry.rank)}`}>
                {getRankIcon(entry.rank)}
              </div>

              {/* Avatar */}
              {entry.avatar_url && (
                <div className="flex-shrink-0 w-12 h-12 rounded-full overflow-hidden mr-4 border-2 border-gray-200">
                  <img
                    src={entry.avatar_url}
                    alt={entry.display_name}
                    className="w-full h-full object-cover"
                  />
                </div>
              )}

              {/* Name and Info */}
              <div className="flex-1 min-w-0">
                <h3 className="text-lg font-semibold text-gray-900 truncate">{entry.display_name}</h3>
                <p className="text-sm text-gray-500">
                  Level {calculateLevel(entry.score)} • {entry.score} XP
                </p>
              </div>

              {/* Score Badge */}
              <div className="flex-shrink-0 ml-4 text-right">
                <div className="bg-primary-600 text-white px-4 py-2 rounded-lg">
                  <div className="text-2xl font-bold">{entry.score}</div>
                  <div className="text-xs opacity-90">points</div>
                </div>
              </div>

              {/* Trophy for top 3 */}
              {entry.rank <= 3 && (
                <div className="flex-shrink-0 ml-4">
                  <svg className="w-8 h-8 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Footer */}
      <div className="bg-gray-50 p-4 text-center text-sm text-gray-600">
        <p>Keep learning to climb the leaderboard!</p>
      </div>
    </div>
  );
};
