import React from 'react';

interface TextOverlayData {
    text: string;
    position: 'top' | 'center' | 'bottom';
    style: 'speech_bubble' | 'caption' | 'dramatic';
}

interface SceneDisplayProps {
    imageUrl: string;
    textOverlay: TextOverlayData;
    isLoading?: boolean;
}

export const SceneDisplay: React.FC<SceneDisplayProps> = ({
    imageUrl,
    textOverlay,
    isLoading = false
}) => {
    const getPositionClass = (position: string): string => {
        switch (position) {
            case 'top':
                return 'top-4 left-0 right-0';
            case 'center':
                return 'top-1/2 left-0 right-0 -translate-y-1/2';
            case 'bottom':
            default:
                return 'bottom-4 left-0 right-0';
        }
    };

    const getStyleClass = (style: string): string => {
        switch (style) {
            case 'speech_bubble':
                return 'mx-4 bg-white rounded-2xl p-4 shadow-lg border-2 border-gray-200 relative before:content-[""] before:absolute before:bottom-[-12px] before:left-8 before:border-8 before:border-transparent before:border-t-white';
            case 'dramatic':
                return 'bg-gradient-to-r from-purple-900/90 via-indigo-900/90 to-purple-900/90 py-4 px-6 text-center font-bold text-xl text-white tracking-wide';
            case 'caption':
            default:
                return 'mx-4 bg-black/70 backdrop-blur-sm rounded-xl p-4 text-white';
        }
    };

    if (isLoading) {
        return (
            <div className="relative w-full aspect-[3/4] bg-gradient-to-br from-gray-200 to-gray-300 rounded-2xl overflow-hidden animate-pulse">
                <div className="absolute inset-0 flex items-center justify-center">
                    <div className="text-center">
                        <div className="text-4xl mb-2">🎨</div>
                        <p className="text-gray-600">Generating scene...</p>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="relative w-full aspect-[3/4] rounded-2xl overflow-hidden shadow-2xl">
            {/* Scene Image */}
            <img
                src={imageUrl}
                alt="Story scene"
                className="w-full h-full object-cover"
                onError={(e) => {
                    (e.target as HTMLImageElement).src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 400"><rect fill="%23f3f4f6" width="300" height="400"/><text x="150" y="200" text-anchor="middle" fill="%239ca3af" font-size="60">📖</text></svg>';
                }}
            />

            {/* Text Overlay */}
            {textOverlay && textOverlay.text && (
                <div className={`absolute ${getPositionClass(textOverlay.position)}`}>
                    <div className={getStyleClass(textOverlay.style)}>
                        {textOverlay.text}
                    </div>
                </div>
            )}
        </div>
    );
};
