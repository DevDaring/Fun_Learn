import React from 'react';

interface MainContentProps {
  children: React.ReactNode;
}

export const MainContent: React.FC<MainContentProps> = ({ children }) => {
  return (
    <main className="flex-1 overflow-y-auto bg-gray-50">
      <div className="container mx-auto p-6">
        {children}
      </div>
    </main>
  );
};
