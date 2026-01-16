import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { cn } from '../../utils/helpers';

interface MenuItem {
  path: string;
  label: string;
  icon: string;
  adminOnly?: boolean;
}

const menuItems: MenuItem[] = [
  { path: '/dashboard', label: 'Dashboard', icon: '📊' },
  { path: '/learning', label: 'Start Learning', icon: '📚' },
  { path: '/avatar', label: 'My Avatar', icon: '👤' },
  { path: '/characters', label: 'Characters', icon: '🎭' },
  { path: '/tournaments', label: 'Tournaments', icon: '🏆' },
  { path: '/leaderboard', label: 'Leaderboard', icon: '📈' },
  { path: '/history', label: 'History', icon: '📜' },
  { path: '/profile', label: 'Profile', icon: '⚙️' },
  { path: '/admin', label: 'Admin Panel', icon: '🔧', adminOnly: true },
];

export const LeftMenu: React.FC = () => {
  const location = useLocation();
  const { isAdmin } = useAuth();

  const filteredItems = menuItems.filter(item => !item.adminOnly || isAdmin);

  return (
    <aside className="w-64 bg-white border-r border-gray-200 h-full overflow-y-auto">
      <nav className="p-4 space-y-2">
        {filteredItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={cn(
              'flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors',
              location.pathname.startsWith(item.path)
                ? 'bg-primary-100 text-primary-700 font-semibold'
                : 'text-gray-700 hover:bg-gray-100'
            )}
          >
            <span className="text-2xl">{item.icon}</span>
            <span>{item.label}</span>
          </Link>
        ))}
      </nav>
    </aside>
  );
};
