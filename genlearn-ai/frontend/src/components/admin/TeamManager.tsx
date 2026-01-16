import React, { useState, useEffect } from 'react';
import { Team } from '../../types';
import { Button } from '../common/Button';
import api from '../../services/api';

export const TeamManager: React.FC = () => {
  const [teams, setTeams] = useState<Team[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedTeam, setSelectedTeam] = useState<Team | null>(null);

  useEffect(() => {
    loadTeams();
  }, []);

  const loadTeams = async () => {
    try {
      setLoading(true);
      const data = await api.getTeams();
      setTeams(data.teams || []);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to load teams');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-4 border-primary-600 border-t-transparent"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Team Management</h2>
        <p className="text-gray-600">View and manage all teams</p>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
          {error}
        </div>
      )}

      {teams.length === 0 ? (
        <div className="text-center py-12 bg-gray-50 rounded-lg">
          <svg className="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          <p className="text-gray-600">No teams found</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
          {teams.map((team) => (
            <div key={team.team_id} className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-lg font-bold text-gray-900">{team.team_name}</h3>
                  <p className="text-sm text-gray-600">Rank #{team.rank}</p>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-primary-600">{team.total_score}</p>
                  <p className="text-xs text-gray-600">Total Score</p>
                </div>
              </div>

              <div className="mb-4">
                <p className="text-sm font-medium text-gray-700 mb-2">Members ({team.members.length})</p>
                <div className="space-y-2">
                  {team.members.slice(0, 3).map((member) => (
                    <div key={member.user_id} className="flex items-center gap-2 text-sm">
                      {member.avatar_url && (
                        <img src={member.avatar_url} alt="" className="w-6 h-6 rounded-full" />
                      )}
                      <span className="text-gray-900">{member.display_name}</span>
                      {member.role === 'leader' && (
                        <span className="text-xs bg-primary-100 text-primary-700 px-2 py-0.5 rounded">Leader</span>
                      )}
                    </div>
                  ))}
                  {team.members.length > 3 && (
                    <p className="text-xs text-gray-500">+{team.members.length - 3} more</p>
                  )}
                </div>
              </div>

              <Button
                onClick={() => setSelectedTeam(team)}
                variant="outline"
                size="sm"
                className="w-full"
              >
                View Details
              </Button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
