import React, { useState } from 'react';
import { DrawingCanvas } from './DrawingCanvas';
import { ImageUploader } from './ImageUploader';
import { AvatarGallery } from './AvatarGallery';
import { Button } from '../common/Button';
import api from '../../services/api';

interface AvatarCreatorProps {
  onComplete: (avatar: any) => void;
  onCancel: () => void;
}

type CreationMethod = 'gallery' | 'upload' | 'draw' | null;

export const AvatarCreator: React.FC<AvatarCreatorProps> = ({ onComplete, onCancel }) => {
  const [method, setMethod] = useState<CreationMethod>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [avatarName, setAvatarName] = useState('');
  const [visualStyle, setVisualStyle] = useState<'cartoon' | 'realistic'>('cartoon');
  const [showNameDialog, setShowNameDialog] = useState(false);
  const [pendingData, setPendingData] = useState<{ data: string | File; method: string } | null>(null);

  const handleMethodSelect = (selectedMethod: CreationMethod) => {
    setMethod(selectedMethod);
    setError(null);
  };

  const handleGallerySelect = (avatarUrl: string) => {
    // For gallery selection, we can directly complete
    onComplete({
      image_url: avatarUrl,
      creation_method: 'gallery',
      name: 'Gallery Avatar'
    });
  };

  const handleDrawingSave = (imageData: string) => {
    setPendingData({ data: imageData, method: 'draw' });
    setShowNameDialog(true);
  };

  const handleFileUpload = (file: File) => {
    setPendingData({ data: file, method: 'upload' });
    setShowNameDialog(true);
  };

  const handleFinalSubmit = async () => {
    if (!pendingData || !avatarName.trim()) return;

    setIsSubmitting(true);
    setError(null);

    try {
      let result;
      if (pendingData.method === 'draw') {
        result = await api.createAvatarFromDrawing(
          pendingData.data as string,
          avatarName,
          visualStyle
        );
      } else if (pendingData.method === 'upload') {
        result = await api.createAvatarFromUpload(
          pendingData.data as File,
          avatarName,
          visualStyle
        );
      }
      onComplete(result);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to create avatar');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (showNameDialog && pendingData) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6 max-w-md mx-auto">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Name Your Avatar</h2>

        <div className="space-y-4 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Avatar Name
            </label>
            <input
              type="text"
              value={avatarName}
              onChange={(e) => setAvatarName(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              placeholder="e.g., My Cool Avatar"
              autoFocus
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Visual Style
            </label>
            <div className="grid grid-cols-2 gap-3">
              <button
                onClick={() => setVisualStyle('cartoon')}
                className={`p-4 border-2 rounded-lg transition-colors ${
                  visualStyle === 'cartoon'
                    ? 'border-primary-600 bg-primary-50'
                    : 'border-gray-300 hover:border-gray-400'
                }`}
              >
                <div className="text-2xl mb-1">🎨</div>
                <div className="font-medium">Cartoon</div>
              </button>
              <button
                onClick={() => setVisualStyle('realistic')}
                className={`p-4 border-2 rounded-lg transition-colors ${
                  visualStyle === 'realistic'
                    ? 'border-primary-600 bg-primary-50'
                    : 'border-gray-300 hover:border-gray-400'
                }`}
              >
                <div className="text-2xl mb-1">📸</div>
                <div className="font-medium">Realistic</div>
              </button>
            </div>
          </div>
        </div>

        {error && (
          <div className="mb-4 bg-red-50 border border-red-200 rounded-lg p-3 text-red-700 text-sm">
            {error}
          </div>
        )}

        <div className="flex gap-3">
          <Button
            onClick={() => {
              setShowNameDialog(false);
              setPendingData(null);
              setAvatarName('');
            }}
            variant="outline"
            className="flex-1"
          >
            Back
          </Button>
          <Button
            onClick={handleFinalSubmit}
            disabled={!avatarName.trim() || isSubmitting}
            isLoading={isSubmitting}
            variant="primary"
            className="flex-1"
          >
            Create Avatar
          </Button>
        </div>
      </div>
    );
  }

  if (method === 'draw') {
    return <DrawingCanvas onSave={handleDrawingSave} onCancel={() => setMethod(null)} />;
  }

  if (method === 'upload') {
    return <ImageUploader onUpload={handleFileUpload} onCancel={() => setMethod(null)} />;
  }

  if (method === 'gallery') {
    return <AvatarGallery onSelect={handleGallerySelect} onCancel={() => setMethod(null)} />;
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-8 max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Create Your Avatar</h2>
        <p className="text-gray-600">Choose how you want to create your personalized avatar</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {/* Gallery Option */}
        <button
          onClick={() => handleMethodSelect('gallery')}
          className="group p-6 border-2 border-gray-300 rounded-xl hover:border-primary-600 hover:shadow-lg transition-all"
        >
          <div className="w-20 h-20 mx-auto mb-4 bg-gradient-to-br from-blue-100 to-blue-200 rounded-full flex items-center justify-center group-hover:scale-110 transition-transform">
            <svg className="w-10 h-10 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">Choose from Gallery</h3>
          <p className="text-gray-600 text-sm">Select from our pre-made avatar collection</p>
        </button>

        {/* Upload Option */}
        <button
          onClick={() => handleMethodSelect('upload')}
          className="group p-6 border-2 border-gray-300 rounded-xl hover:border-primary-600 hover:shadow-lg transition-all"
        >
          <div className="w-20 h-20 mx-auto mb-4 bg-gradient-to-br from-green-100 to-green-200 rounded-full flex items-center justify-center group-hover:scale-110 transition-transform">
            <svg className="w-10 h-10 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">Upload Image</h3>
          <p className="text-gray-600 text-sm">Use your own photo or image</p>
        </button>

        {/* Draw Option */}
        <button
          onClick={() => handleMethodSelect('draw')}
          className="group p-6 border-2 border-gray-300 rounded-xl hover:border-primary-600 hover:shadow-lg transition-all"
        >
          <div className="w-20 h-20 mx-auto mb-4 bg-gradient-to-br from-purple-100 to-purple-200 rounded-full flex items-center justify-center group-hover:scale-110 transition-transform">
            <svg className="w-10 h-10 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
            </svg>
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">Draw Avatar</h3>
          <p className="text-gray-600 text-sm">Create your own using our drawing tool</p>
        </button>
      </div>

      <div className="text-center">
        <Button onClick={onCancel} variant="outline">
          Cancel
        </Button>
      </div>
    </div>
  );
};
