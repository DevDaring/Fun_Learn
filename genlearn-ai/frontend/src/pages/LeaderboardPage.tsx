import React from 'react';

export const LeaderboardPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg p-8 shadow-md">
        <h1 className="text-3xl font-bold mb-6">Leaderboard</h1>
        <div className="text-center py-12 text-gray-500">
          <div className="text-6xl mb-4">📈</div>
          <p>Top learners will be displayed here.</p>
          <p className="text-sm mt-2">Keep learning to climb the ranks!</p>
        </div>
      </div>
    </div>
  );
};
