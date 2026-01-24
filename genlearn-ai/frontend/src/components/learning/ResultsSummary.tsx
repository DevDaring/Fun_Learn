import React from 'react';

interface ResultsSummaryProps {
    topic: string;
    totalQuestions: number;
    correctAnswers: number;
    totalScore: number;
    xpEarned: number;
    timeSpent: number; // in seconds
    longestStreak: number;
    onPlayAgain: () => void;
    onGoHome: () => void;
}

export const ResultsSummary: React.FC<ResultsSummaryProps> = ({
    topic,
    totalQuestions,
    correctAnswers,
    totalScore,
    xpEarned,
    timeSpent,
    longestStreak,
    onPlayAgain,
    onGoHome
}) => {
    const accuracyRate = totalQuestions > 0 ? Math.round((correctAnswers / totalQuestions) * 100) : 0;

    const formatTime = (seconds: number): string => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    const getPerformanceEmoji = (): string => {
        if (accuracyRate >= 90) return '🏆';
        if (accuracyRate >= 70) return '🌟';
        if (accuracyRate >= 50) return '👍';
        return '💪';
    };

    const getPerformanceMessage = (): string => {
        if (accuracyRate >= 90) return 'Outstanding! You mastered this topic!';
        if (accuracyRate >= 70) return 'Great job! Keep up the good work!';
        if (accuracyRate >= 50) return 'Good effort! Practice makes perfect!';
        return 'Keep trying! Every attempt makes you stronger!';
    };

    return (
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden max-w-lg mx-auto">
            {/* Header */}
            <div className="bg-gradient-to-r from-primary-600 to-purple-600 p-6 text-white text-center">
                <div className="text-6xl mb-2">{getPerformanceEmoji()}</div>
                <h2 className="text-2xl font-bold mb-1">Session Complete!</h2>
                <p className="opacity-90">{getPerformanceMessage()}</p>
            </div>

            {/* Topic */}
            <div className="px-6 py-4 bg-gray-50 border-b border-gray-100">
                <p className="text-sm text-gray-500">Topic</p>
                <p className="font-semibold text-gray-800">{topic}</p>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-2 gap-4 p-6">
                {/* Score */}
                <div className="bg-gradient-to-br from-yellow-50 to-yellow-100 rounded-xl p-4 text-center">
                    <div className="text-3xl mb-1">⭐</div>
                    <div className="text-2xl font-bold text-yellow-700">{totalScore}</div>
                    <div className="text-sm text-yellow-600">Total Score</div>
                </div>

                {/* XP Earned */}
                <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl p-4 text-center">
                    <div className="text-3xl mb-1">✨</div>
                    <div className="text-2xl font-bold text-purple-700">+{xpEarned}</div>
                    <div className="text-sm text-purple-600">XP Earned</div>
                </div>

                {/* Accuracy */}
                <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-xl p-4 text-center">
                    <div className="text-3xl mb-1">🎯</div>
                    <div className="text-2xl font-bold text-green-700">{accuracyRate}%</div>
                    <div className="text-sm text-green-600">{correctAnswers}/{totalQuestions} Correct</div>
                </div>

                {/* Time */}
                <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-4 text-center">
                    <div className="text-3xl mb-1">⏱️</div>
                    <div className="text-2xl font-bold text-blue-700">{formatTime(timeSpent)}</div>
                    <div className="text-sm text-blue-600">Time Spent</div>
                </div>
            </div>

            {/* Streak Badge */}
            {longestStreak >= 3 && (
                <div className="mx-6 mb-4 bg-gradient-to-r from-orange-100 to-red-100 rounded-xl p-4 flex items-center gap-3">
                    <span className="text-3xl">🔥</span>
                    <div>
                        <div className="font-bold text-orange-700">{longestStreak} Answer Streak!</div>
                        <div className="text-sm text-orange-600">Your best streak this session</div>
                    </div>
                </div>
            )}

            {/* Actions */}
            <div className="p-6 space-y-3">
                <button
                    onClick={onPlayAgain}
                    className="w-full py-4 rounded-xl font-bold text-lg bg-gradient-to-r from-primary-600 to-primary-700 text-white hover:from-primary-700 hover:to-primary-800 shadow-lg transition-all"
                >
                    🔄 Play Again
                </button>
                <button
                    onClick={onGoHome}
                    className="w-full py-3 rounded-xl font-semibold text-gray-600 hover:bg-gray-100 transition-all"
                >
                    ← Back to Dashboard
                </button>
            </div>
        </div>
    );
};
