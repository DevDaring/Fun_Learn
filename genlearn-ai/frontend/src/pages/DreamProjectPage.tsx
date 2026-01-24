import React, { useState } from 'react';
import api from '../services/api';

interface SkillRequired {
    skill: string;
    category: string;
    importance: string;
    why_needed: string;
}

interface Phase {
    phase_number: number;
    phase_name: string;
    duration: string;
    topics: { subject: string; topic: string; hours: number }[];
    milestone: string;
    checkpoint_project: string;
}

interface DreamAnalysis {
    dream_analysis: {
        dream_title: string;
        reality_check: string;
        career_paths: string[];
    };
    skills_required: SkillRequired[];
    learning_path: {
        total_duration: string;
        phases: Phase[];
    };
    motivation: {
        why_achievable: string;
        first_step: string;
    };
}

export const DreamProjectPage: React.FC = () => {
    const [step, setStep] = useState<'input' | 'result'>('input');
    const [dream, setDream] = useState('');
    const [gradeLevel, setGradeLevel] = useState(10);
    const [hoursPerWeek, setHoursPerWeek] = useState(5);
    const [analysis, setAnalysis] = useState<DreamAnalysis | null>(null);
    const [loading, setLoading] = useState(false);

    const handleAnalyze = async () => {
        if (!dream.trim()) return;

        setLoading(true);
        try {
            const response = await api.client.post('/features/dream/analyze', {
                dream,
                grade_level: gradeLevel,
                hours_per_week: hoursPerWeek
            });

            setAnalysis(response.data);
            setStep('result');
        } catch (err) {
            console.error('Analysis failed:', err);
            alert('Failed to analyze dream project. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            <div className="bg-white rounded-xl p-6 shadow-lg">
                <h1 className="text-3xl font-bold text-gray-900 mb-2">🎯 Dream Project Path</h1>
                <p className="text-gray-600">Tell us your dream, and we'll create a personalized learning path to achieve it!</p>
            </div>

            {step === 'input' && (
                <div className="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-xl p-8">
                    <div className="mb-6">
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            What do you dream of building/creating/achieving?
                        </label>
                        <textarea
                            value={dream}
                            onChange={(e) => setDream(e.target.value)}
                            placeholder="e.g., I want to build a Mars rover, create a popular video game, start a tech company..."
                            className="w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 h-32 resize-none"
                        />
                    </div>

                    <div className="grid grid-cols-2 gap-4 mb-6">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Current Grade/Level
                            </label>
                            <select
                                value={gradeLevel}
                                onChange={(e) => setGradeLevel(Number(e.target.value))}
                                className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                            >
                                <optgroup label="School">
                                    {[6, 7, 8, 9, 10, 11, 12].map(g => (
                                        <option key={g} value={g}>Class {g}</option>
                                    ))}
                                </optgroup>
                                <optgroup label="Higher Education">
                                    <option value={13}>Undergraduate (1st Year)</option>
                                    <option value={14}>Undergraduate (2nd Year)</option>
                                    <option value={15}>Undergraduate (3rd Year)</option>
                                    <option value={16}>Undergraduate (Final Year)</option>
                                    <option value={17}>Post-Graduate (Masters)</option>
                                    <option value={18}>PhD / Research Scholar</option>
                                </optgroup>
                                <optgroup label="Professional">
                                    <option value={19}>Working Professional (0-2 years)</option>
                                    <option value={20}>Working Professional (3-5 years)</option>
                                    <option value={21}>Working Professional (5+ years)</option>
                                </optgroup>
                            </select>
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Available Time Per Week
                            </label>
                            <select
                                value={hoursPerWeek}
                                onChange={(e) => setHoursPerWeek(Number(e.target.value))}
                                className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                            >
                                {[2, 3, 5, 7, 10, 15].map(h => (
                                    <option key={h} value={h}>{h} hours/week</option>
                                ))}
                            </select>
                        </div>
                    </div>

                    <button
                        onClick={handleAnalyze}
                        disabled={!dream.trim() || loading}
                        className="w-full py-3 bg-gradient-to-r from-indigo-500 to-purple-500 text-white rounded-lg font-bold hover:from-indigo-600 hover:to-purple-600 disabled:opacity-50"
                    >
                        {loading ? '🔮 Analyzing your dream...' : '🚀 Generate My Learning Path'}
                    </button>
                </div>
            )}

            {step === 'result' && analysis && (
                <div className="space-y-6">
                    {/* Dream Title */}
                    <div className="bg-gradient-to-r from-indigo-500 to-purple-500 rounded-xl p-6 text-white">
                        <h2 className="text-2xl font-bold">🌟 {analysis.dream_analysis?.dream_title || 'Your Dream'}</h2>
                        <p className="mt-2 opacity-90">{analysis.dream_analysis?.reality_check}</p>
                        {analysis.dream_analysis?.career_paths && (
                            <div className="mt-4 flex flex-wrap gap-2">
                                {analysis.dream_analysis.career_paths.map((path, i) => (
                                    <span key={i} className="px-3 py-1 bg-white/20 rounded-full text-sm">{path}</span>
                                ))}
                            </div>
                        )}
                    </div>

                    {/* Skills Required */}
                    {analysis.skills_required && (
                        <div className="bg-white rounded-xl p-6 shadow-lg">
                            <h3 className="text-xl font-bold text-gray-800 mb-4">🛠️ Skills You'll Need</h3>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                {analysis.skills_required.map((skill, i) => (
                                    <div key={i} className="p-3 bg-gray-50 rounded-lg border">
                                        <div className="flex justify-between items-start">
                                            <span className="font-medium text-gray-800">{skill.skill}</span>
                                            <span className={`text-xs px-2 py-1 rounded ${skill.importance === 'Critical' ? 'bg-red-100 text-red-700' : 'bg-yellow-100 text-yellow-700'
                                                }`}>{skill.importance}</span>
                                        </div>
                                        <p className="text-sm text-gray-600 mt-1">{skill.why_needed}</p>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Learning Path */}
                    {analysis.learning_path && (
                        <div className="bg-white rounded-xl p-6 shadow-lg">
                            <h3 className="text-xl font-bold text-gray-800 mb-4">
                                📚 Your Learning Path ({analysis.learning_path.total_duration})
                            </h3>
                            <div className="space-y-4">
                                {analysis.learning_path.phases?.map((phase, i) => (
                                    <div key={i} className="p-4 border rounded-lg">
                                        <div className="flex items-center gap-3 mb-2">
                                            <div className="w-8 h-8 bg-indigo-500 text-white rounded-full flex items-center justify-center font-bold">
                                                {phase.phase_number}
                                            </div>
                                            <div>
                                                <h4 className="font-bold text-gray-800">{phase.phase_name}</h4>
                                                <span className="text-sm text-gray-500">{phase.duration}</span>
                                            </div>
                                        </div>

                                        {phase.topics && (
                                            <div className="ml-11 space-y-1">
                                                {phase.topics.map((t, j) => (
                                                    <div key={j} className="text-sm text-gray-600">
                                                        📖 {t.subject}: {t.topic} ({t.hours}h)
                                                    </div>
                                                ))}
                                            </div>
                                        )}

                                        <div className="ml-11 mt-2 text-sm">
                                            <p className="text-green-600">🎯 Milestone: {phase.milestone}</p>
                                            <p className="text-blue-600">🔧 Project: {phase.checkpoint_project}</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Motivation */}
                    {analysis.motivation && (
                        <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-6 border border-green-200">
                            <h3 className="text-lg font-bold text-green-800 mb-2">💪 You Can Do This!</h3>
                            <p className="text-green-700 mb-4">{analysis.motivation.why_achievable}</p>
                            <div className="bg-white p-4 rounded-lg border border-green-300">
                                <p className="font-medium text-green-800">🚀 First Step (Do This TODAY!):</p>
                                <p className="text-green-700">{analysis.motivation.first_step}</p>
                            </div>
                        </div>
                    )}

                    <button
                        onClick={() => setStep('input')}
                        className="w-full py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
                    >
                        ← Try Another Dream
                    </button>
                </div>
            )}
        </div>
    );
};
