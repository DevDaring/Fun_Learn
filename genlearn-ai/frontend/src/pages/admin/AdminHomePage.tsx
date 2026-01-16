import React from 'react';
import { Link } from 'react-router-dom';

export const AdminHomePage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg p-8 shadow-md">
        <h1 className="text-3xl font-bold mb-6">Admin Dashboard</h1>

        <div className="grid md:grid-cols-2 gap-6">
          <Link to="/admin/tournaments">
            <div className="p-6 border-2 border-gray-300 rounded-lg hover:border-primary-600 transition-colors">
              <div className="text-4xl mb-4">🏆</div>
              <h3 className="text-xl font-semibold mb-2">Manage Tournaments</h3>
              <p className="text-gray-600">Create and manage tournaments</p>
            </div>
          </Link>

          <Link to="/admin/teams">
            <div className="p-6 border-2 border-gray-300 rounded-lg hover:border-primary-600 transition-colors">
              <div className="text-4xl mb-4">👥</div>
              <h3 className="text-xl font-semibold mb-2">Manage Teams</h3>
              <p className="text-gray-600">View and manage teams</p>
            </div>
          </Link>

          <Link to="/admin/questions">
            <div className="p-6 border-2 border-gray-300 rounded-lg hover:border-primary-600 transition-colors">
              <div className="text-4xl mb-4">❓</div>
              <h3 className="text-xl font-semibold mb-2">Upload Questions</h3>
              <p className="text-gray-600">Upload MCQ and descriptive questions</p>
            </div>
          </Link>

          <Link to="/admin/users">
            <div className="p-6 border-2 border-gray-300 rounded-lg hover:border-primary-600 transition-colors">
              <div className="text-4xl mb-4">👤</div>
              <h3 className="text-xl font-semibold mb-2">Manage Users</h3>
              <p className="text-gray-600">View and manage user accounts</p>
            </div>
          </Link>
        </div>
      </div>
    </div>
  );
};
