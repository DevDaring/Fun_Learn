import React from 'react';
import { TopNavbar } from './TopNavbar';
import { LeftMenu } from './LeftMenu';
import { RightPanel } from './RightPanel';
import { MainContent } from './MainContent';

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="h-screen flex flex-col">
      <TopNavbar />
      <div className="flex-1 flex overflow-hidden">
        <LeftMenu />
        <MainContent>{children}</MainContent>
        <RightPanel />
      </div>
    </div>
  );
};
