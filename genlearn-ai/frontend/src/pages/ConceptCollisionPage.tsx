import React, { useState } from 'react';
import api from '../services/api';

interface Topic {
    name: string;
    subject: string;
    learned_date?: string;
}

interface Connection {
    topic1: Topic;
    topic2: Topic;
    connection_title: string;
    hook: string;
    brief_explanation: string;
    mind_blown_fact?: string;
}

interface ConnectionsResult {
    connections: Connection[];
    weekly_theme?: string;
}

export const ConceptCollisionPage: React.FC = () => {
    const [topics, setTopics] = useState<Topic[]>([
        { name: 'Compound Interest', subject: 'Mathematics', learned_date: 'Jan 15' },
        { name: 'Bacterial Growth', subject: 'Biology', learned_date: 'Jan 12' },
    ]);
    const [newTopic, setNewTopic] = useState({ name: '', subject: 'Mathematics' });
    const [result, setResult] = useState<ConnectionsResult | null>(null);
    const [loading, setLoading] = useState(false);
    const [expandedConnection, setExpandedConnection] = useState<number | null>(null);

    const handleAddTopic = () => {
        if (!newTopic.name.trim()) return;
        setTopics(prev => [...prev, { ...newTopic, learned_date: 'Today' }]);
        setNewTopic({ name: '', subject: 'Mathematics' });
    };

    const handleRemoveTopic = (index: number) => {
        setTopics(prev => prev.filter((_, i) => i !== index));
    };

    const handleFindConnections = async () => {
        if (topics.length < 2) {
            alert('Please add at least 2 topics to find connections!');
            return;
        }

        setLoading(true);
        try {
            const response = await api.client.post('/features/concepts/find-connections', {
                topics: topics
            });

            setResult(response.data);
        } catch (err) {
            console.error('Failed to find connections:', err);
            alert('Failed to find connections. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const subjects = ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'History', 'Geography', 'Economics', 'Computer Science'];

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            <div className="bg-white rounded-xl p-6 shadow-lg">
                <h1 className="text-3xl font-bold text-gray-900 mb-2">🔗 Concept Collision</h1>
                <p className="text-gray-600">Discover mind-blowing connections between topics you've learned!</p>
            </div>

            {/* Topics List */}
            <div className="bg-gradient-to-br from-violet-50 to-purple-50 rounded-xl p-6">
                <h2 className="text-xl font-bold text-gray-800 mb-4">Your Recent Topics</h2>

                <div className="flex flex-wrap gap-2 mb-4">
                    {topics.map((topic, idx) => (
                        <div
                            key={idx}
                            className="bg-white px-4 py-2 rounded-full border-2 border-violet-200 flex items-center gap-2"
                        >
                            <span className="font-medium text-gray-800">{topic.name}</span>
                            <span className="text-sm text-violet-600">({topic.subject})</span>
                            <button
                                onClick={() => handleRemoveTopic(idx)}
                                className="text-gray-400 hover:text-red-500"
                            >
                                ✕
                            </button>
                        </div>
                    ))}
                </div>

                <div className="flex gap-2">
                    <input
                        type="text"
                        value={newTopic.name}
                        onChange={(e) => setNewTopic(prev => ({ ...prev, name: e.target.value }))}
                        placeholder="Add a topic you've learned..."
                        className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-violet-500"
                        onKeyPress={(e) => e.key === 'Enter' && handleAddTopic()}
                    />
                    <select
                        value={newTopic.subject}
                        onChange={(e) => setNewTopic(prev => ({ ...prev, subject: e.target.value }))}
                        className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-violet-500"
                    >
                        {subjects.map(s => (
                            <option key={s} value={s}>{s}</option>
                        ))}
                    </select>
                    <button
                        onClick={handleAddTopic}
                        disabled={!newTopic.name.trim()}
                        className="px-4 py-2 bg-violet-500 text-white rounded-lg hover:bg-violet-600 disabled:opacity-50"
                    >
                        Add
                    </button>
                </div>

                <button
                    onClick={handleFindConnections}
                    disabled={loading || topics.length < 2}
                    className="w-full mt-4 py-3 bg-gradient-to-r from-violet-500 to-purple-500 text-white rounded-lg font-bold hover:from-violet-600 hover:to-purple-600 disabled:opacity-50"
                >
                    {loading ? '🔮 Finding Connections...' : '🔗 Find Mind-Blowing Connections'}
                </button>
            </div>

            {/* Results */}
            {result && (
                <div className="space-y-4">
                    {result.weekly_theme && (
                        <div className="bg-gradient-to-r from-violet-500 to-purple-500 rounded-xl p-4 text-white text-center">
                            <p className="text-lg">{result.weekly_theme}</p>
                        </div>
                    )}

                    {result.connections && result.connections.map((conn, idx) => (
                        <div
                            key={idx}
                            className="bg-white rounded-xl shadow-lg overflow-hidden cursor-pointer"
                            onClick={() => setExpandedConnection(expandedConnection === idx ? null : idx)}
                        >
                            <div className="p-6">
                                <div className="flex items-center justify-center gap-4 mb-4">
                                    <div className="text-center p-4 bg-violet-50 rounded-lg">
                                        <p className="text-sm text-violet-600">{conn.topic1.subject}</p>
                                        <p className="font-bold text-gray-800">{conn.topic1.name}</p>
                                    </div>
                                    <div className="text-3xl">🔗</div>
                                    <div className="text-center p-4 bg-purple-50 rounded-lg">
                                        <p className="text-sm text-purple-600">{conn.topic2.subject}</p>
                                        <p className="font-bold text-gray-800">{conn.topic2.name}</p>
                                    </div>
                                </div>

                                <h3 className="text-xl font-bold text-center text-gray-800 mb-2">
                                    {conn.connection_title}
                                </h3>

                                <p className="text-center text-violet-600 font-medium">
                                    🤯 {conn.hook}
                                </p>
                            </div>

                            {expandedConnection === idx && (
                                <div className="border-t p-6 bg-gradient-to-br from-violet-50 to-purple-50">
                                    <p className="text-gray-700 mb-4">{conn.brief_explanation}</p>

                                    {conn.mind_blown_fact && (
                                        <div className="bg-white p-4 rounded-lg border border-violet-200">
                                            <p className="text-sm text-violet-600 font-medium">🤯 Mind-Blown Fact:</p>
                                            <p className="text-gray-800">{conn.mind_blown_fact}</p>
                                        </div>
                                    )}
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};
