import React, { useState } from 'react';
import { Button } from '../common/Button';

interface AvatarGalleryProps {
  onSelect: (avatarUrl: string) => void;
  onCancel: () => void;
}

// Pre-defined avatar options
const defaultAvatars = [
  { id: 1, url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Felix', name: 'Felix' },
  { id: 2, url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Aneka', name: 'Aneka' },
  { id: 3, url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Luna', name: 'Luna' },
  { id: 4, url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Max', name: 'Max' },
  { id: 5, url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Sophie', name: 'Sophie' },
  { id: 6, url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Oliver', name: 'Oliver' },
  { id: 7, url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Emma', name: 'Emma' },
  { id: 8, url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Leo', name: 'Leo' },
  { id: 9, url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Mia', name: 'Mia' },
  { id: 10, url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Jack', name: 'Jack' },
  { id: 11, url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Lily', name: 'Lily' },
  { id: 12, url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Charlie', name: 'Charlie' },
  { id: 13, url: 'https://api.dicebear.com/7.x/adventurer/svg?seed=Midnight', name: 'Midnight' },
  { id: 14, url: 'https://api.dicebear.com/7.x/adventurer/svg?seed=Sunny', name: 'Sunny' },
  { id: 15, url: 'https://api.dicebear.com/7.x/adventurer/svg?seed=Rocky', name: 'Rocky' },
  { id: 16, url: 'https://api.dicebear.com/7.x/adventurer/svg?seed=Bella', name: 'Bella' },
  { id: 17, url: 'https://api.dicebear.com/7.x/bottts/svg?seed=Buster', name: 'Buster' },
  { id: 18, url: 'https://api.dicebear.com/7.x/bottts/svg?seed=Coco', name: 'Coco' },
  { id: 19, url: 'https://api.dicebear.com/7.x/bottts/svg?seed=Daisy', name: 'Daisy' },
  { id: 20, url: 'https://api.dicebear.com/7.x/bottts/svg?seed=Duke', name: 'Duke' },
];

export const AvatarGallery: React.FC<AvatarGalleryProps> = ({ onSelect, onCancel }) => {
  const [selectedAvatar, setSelectedAvatar] = useState<string | null>(null);
  const [filter, setFilter] = useState<'all' | 'human' | 'adventure' | 'robot'>('all');

  const filteredAvatars = defaultAvatars.filter((avatar) => {
    if (filter === 'all') return true;
    if (filter === 'human') return avatar.url.includes('avataaars');
    if (filter === 'adventure') return avatar.url.includes('adventurer');
    if (filter === 'robot') return avatar.url.includes('bottts');
    return true;
  });

  const handleSelect = () => {
    if (selectedAvatar) {
      onSelect(selectedAvatar);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Choose from Gallery</h2>

      {/* Filter Tabs */}
      <div className="mb-6 flex flex-wrap gap-2">
        <button
          onClick={() => setFilter('all')}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            filter === 'all'
              ? 'bg-primary-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          All Avatars
        </button>
        <button
          onClick={() => setFilter('human')}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            filter === 'human'
              ? 'bg-primary-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          Human Style
        </button>
        <button
          onClick={() => setFilter('adventure')}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            filter === 'adventure'
              ? 'bg-primary-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          Adventurer
        </button>
        <button
          onClick={() => setFilter('robot')}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            filter === 'robot'
              ? 'bg-primary-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          Robot
        </button>
      </div>

      {/* Avatar Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 mb-6 max-h-96 overflow-y-auto p-2">
        {filteredAvatars.map((avatar) => (
          <button
            key={avatar.id}
            onClick={() => setSelectedAvatar(avatar.url)}
            className={`relative group rounded-lg overflow-hidden border-4 transition-all hover:scale-105 ${
              selectedAvatar === avatar.url
                ? 'border-primary-600 shadow-lg scale-105'
                : 'border-gray-200 hover:border-primary-400'
            }`}
          >
            <div className="aspect-square bg-gradient-to-br from-gray-50 to-gray-100">
              <img
                src={avatar.url}
                alt={avatar.name}
                className="w-full h-full object-cover"
              />
            </div>
            <div className={`absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-2 transition-opacity ${
              selectedAvatar === avatar.url ? 'opacity-100' : 'opacity-0 group-hover:opacity-100'
            }`}>
              <p className="text-white text-xs font-semibold text-center">{avatar.name}</p>
            </div>
            {selectedAvatar === avatar.url && (
              <div className="absolute top-2 right-2 bg-primary-600 text-white rounded-full p-1">
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
            )}
          </button>
        ))}
      </div>

      {/* Selected Avatar Preview */}
      {selectedAvatar && (
        <div className="mb-6 bg-gradient-to-br from-primary-50 to-purple-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 text-center">Selected Avatar</h3>
          <div className="flex justify-center">
            <div className="w-32 h-32 rounded-lg overflow-hidden border-4 border-primary-600 shadow-xl">
              <img
                src={selectedAvatar}
                alt="Selected avatar"
                className="w-full h-full object-cover"
              />
            </div>
          </div>
        </div>
      )}

      {/* Info Box */}
      <div className="mb-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 className="font-semibold text-blue-900 mb-2 flex items-center">
          <svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          About Gallery Avatars
        </h4>
        <p className="text-sm text-blue-800">
          Choose from our curated collection of avatars. These avatars are ready to use
          and will represent you across the platform. You can change your avatar anytime
          from your profile settings.
        </p>
      </div>

      {/* Action Buttons */}
      <div className="flex gap-3">
        <Button onClick={onCancel} variant="outline" className="flex-1">
          Cancel
        </Button>
        <Button
          onClick={handleSelect}
          disabled={!selectedAvatar}
          variant="primary"
          className="flex-1"
        >
          <svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
          Select Avatar
        </Button>
      </div>
    </div>
  );
};
