import React from 'react';

export const TournamentsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg p-8 shadow-md">
        <h1 className="text-3xl font-bold mb-6">Tournaments</h1>
        <div className="text-center py-12 text-gray-500">
          <div className="text-6xl mb-4">🏆</div>
          <p>Join exciting learning tournaments and compete with others!</p>
          <p className="text-sm mt-2">Check back soon for upcoming tournaments.</p>
        </div>
      </div>
    </div>
  );
};
