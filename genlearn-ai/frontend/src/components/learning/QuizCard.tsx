import React, { useState } from 'react';

interface QuizOption {
    key: string;
    text: string;
}

interface QuizCardProps {
    questionNumber: number;
    totalQuestions: number;
    questionText: string;
    options: QuizOption[];
    isMultiSelect: boolean;
    points: number;
    onAnswer: (selectedKeys: string[]) => void;
    isSubmitting?: boolean;
}

export const QuizCard: React.FC<QuizCardProps> = ({
    questionNumber,
    totalQuestions,
    questionText,
    options,
    isMultiSelect,
    points,
    onAnswer,
    isSubmitting = false
}) => {
    const [selectedOptions, setSelectedOptions] = useState<string[]>([]);

    const handleOptionClick = (key: string) => {
        if (isMultiSelect) {
            setSelectedOptions(prev =>
                prev.includes(key)
                    ? prev.filter(k => k !== key)
                    : [...prev, key]
            );
        } else {
            setSelectedOptions([key]);
        }
    };

    const handleSubmit = () => {
        if (selectedOptions.length > 0) {
            onAnswer(selectedOptions);
        }
    };

    const getOptionStyle = (key: string) => {
        const isSelected = selectedOptions.includes(key);
        if (isSelected) {
            return 'border-primary-600 bg-primary-50 ring-2 ring-primary-300';
        }
        return 'border-gray-200 hover:border-primary-300 hover:bg-gray-50';
    };

    return (
        <div className="bg-white rounded-2xl shadow-xl p-6 border-2 border-gray-100">
            {/* Header */}
            <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                    <span className="bg-primary-100 text-primary-700 px-3 py-1 rounded-full text-sm font-semibold">
                        Question {questionNumber}/{totalQuestions}
                    </span>
                    {isMultiSelect && (
                        <span className="bg-purple-100 text-purple-700 px-2 py-1 rounded-full text-xs">
                            Select all that apply
                        </span>
                    )}
                </div>
                <div className="flex items-center gap-1 text-yellow-600">
                    <span className="text-lg">⭐</span>
                    <span className="font-bold">{points} pts</span>
                </div>
            </div>

            {/* Question */}
            <h3 className="text-xl font-bold text-gray-900 mb-6 leading-relaxed">
                {questionText}
            </h3>

            {/* Options */}
            <div className="space-y-3 mb-6">
                {options.map((option) => (
                    <button
                        key={option.key}
                        onClick={() => handleOptionClick(option.key)}
                        disabled={isSubmitting}
                        className={`w-full text-left p-4 rounded-xl border-2 transition-all flex items-start gap-3 ${getOptionStyle(option.key)} ${isSubmitting ? 'opacity-50 cursor-not-allowed' : ''}`}
                    >
                        <span className={`flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center font-bold text-sm ${selectedOptions.includes(option.key)
                                ? 'bg-primary-600 text-white'
                                : 'bg-gray-100 text-gray-600'
                            }`}>
                            {option.key}
                        </span>
                        <span className="text-gray-800 pt-1">{option.text}</span>
                    </button>
                ))}
            </div>

            {/* Submit Button */}
            <button
                onClick={handleSubmit}
                disabled={selectedOptions.length === 0 || isSubmitting}
                className={`w-full py-4 rounded-xl font-bold text-lg transition-all ${selectedOptions.length > 0 && !isSubmitting
                        ? 'bg-gradient-to-r from-primary-600 to-primary-700 text-white hover:from-primary-700 hover:to-primary-800 shadow-lg'
                        : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                    }`}
            >
                {isSubmitting ? (
                    <span className="flex items-center justify-center gap-2">
                        <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                        </svg>
                        Checking...
                    </span>
                ) : (
                    '✓ Submit Answer'
                )}
            </button>
        </div>
    );
};

interface QuizResultProps {
    isCorrect: boolean;
    correctAnswer: string;
    explanation: string;
    pointsEarned: number;
    streak: number;
    onContinue: () => void;
}

export const QuizResult: React.FC<QuizResultProps> = ({
    isCorrect,
    correctAnswer,
    explanation,
    pointsEarned,
    streak,
    onContinue
}) => {
    return (
        <div className={`rounded-2xl p-6 border-2 ${isCorrect ? 'bg-green-50 border-green-300' : 'bg-red-50 border-red-300'}`}>
            {/* Result Header */}
            <div className="text-center mb-4">
                <div className="text-5xl mb-2">{isCorrect ? '🎉' : '😔'}</div>
                <h3 className={`text-2xl font-bold ${isCorrect ? 'text-green-700' : 'text-red-700'}`}>
                    {isCorrect ? 'Correct!' : 'Not quite...'}
                </h3>
            </div>

            {/* Points Earned */}
            <div className="text-center mb-4">
                <div className="inline-flex items-center gap-2 bg-yellow-100 text-yellow-700 px-4 py-2 rounded-full">
                    <span className="text-xl">⭐</span>
                    <span className="font-bold">+{pointsEarned} points</span>
                </div>
                {streak >= 3 && (
                    <div className="mt-2 text-orange-600 font-semibold">
                        🔥 {streak} streak bonus!
                    </div>
                )}
            </div>

            {/* Correct Answer (if wrong) */}
            {!isCorrect && (
                <div className="bg-white rounded-xl p-4 mb-4 border border-gray-200">
                    <p className="text-sm text-gray-500 mb-1">Correct answer:</p>
                    <p className="font-semibold text-gray-800">{correctAnswer}</p>
                </div>
            )}

            {/* Explanation */}
            <div className="bg-white rounded-xl p-4 mb-6 border border-gray-200">
                <p className="text-sm text-gray-500 mb-1">💡 Explanation:</p>
                <p className="text-gray-700">{explanation}</p>
            </div>

            {/* Continue Button */}
            <button
                onClick={onContinue}
                className="w-full py-4 rounded-xl font-bold text-lg bg-gradient-to-r from-primary-600 to-primary-700 text-white hover:from-primary-700 hover:to-primary-800 shadow-lg transition-all"
            >
                Continue →
            </button>
        </div>
    );
};
