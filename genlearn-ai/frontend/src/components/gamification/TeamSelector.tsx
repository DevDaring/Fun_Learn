import React, { useState, useEffect } from 'react';
import { Team } from '../../types';
import { Dropdown } from '../common/Dropdown';
import { Button } from '../common/Button';
import api from '../../services/api';

interface TeamSelectorProps {
  value?: string;
  onChange: (teamId: string) => void;
  allowCreate?: boolean;
}

export const TeamSelector: React.FC<TeamSelectorProps> = ({ value, onChange, allowCreate = true }) => {
  const [teams, setTeams] = useState<Team[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newTeamName, setNewTeamName] = useState('');
  const [isCreating, setIsCreating] = useState(false);

  useEffect(() => {
    loadTeams();
  }, []);

  const loadTeams = async () => {
    try {
      setLoading(true);
      const data = await api.getTeams();
      setTeams(data.teams || []);
    } catch (err) {
      console.error('Failed to load teams:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTeam = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTeamName.trim()) return;

    setIsCreating(true);
    try {
      const newTeam = await api.createTeam(newTeamName);
      setTeams([...teams, newTeam]);
      onChange(newTeam.team_id);
      setShowCreateModal(false);
      setNewTeamName('');
    } catch (err: any) {
      alert(err.response?.data?.message || 'Failed to create team');
    } finally {
      setIsCreating(false);
    }
  };

  const teamOptions = teams.map((team) => ({
    value: team.team_id,
    label: `${team.team_name} (${team.members.length} members)`,
  }));

  if (loading) {
    return (
      <div className="flex items-center justify-center p-4">
        <div className="animate-spin rounded-full h-8 w-8 border-4 border-primary-600 border-t-transparent"></div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-end gap-3">
        <div className="flex-1">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select Team
          </label>
          <Dropdown
            options={teamOptions}
            value={value || ''}
            onChange={onChange}
            placeholder="Choose a team..."
          />
        </div>
        {allowCreate && (
          <Button onClick={() => setShowCreateModal(true)} variant="outline">
            <svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Create Team
          </Button>
        )}
      </div>

      {/* Create Team Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl p-6 max-w-md w-full">
            <h3 className="text-xl font-bold text-gray-900 mb-4">Create New Team</h3>
            <form onSubmit={handleCreateTeam}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Team Name
                </label>
                <input
                  type="text"
                  value={newTeamName}
                  onChange={(e) => setNewTeamName(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                  placeholder="Enter team name..."
                  autoFocus
                  required
                />
              </div>
              <div className="flex gap-3">
                <Button
                  type="button"
                  onClick={() => {
                    setShowCreateModal(false);
                    setNewTeamName('');
                  }}
                  variant="outline"
                  className="flex-1"
                >
                  Cancel
                </Button>
                <Button
                  type="submit"
                  disabled={!newTeamName.trim() || isCreating}
                  isLoading={isCreating}
                  variant="primary"
                  className="flex-1"
                >
                  Create
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
