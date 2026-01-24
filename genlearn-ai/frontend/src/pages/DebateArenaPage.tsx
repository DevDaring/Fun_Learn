import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { formatChatContent } from '../utils/helpers';

interface DebateTopic {
    topic: string;
    category: string;
}

interface RoundScore {
    student: number;
    ai: number;
    reasoning: string;
}

interface ChatMessage {
    role: 'user' | 'assistant';
    content: string;
    imageUrl?: string;
    roundScore?: RoundScore;
    nextRoundHint?: string;
    argumentType?: string;
}

export const DebateArenaPage: React.FC = () => {
    const [step, setStep] = useState<'setup' | 'debate'>('setup');
    const [topics, setTopics] = useState<DebateTopic[]>([]);
    const [selectedTopic, setSelectedTopic] = useState<DebateTopic | null>(null);
    const [position, setPosition] = useState<'YES' | 'NO' | null>(null);
    const [difficulty, setDifficulty] = useState<'casual' | 'challenging' | 'ruthless'>('casual');
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [userInput, setUserInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [roundNumber, setRoundNumber] = useState(1);
    const [scores, setScores] = useState({ student: 0, ai: 0 });

    useEffect(() => {
        loadTopics();
    }, []);

    const loadTopics = async () => {
        try {
            const response = await api.client.get('/features/debate/topics');
            setTopics(response.data.topics || []);
        } catch (err) {
            setTopics([
                { topic: "Should homework be abolished?", category: "Education" },
                { topic: "Is social media harmful for teenagers?", category: "Technology" },
                { topic: "Should AI replace teachers?", category: "Education" },
                { topic: "Is climate change the biggest threat?", category: "Society" },
            ]);
        }
    };

    const handleStartDebate = () => {
        if (!selectedTopic || !position) return;
        setStep('debate');
        setMessages([{
            role: 'assistant',
            content: `⚔️ **Welcome to the Debate Arena!**\n\nTopic: **${selectedTopic.topic}**\n\nYou are arguing: **${position}**\nI will argue: **${position === 'YES' ? 'NO' : 'YES'}**\nDifficulty: **${difficulty}**\n\nThis is a 5-round debate. Make your opening argument!\n\n*Your move, challenger!* 🎯`,
        }]);
    };

    const handleSendArgument = async () => {
        if (!userInput.trim() || !selectedTopic || !position) return;

        const argument = userInput;
        setUserInput('');
        setMessages(prev => [...prev, { role: 'user', content: argument }]);

        setLoading(true);
        try {
            const response = await api.client.post('/features/debate/round', {
                topic: selectedTopic.topic,
                student_position: position,
                user_message: argument,
                difficulty,
                round_number: roundNumber
            });

            const roundScore = response.data.round_score || { student: 0, ai: 0 };
            setScores(prev => ({
                student: prev.student + roundScore.student,
                ai: prev.ai + roundScore.ai
            }));
            setRoundNumber(prev => prev + 1);

            setMessages(prev => [...prev, {
                role: 'assistant',
                content: response.data.message || "Interesting point...",
                imageUrl: response.data.image_url,
                roundScore: roundScore,
                nextRoundHint: response.data.next_round_hint,
                argumentType: response.data.argument_type
            }]);
        } catch (err) {
            console.error('Debate failed:', err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            <div className="bg-white rounded-xl p-6 shadow-lg">
                <h1 className="text-3xl font-bold text-gray-900 mb-2">⚔️ Debate Arena</h1>
                <p className="text-gray-600">Take a position, and I'll argue the opposite. Build critical thinking!</p>
            </div>

            {step === 'setup' && (
                <div className="space-y-6">
                    <div className="bg-gradient-to-br from-red-50 to-orange-50 rounded-xl p-6">
                        <h2 className="text-xl font-bold text-gray-800 mb-4">Choose a Topic</h2>

                        {/* Custom Topic Input */}
                        <div className="mb-4">
                            <input
                                type="text"
                                value={selectedTopic?.category === 'Custom' ? selectedTopic.topic : ''}
                                onChange={(e) => {
                                    if (e.target.value.trim()) {
                                        setSelectedTopic({ topic: e.target.value, category: 'Custom' });
                                    } else {
                                        setSelectedTopic(null);
                                    }
                                }}
                                placeholder="✍️ Or enter your own debate topic..."
                                className="w-full px-4 py-3 rounded-lg border-2 border-dashed border-orange-300 focus:border-red-500 focus:outline-none bg-white"
                            />
                        </div>

                        <p className="text-sm text-gray-500 mb-3">Or choose from popular topics:</p>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                            {topics.map((t, idx) => (
                                <button
                                    key={idx}
                                    onClick={() => setSelectedTopic(t)}
                                    className={`p-4 rounded-lg border-2 text-left transition-all ${selectedTopic?.topic === t.topic && selectedTopic?.category !== 'Custom'
                                        ? 'border-red-500 bg-red-50'
                                        : 'border-gray-200 hover:border-red-300'
                                        }`}
                                >
                                    <span className="text-xs text-gray-500">{t.category}</span>
                                    <p className="font-medium text-gray-800">{t.topic}</p>
                                </button>
                            ))}
                        </div>
                    </div>

                    {selectedTopic && (
                        <div className="bg-white rounded-xl p-6 shadow-lg">
                            <h2 className="text-xl font-bold text-gray-800 mb-4">Choose Your Side</h2>
                            <div className="flex gap-4 mb-6">
                                <button
                                    onClick={() => setPosition('YES')}
                                    className={`flex-1 py-4 rounded-lg border-2 font-bold transition-all ${position === 'YES'
                                        ? 'border-green-500 bg-green-50 text-green-700'
                                        : 'border-gray-200 hover:border-green-300'
                                        }`}
                                >
                                    ✅ YES
                                </button>
                                <button
                                    onClick={() => setPosition('NO')}
                                    className={`flex-1 py-4 rounded-lg border-2 font-bold transition-all ${position === 'NO'
                                        ? 'border-red-500 bg-red-50 text-red-700'
                                        : 'border-gray-200 hover:border-red-300'
                                        }`}
                                >
                                    ❌ NO
                                </button>
                            </div>

                            <h3 className="font-medium text-gray-800 mb-2">Difficulty</h3>
                            <div className="flex gap-4 mb-6">
                                {(['casual', 'challenging', 'ruthless'] as const).map((d) => (
                                    <button
                                        key={d}
                                        onClick={() => setDifficulty(d)}
                                        className={`px-4 py-2 rounded-lg border-2 capitalize ${difficulty === d
                                            ? 'border-orange-500 bg-orange-50'
                                            : 'border-gray-200'
                                            }`}
                                    >
                                        {d === 'casual' && '😊 '}
                                        {d === 'challenging' && '💪 '}
                                        {d === 'ruthless' && '🔥 '}
                                        {d}
                                    </button>
                                ))}
                            </div>

                            <button
                                onClick={handleStartDebate}
                                disabled={!position}
                                className="w-full py-3 bg-gradient-to-r from-red-500 to-orange-500 text-white rounded-lg font-bold hover:from-red-600 hover:to-orange-600 disabled:opacity-50"
                            >
                                ⚔️ Start Debate - 5 Rounds
                            </button>
                        </div>
                    )}
                </div>
            )}

            {step === 'debate' && selectedTopic && (
                <div className="bg-white rounded-xl shadow-lg overflow-hidden">
                    <div className="bg-gradient-to-r from-red-500 to-orange-500 text-white p-4 flex justify-between items-center">
                        <div>
                            <h2 className="font-bold">Round {Math.min(roundNumber, 5)} of 5</h2>
                            <p className="text-sm opacity-80">{selectedTopic.topic}</p>
                        </div>
                        <div className="flex gap-4 text-center">
                            <div>
                                <div className="text-2xl font-bold">{scores.student}</div>
                                <div className="text-xs opacity-80">You</div>
                            </div>
                            <div className="text-2xl">vs</div>
                            <div>
                                <div className="text-2xl font-bold">{scores.ai}</div>
                                <div className="text-xs opacity-80">AI</div>
                            </div>
                        </div>
                    </div>

                    <div className="h-96 overflow-y-auto p-4 space-y-4">
                        {messages.map((msg, idx) => (
                            <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                <div className={`max-w-3/4 p-3 rounded-lg ${msg.role === 'user'
                                    ? 'bg-green-500 text-white'
                                    : 'bg-gray-100 text-gray-800'
                                    }`}>
                                    <div dangerouslySetInnerHTML={{ __html: formatChatContent(msg.content) }} />

                                    {msg.roundScore && (
                                        <div className="mt-2 pt-2 border-t border-gray-200 text-xs">
                                            <p>Round Score: You {msg.roundScore.student} - AI {msg.roundScore.ai}</p>
                                            <p className="text-gray-500 italic">{msg.roundScore.reasoning}</p>
                                        </div>
                                    )}

                                    {msg.nextRoundHint && (
                                        <p className="mt-2 text-xs text-blue-600">💡 Hint: {msg.nextRoundHint}</p>
                                    )}
                                </div>
                            </div>
                        ))}
                        {loading && (
                            <div className="flex justify-start">
                                <div className="bg-gray-100 p-3 rounded-lg animate-pulse">
                                    🤔 Preparing counterargument...
                                </div>
                            </div>
                        )}
                    </div>

                    <div className="p-4 border-t flex gap-2">
                        <input
                            type="text"
                            value={userInput}
                            onChange={(e) => setUserInput(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && handleSendArgument()}
                            placeholder="Make your argument..."
                            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
                            disabled={roundNumber > 5}
                        />
                        <button
                            onClick={handleSendArgument}
                            disabled={loading || roundNumber > 5}
                            className="px-6 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 disabled:opacity-50"
                        >
                            Argue
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};
