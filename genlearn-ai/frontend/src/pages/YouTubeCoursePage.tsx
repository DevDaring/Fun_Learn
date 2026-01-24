import React, { useState } from 'react';
import api from '../services/api';

interface Chapter {
    chapter_number: number;
    title: string;
    start_time: string;
    end_time: string;
    summary: string;
    key_terms?: string[];
}

interface Flashcard {
    front: string;
    back: string;
}

interface MCQ {
    question: string;
    options: string[];
    correct: string;
    explanation: string;
}

interface CourseData {
    course_title: string;
    subject: string;
    difficulty_level: string;
    chapters: Chapter[];
    quiz?: { mcq: MCQ[] };
    flashcards?: Flashcard[];
}

export const YouTubeCoursePage: React.FC = () => {
    const [step, setStep] = useState<'input' | 'course'>('input');
    const [videoUrl, setVideoUrl] = useState('');
    const [transcript, setTranscript] = useState('');
    const [title, setTitle] = useState('');
    const [course, setCourse] = useState<CourseData | null>(null);
    const [loading, setLoading] = useState(false);
    const [activeTab, setActiveTab] = useState<'chapters' | 'quiz' | 'flashcards'>('chapters');
    const [currentQuiz, setCurrentQuiz] = useState(0);
    const [showAnswer, setShowAnswer] = useState(false);
    const [flippedCard, setFlippedCard] = useState<number | null>(null);

    const handleGenerate = async () => {
        if (!transcript.trim() && !title.trim()) return;

        setLoading(true);
        try {
            const response = await api.client.post('/features/youtube/process', {
                video_url: videoUrl,
                transcript: transcript,
                title: title || 'Educational Video',
                channel: 'Unknown',
                duration: 'Unknown'
            });

            setCourse(response.data);
            setStep('course');
        } catch (err) {
            console.error('Course generation failed:', err);
            alert('Failed to generate course. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            <div className="bg-white rounded-xl p-6 shadow-lg">
                <h1 className="text-3xl font-bold text-gray-900 mb-2">📺 YouTube to Course</h1>
                <p className="text-gray-600">Transform any video into a structured course with chapters, quizzes, and flashcards!</p>
            </div>

            {step === 'input' && (
                <div className="bg-gradient-to-br from-rose-50 to-pink-50 rounded-xl p-6">
                    <div className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Video Title</label>
                            <input
                                type="text"
                                value={title}
                                onChange={(e) => setTitle(e.target.value)}
                                placeholder="e.g., Quantum Computing Explained"
                                className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-500"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">YouTube URL (Optional)</label>
                            <input
                                type="text"
                                value={videoUrl}
                                onChange={(e) => setVideoUrl(e.target.value)}
                                placeholder="https://youtube.com/watch?v=..."
                                className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-500"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                Video Transcript/Content
                                <span className="text-gray-500 text-xs ml-2">(Paste the video transcript or your notes)</span>
                            </label>
                            <textarea
                                value={transcript}
                                onChange={(e) => setTranscript(e.target.value)}
                                placeholder="Paste the video transcript here... You can get this from YouTube's CC or various transcript tools."
                                className="w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-500 h-48"
                            />
                        </div>

                        <button
                            onClick={handleGenerate}
                            disabled={loading || (!transcript.trim() && !title.trim())}
                            className="w-full py-3 bg-gradient-to-r from-rose-500 to-pink-500 text-white rounded-lg font-bold hover:from-rose-600 hover:to-pink-600 disabled:opacity-50"
                        >
                            {loading ? '✨ Generating Course...' : '🎓 Generate Course'}
                        </button>
                    </div>
                </div>
            )}

            {step === 'course' && course && (
                <div className="space-y-6">
                    {/* Course Header */}
                    <div className="bg-gradient-to-r from-rose-500 to-pink-500 rounded-xl p-6 text-white">
                        <h2 className="text-2xl font-bold">{course.course_title}</h2>
                        <div className="flex gap-4 mt-2 text-sm opacity-90">
                            <span>📚 {course.subject}</span>
                            <span>📊 {course.difficulty_level}</span>
                            <span>📖 {course.chapters?.length || 0} Chapters</span>
                        </div>
                    </div>

                    {/* Tabs */}
                    <div className="flex gap-2 bg-white rounded-xl p-2 shadow-lg">
                        {(['chapters', 'quiz', 'flashcards'] as const).map((tab) => (
                            <button
                                key={tab}
                                onClick={() => setActiveTab(tab)}
                                className={`flex-1 py-2 px-4 rounded-lg capitalize font-medium transition-all ${activeTab === tab
                                        ? 'bg-rose-500 text-white'
                                        : 'hover:bg-gray-100'
                                    }`}
                            >
                                {tab === 'chapters' && '📖 '}
                                {tab === 'quiz' && '❓ '}
                                {tab === 'flashcards' && '🃏 '}
                                {tab}
                            </button>
                        ))}
                    </div>

                    {/* Chapters Tab */}
                    {activeTab === 'chapters' && course.chapters && (
                        <div className="bg-white rounded-xl p-6 shadow-lg space-y-4">
                            {course.chapters.map((chapter, i) => (
                                <div key={i} className="p-4 border rounded-lg hover:bg-gray-50">
                                    <div className="flex items-center gap-3">
                                        <div className="w-8 h-8 bg-rose-500 text-white rounded-full flex items-center justify-center font-bold">
                                            {chapter.chapter_number}
                                        </div>
                                        <div className="flex-1">
                                            <h3 className="font-bold text-gray-800">{chapter.title}</h3>
                                            <p className="text-sm text-gray-500">{chapter.start_time} - {chapter.end_time}</p>
                                        </div>
                                    </div>
                                    <p className="mt-2 text-gray-600 ml-11">{chapter.summary}</p>
                                    {chapter.key_terms && (
                                        <div className="mt-2 ml-11 flex flex-wrap gap-2">
                                            {chapter.key_terms.map((term, j) => (
                                                <span key={j} className="text-xs bg-rose-100 text-rose-700 px-2 py-1 rounded">
                                                    {term}
                                                </span>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    )}

                    {/* Quiz Tab */}
                    {activeTab === 'quiz' && course.quiz?.mcq && (
                        <div className="bg-white rounded-xl p-6 shadow-lg">
                            {course.quiz.mcq.length > 0 && (
                                <div className="space-y-4">
                                    <div className="text-sm text-gray-500">
                                        Question {currentQuiz + 1} of {course.quiz.mcq.length}
                                    </div>

                                    <h3 className="text-lg font-bold text-gray-800">
                                        {course.quiz.mcq[currentQuiz].question}
                                    </h3>

                                    <div className="space-y-2">
                                        {course.quiz.mcq[currentQuiz].options.map((opt, i) => (
                                            <button
                                                key={i}
                                                onClick={() => setShowAnswer(true)}
                                                className={`w-full p-3 text-left rounded-lg border-2 transition-all ${showAnswer && course.quiz!.mcq[currentQuiz].correct === String.fromCharCode(65 + i)
                                                        ? 'border-green-500 bg-green-50'
                                                        : 'border-gray-200 hover:border-rose-300'
                                                    }`}
                                            >
                                                <span className="font-medium">{String.fromCharCode(65 + i)}.</span> {opt}
                                            </button>
                                        ))}
                                    </div>

                                    {showAnswer && (
                                        <div className="bg-green-50 p-4 rounded-lg border border-green-200">
                                            <p className="font-medium text-green-800">Explanation:</p>
                                            <p className="text-green-700">{course.quiz.mcq[currentQuiz].explanation}</p>
                                        </div>
                                    )}

                                    <div className="flex gap-4">
                                        <button
                                            onClick={() => { setCurrentQuiz(prev => Math.max(0, prev - 1)); setShowAnswer(false); }}
                                            disabled={currentQuiz === 0}
                                            className="flex-1 py-2 bg-gray-200 rounded-lg disabled:opacity-50"
                                        >
                                            ← Previous
                                        </button>
                                        <button
                                            onClick={() => { setCurrentQuiz(prev => Math.min(course.quiz!.mcq.length - 1, prev + 1)); setShowAnswer(false); }}
                                            disabled={currentQuiz >= course.quiz.mcq.length - 1}
                                            className="flex-1 py-2 bg-rose-500 text-white rounded-lg disabled:opacity-50"
                                        >
                                            Next →
                                        </button>
                                    </div>
                                </div>
                            )}
                        </div>
                    )}

                    {/* Flashcards Tab */}
                    {activeTab === 'flashcards' && course.flashcards && (
                        <div className="bg-white rounded-xl p-6 shadow-lg">
                            <div className="grid grid-cols-2 gap-4">
                                {course.flashcards.map((card, i) => (
                                    <div
                                        key={i}
                                        onClick={() => setFlippedCard(flippedCard === i ? null : i)}
                                        className={`p-4 rounded-lg border-2 cursor-pointer transition-all min-h-24 ${flippedCard === i
                                                ? 'border-rose-500 bg-rose-50'
                                                : 'border-gray-200 hover:border-rose-300'
                                            }`}
                                    >
                                        <p className="font-medium text-gray-800">
                                            {flippedCard === i ? card.back : card.front}
                                        </p>
                                        <p className="text-xs text-gray-500 mt-2">
                                            {flippedCard === i ? '(Click to flip back)' : '(Click to reveal)'}
                                        </p>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    <button
                        onClick={() => { setStep('input'); setCourse(null); }}
                        className="w-full py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
                    >
                        ← Process Another Video
                    </button>
                </div>
            )}
        </div>
    );
};
