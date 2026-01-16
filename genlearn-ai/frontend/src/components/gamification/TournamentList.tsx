import React, { useState, useEffect } from 'react';
import { Tournament } from '../../types';
import { TournamentCard } from './TournamentCard';
import api from '../../services/api';

interface TournamentListProps {
  onJoinTournament?: (tournament: Tournament) => void;
}

export const TournamentList: React.FC<TournamentListProps> = ({ onJoinTournament }) => {
  const [tournaments, setTournaments] = useState<Tournament[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<'all' | 'upcoming' | 'active' | 'completed'>('all');

  useEffect(() => {
    loadTournaments();
  }, [filter]);

  const loadTournaments = async () => {
    try {
      setLoading(true);
      setError(null);
      const filterStatus = filter === 'all' ? undefined : filter;
      const data = await api.getTournaments(filterStatus);
      setTournaments(data.tournaments || []);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to load tournaments');
    } finally {
      setLoading(false);
    }
  };

  const handleJoin = async (tournament: Tournament) => {
    if (onJoinTournament) {
      onJoinTournament(tournament);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-4 border-primary-600 border-t-transparent mx-auto mb-4"></div>
          <p className="text-gray-600">Loading tournaments...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-red-700">
        {error}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Tournaments</h2>
        <p className="text-gray-600">Compete with others and win prizes</p>
      </div>

      {/* Filter Tabs */}
      <div className="flex flex-wrap gap-2">
        {(['all', 'upcoming', 'active', 'completed'] as const).map((status) => (
          <button
            key={status}
            onClick={() => setFilter(status)}
            className={`px-4 py-2 rounded-lg font-medium transition-colors capitalize ${
              filter === status
                ? 'bg-primary-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            {status}
          </button>
        ))}
      </div>

      {/* Tournament Grid */}
      {tournaments.length === 0 ? (
        <div className="text-center py-12 bg-gray-50 rounded-lg">
          <svg className="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No Tournaments</h3>
          <p className="text-gray-600">Check back later for upcoming tournaments</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {tournaments.map((tournament) => (
            <TournamentCard
              key={tournament.tournament_id}
              tournament={tournament}
              onJoin={() => handleJoin(tournament)}
            />
          ))}
        </div>
      )}
    </div>
  );
};
