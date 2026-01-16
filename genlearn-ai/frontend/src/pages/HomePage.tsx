import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { APP_NAME } from '../utils/constants';
import { Button } from '../components/common/Button';

export const HomePage: React.FC = () => {
  const { isAuthenticated } = useAuth();

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-500 to-primary-700">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center text-white mb-12">
          <h1 className="text-6xl font-bold mb-4">{APP_NAME}</h1>
          <p className="text-2xl mb-8">Generative AI-Powered Adaptive Learning</p>
          <div className="flex justify-center space-x-4">
            {isAuthenticated ? (
              <Link to="/dashboard">
                <Button size="lg" variant="secondary">
                  Go to Dashboard
                </Button>
              </Link>
            ) : (
              <Link to="/login">
                <Button size="lg" variant="secondary">
                  Get Started
                </Button>
              </Link>
            )}
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {[
            { icon: '🎨', title: 'Personalized Learning', desc: 'AI-generated content tailored to your level' },
            { icon: '🏆', title: 'Gamification', desc: 'Compete in tournaments and climb leaderboards' },
            { icon: '🗣️', title: 'Voice Enabled', desc: 'Full vocal mode for hands-free learning' },
          ].map((feature, i) => (
            <div key={i} className="bg-white rounded-lg p-6 shadow-xl">
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-600">{feature.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
