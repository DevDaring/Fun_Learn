import React from 'react';

export const HistoryPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg p-8 shadow-md">
        <h1 className="text-3xl font-bold mb-6">Learning History</h1>
        <div className="text-center py-12 text-gray-500">
          <div className="text-6xl mb-4">📜</div>
          <p>Your learning history will appear here.</p>
          <p className="text-sm mt-2">Complete sessions to build your history!</p>
        </div>
      </div>
    </div>
  );
};
