import React, { useState, useRef, useEffect } from 'react';
import api from '../services/api';
import { formatChatContent } from '../utils/helpers';

interface Diagnosis {
    most_likely_error: string;
    confidence: string;
    error_category: string;
    thought_process_reconstruction: string;
    misconception_identified: string;
}

interface Remediation {
    quick_fix: string;
    practice_problems: { question: string; focus: string }[];
}

interface AnalysisResult {
    diagnosis: Diagnosis;
    message: string;
    remediation: Remediation;
    encouragement: string;
    imageUrl?: string;
}

interface MCTMessage {
    role: 'user' | 'assistant';
    content: string;
    phase?: string;
    diagnosticQuestion?: string;
    imageUrl?: string;
}

interface CascadeTracking {
    surface_error: string;
    tested_prerequisites: string[];
    broken_link_found: boolean;
    root_misconception: string | null;
    repair_progress: string[];
}

export const MistakeAutopsyPage: React.FC = () => {
    const [mode, setMode] = useState<'input' | 'basic_result' | 'mct_chat'>('input');
    const [question, setQuestion] = useState('');
    const [correctAnswer, setCorrectAnswer] = useState('');
    const [studentAnswer, setStudentAnswer] = useState('');
    const [subject, setSubject] = useState('Mathematics');
    const [topic, setTopic] = useState('');
    const [result, setResult] = useState<AnalysisResult | null>(null);
    const [loading, setLoading] = useState(false);

    // MCT Chat State
    const [mctMessages, setMctMessages] = useState<MCTMessage[]>([]);
    const [mctInput, setMctInput] = useState('');
    const [mctSessionId, setMctSessionId] = useState<string | null>(null);
    const [currentPhase, setCurrentPhase] = useState('surface_capture');
    const [cascadeTracking, setCascadeTracking] = useState<CascadeTracking>({
        surface_error: '',
        tested_prerequisites: [],
        broken_link_found: false,
        root_misconception: null,
        repair_progress: []
    });
    const chatEndRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [mctMessages]);

    const handleBasicAnalyze = async () => {
        if (!question.trim() || !correctAnswer.trim() || !studentAnswer.trim()) return;

        setLoading(true);
        try {
            const response = await api.client.post('/features/mistake/analyze', {
                question,
                correct_answer: correctAnswer,
                student_answer: studentAnswer,
                subject,
                topic: topic || subject
            });

            setResult(response.data);
            setMode('basic_result');
        } catch (err) {
            console.error('Analysis failed:', err);
            alert('Failed to analyze mistake. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleStartMCT = async () => {
        if (!question.trim() || !correctAnswer.trim() || !studentAnswer.trim()) return;

        setLoading(true);
        try {
            const response = await api.client.post('/features/mct/start', {
                question,
                correct_answer: correctAnswer,
                student_answer: studentAnswer,
                subject,
                topic: topic || subject
            });

            setMctSessionId(response.data.session_id);
            setCurrentPhase(response.data.phase || 'surface_capture');
            setCascadeTracking(response.data.cascade_tracking || cascadeTracking);

            setMctMessages([{
                role: 'assistant',
                content: response.data.message || "Let's explore what happened with your answer...",
                phase: response.data.phase,
                diagnosticQuestion: response.data.diagnostic_question
            }]);

            setMode('mct_chat');
        } catch (err) {
            console.error('MCT start failed:', err);
            alert('Failed to start MCT session. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleMCTSend = async () => {
        if (!mctInput.trim()) return;

        const userMessage = mctInput;
        setMctInput('');
        setMctMessages(prev => [...prev, { role: 'user', content: userMessage }]);

        setLoading(true);
        try {
            // Build conversation history for context
            const conversationHistory = mctMessages.map(m => ({
                role: m.role,
                content: m.content
            }));

            const response = await api.client.post('/features/mct/chat', {
                question,
                correct_answer: correctAnswer,
                student_answer: studentAnswer,
                subject,
                topic: topic || subject,
                user_message: userMessage,
                session_id: mctSessionId,
                conversation_history: conversationHistory,
                phase: currentPhase,
                cascade_tracking: cascadeTracking
            });

            // Update phase and tracking
            if (response.data.phase) setCurrentPhase(response.data.phase);
            if (response.data.cascade_tracking) setCascadeTracking(response.data.cascade_tracking);

            setMctMessages(prev => [...prev, {
                role: 'assistant',
                content: response.data.message || "I see...",
                phase: response.data.phase,
                diagnosticQuestion: response.data.diagnostic_question,
                imageUrl: response.data.image_url
            }]);
        } catch (err) {
            console.error('MCT chat failed:', err);
            setMctMessages(prev => [...prev, {
                role: 'assistant',
                content: "I encountered an issue. Let's try that again."
            }]);
        } finally {
            setLoading(false);
        }
    };

    const getPhaseLabel = (phase: string) => {
        const phases: Record<string, { label: string; color: string; icon: string }> = {
            'surface_capture': { label: 'Analyzing', color: 'bg-blue-500', icon: '🔍' },
            'diagnostic_probing': { label: 'Probing', color: 'bg-yellow-500', icon: '🧐' },
            'root_found': { label: 'Root Found!', color: 'bg-orange-500', icon: '🎯' },
            'remediation': { label: 'Repairing', color: 'bg-green-500', icon: '🔧' },
            'verification': { label: 'Verifying', color: 'bg-purple-500', icon: '✅' }
        };
        return phases[phase] || { label: phase, color: 'bg-gray-500', icon: '📝' };
    };

    const resetToInput = () => {
        setMode('input');
        setResult(null);
        setMctMessages([]);
        setMctSessionId(null);
        setCurrentPhase('surface_capture');
        setCascadeTracking({
            surface_error: '',
            tested_prerequisites: [],
            broken_link_found: false,
            root_misconception: null,
            repair_progress: []
        });
    };

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            <div className="bg-white rounded-xl p-6 shadow-lg">
                <h1 className="text-3xl font-bold text-gray-900 mb-2">🔬 Mistake Autopsy + MCT</h1>
                <p className="text-gray-600">
                    Understand WHY you made a mistake and trace it to its root cause!
                </p>
            </div>

            {mode === 'input' && (
                <div className="bg-gradient-to-br from-teal-50 to-cyan-50 rounded-xl p-6">
                    <h2 className="text-xl font-bold text-gray-800 mb-4">Enter the Mistake Details</h2>

                    <div className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Question</label>
                            <textarea
                                value={question}
                                onChange={(e) => setQuestion(e.target.value)}
                                placeholder="e.g., Solve: x² + 5x + 6 = 0"
                                className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
                                rows={2}
                            />
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Your Answer</label>
                                <input
                                    type="text"
                                    value={studentAnswer}
                                    onChange={(e) => setStudentAnswer(e.target.value)}
                                    placeholder="e.g., x = -2, x = -4"
                                    className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Correct Answer</label>
                                <input
                                    type="text"
                                    value={correctAnswer}
                                    onChange={(e) => setCorrectAnswer(e.target.value)}
                                    placeholder="e.g., x = -2, x = -3"
                                    className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                                />
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Subject</label>
                                <select
                                    value={subject}
                                    onChange={(e) => setSubject(e.target.value)}
                                    className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
                                >
                                    <option>Mathematics</option>
                                    <option>Physics</option>
                                    <option>Chemistry</option>
                                    <option>Biology</option>
                                    <option>History</option>
                                    <option>Geography</option>
                                    <option>English</option>
                                </select>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Topic (Optional)</label>
                                <input
                                    type="text"
                                    value={topic}
                                    onChange={(e) => setTopic(e.target.value)}
                                    placeholder="e.g., Quadratic Equations"
                                    className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
                                />
                            </div>
                        </div>

                        {/* Two Analysis Options */}
                        <div className="grid grid-cols-2 gap-4 pt-4">
                            <button
                                onClick={handleBasicAnalyze}
                                disabled={loading || !question || !correctAnswer || !studentAnswer}
                                className="py-3 bg-gradient-to-r from-teal-500 to-cyan-500 text-white rounded-lg font-bold hover:from-teal-600 hover:to-cyan-600 disabled:opacity-50"
                            >
                                {loading ? '🔬 Analyzing...' : '🔬 Quick Autopsy'}
                            </button>
                            <button
                                onClick={handleStartMCT}
                                disabled={loading || !question || !correctAnswer || !studentAnswer}
                                className="py-3 bg-gradient-to-r from-purple-500 to-indigo-500 text-white rounded-lg font-bold hover:from-purple-600 hover:to-indigo-600 disabled:opacity-50"
                            >
                                {loading ? '🧠 Starting...' : '🧠 Deep MCT Session'}
                            </button>
                        </div>
                        <p className="text-sm text-gray-500 text-center">
                            <strong>Quick Autopsy:</strong> Fast single analysis | <strong>MCT Session:</strong> Interactive deep-dive to root cause
                        </p>
                    </div>
                </div>
            )}

            {/* Basic Result Mode */}
            {mode === 'basic_result' && result && (
                <div className="space-y-4">
                    <div className="bg-white rounded-xl p-6 shadow-lg">
                        <h3 className="text-xl font-bold text-red-600 mb-4">🐛 Bug Found in Your Brain!</h3>
                        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
                            <p className="font-medium text-red-800">Error Type: {result.diagnosis?.error_category || 'Unknown'}</p>
                            <p className="text-red-700 mt-1">{result.diagnosis?.most_likely_error}</p>
                        </div>
                        {result.diagnosis?.misconception_identified && (
                            <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
                                <p className="font-medium text-orange-800">The Wrong Belief:</p>
                                <p className="text-orange-700 mt-1">{result.diagnosis.misconception_identified}</p>
                            </div>
                        )}
                    </div>

                    <div className="bg-white rounded-xl p-6 shadow-lg">
                        <div className="flex justify-between items-center mb-4">
                            <h3 className="text-xl font-bold text-gray-800">📝 Explanation</h3>
                            <button
                                onClick={handleStartMCT}
                                className="px-4 py-2 bg-purple-500 text-white rounded-lg text-sm hover:bg-purple-600"
                            >
                                🧠 Go Deeper with MCT
                            </button>
                        </div>
                        <div
                            className="prose prose-sm max-w-none"
                            dangerouslySetInnerHTML={{
                                __html: formatChatContent(result.message || '')
                            }}
                        />
                    </div>

                    <button onClick={resetToInput} className="w-full py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300">
                        ← Try Another Problem
                    </button>
                </div>
            )}

            {/* MCT Chat Mode */}
            {mode === 'mct_chat' && (
                <div className="bg-white rounded-xl shadow-lg overflow-hidden">
                    {/* Header with Phase Progress */}
                    <div className="bg-gradient-to-r from-purple-600 to-indigo-600 text-white p-4">
                        <div className="flex justify-between items-center">
                            <div>
                                <h2 className="font-bold">🧠 Misconception Cascade Tracing</h2>
                                <p className="text-sm opacity-80 truncate max-w-md">{question}</p>
                            </div>
                            <div className="text-right">
                                <div className={`px-3 py-1 rounded-full text-sm ${getPhaseLabel(currentPhase).color}`}>
                                    {getPhaseLabel(currentPhase).icon} {getPhaseLabel(currentPhase).label}
                                </div>
                            </div>
                        </div>

                        {/* Cascade Progress Bar */}
                        <div className="mt-3 flex gap-1">
                            {['surface_capture', 'diagnostic_probing', 'root_found', 'remediation', 'verification'].map((phase, idx) => (
                                <div
                                    key={phase}
                                    className={`h-2 flex-1 rounded ${['surface_capture', 'diagnostic_probing', 'root_found', 'remediation', 'verification']
                                        .indexOf(currentPhase) >= idx
                                        ? 'bg-white'
                                        : 'bg-white/30'
                                        }`}
                                />
                            ))}
                        </div>
                    </div>

                    {/* Root Found Banner */}
                    {cascadeTracking.broken_link_found && cascadeTracking.root_misconception && (
                        <div className="bg-orange-100 border-b border-orange-200 p-3 text-center">
                            <p className="text-orange-800 font-medium">
                                🎯 Root Misconception Found: <strong>{cascadeTracking.root_misconception}</strong>
                            </p>
                        </div>
                    )}

                    {/* Chat Messages */}
                    <div className="h-96 overflow-y-auto p-4 space-y-4">
                        {mctMessages.map((msg, idx) => (
                            <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                <div className={`max-w-[80%] p-3 rounded-lg ${msg.role === 'user'
                                    ? 'bg-purple-500 text-white'
                                    : 'bg-gray-100 text-gray-800'
                                    }`}>
                                    <div dangerouslySetInnerHTML={{
                                        __html: formatChatContent(msg.content)
                                    }} />

                                    {msg.diagnosticQuestion && msg.role === 'assistant' && (
                                        <div className="mt-2 pt-2 border-t border-gray-200">
                                            <p className="text-sm font-medium text-purple-700">
                                                🤔 {msg.diagnosticQuestion}
                                            </p>
                                        </div>
                                    )}

                                    {msg.imageUrl && (
                                        <img
                                            src={`http://localhost:8000${msg.imageUrl}`}
                                            alt="Explanation"
                                            className="mt-2 rounded-lg max-w-full"
                                        />
                                    )}
                                </div>
                            </div>
                        ))}
                        {loading && (
                            <div className="flex justify-start">
                                <div className="bg-gray-100 p-3 rounded-lg animate-pulse">
                                    🧠 Analyzing your thinking...
                                </div>
                            </div>
                        )}
                        <div ref={chatEndRef} />
                    </div>

                    {/* Input */}
                    <div className="p-4 border-t flex gap-2">
                        <input
                            type="text"
                            value={mctInput}
                            onChange={(e) => setMctInput(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && handleMCTSend()}
                            placeholder="Answer the question or explain your thinking..."
                            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                            disabled={loading}
                        />
                        <button
                            onClick={handleMCTSend}
                            disabled={loading || !mctInput.trim()}
                            className="px-6 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 disabled:opacity-50"
                        >
                            Send
                        </button>
                    </div>

                    {/* Footer with Reset */}
                    <div className="p-2 border-t bg-gray-50 text-center">
                        <button onClick={resetToInput} className="text-sm text-gray-500 hover:text-gray-700">
                            ← Start Over with New Problem
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};
