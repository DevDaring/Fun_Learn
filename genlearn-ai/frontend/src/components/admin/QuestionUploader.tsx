import React, { useState, useRef } from 'react';
import { Button } from '../common/Button';
import api from '../../services/api';

export const QuestionUploader: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [questionType, setQuestionType] = useState<'mcq' | 'descriptive'>('mcq');
  const [isUploading, setIsUploading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
      setError(null);
      setResult(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setIsUploading(true);
    setError(null);
    setResult(null);

    try {
      const data = await api.uploadQuestions(selectedFile, questionType);
      setResult(data);
      setSelectedFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to upload questions');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Upload Questions</h2>

      {/* Question Type Selection */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Question Type
        </label>
        <div className="grid grid-cols-2 gap-4">
          <button
            onClick={() => setQuestionType('mcq')}
            className={`p-4 border-2 rounded-lg transition-colors ${
              questionType === 'mcq'
                ? 'border-primary-600 bg-primary-50'
                : 'border-gray-300 hover:border-gray-400'
            }`}
          >
            <h3 className="font-semibold text-gray-900 mb-1">Multiple Choice (MCQ)</h3>
            <p className="text-sm text-gray-600">Questions with A, B, C, D options</p>
          </button>

          <button
            onClick={() => setQuestionType('descriptive')}
            className={`p-4 border-2 rounded-lg transition-colors ${
              questionType === 'descriptive'
                ? 'border-primary-600 bg-primary-50'
                : 'border-gray-300 hover:border-gray-400'
            }`}
          >
            <h3 className="font-semibold text-gray-900 mb-1">Descriptive</h3>
            <p className="text-sm text-gray-600">Open-ended text questions</p>
          </button>
        </div>
      </div>

      {/* File Upload */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          CSV File
        </label>
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
        />
        {selectedFile && (
          <p className="mt-2 text-sm text-gray-600">
            Selected: {selectedFile.name} ({(selectedFile.size / 1024).toFixed(2)} KB)
          </p>
        )}
      </div>

      {/* CSV Format Info */}
      <div className="mb-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 className="font-semibold text-blue-900 mb-2 flex items-center">
          <svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          CSV Format
        </h4>
        {questionType === 'mcq' ? (
          <div className="text-sm text-blue-800">
            <p className="mb-2">Required columns:</p>
            <ul className="list-disc list-inside space-y-1 ml-2">
              <li>question_text</li>
              <li>option_a, option_b, option_c, option_d</li>
              <li>correct_answer (A, B, C, or D)</li>
              <li>explanation</li>
              <li>difficulty_level (1-10)</li>
              <li>topic</li>
            </ul>
          </div>
        ) : (
          <div className="text-sm text-blue-800">
            <p className="mb-2">Required columns:</p>
            <ul className="list-disc list-inside space-y-1 ml-2">
              <li>question_text</li>
              <li>sample_answer</li>
              <li>max_score</li>
              <li>difficulty_level (1-10)</li>
              <li>topic</li>
            </ul>
          </div>
        )}
      </div>

      {/* Error Message */}
      {error && (
        <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
          {error}
        </div>
      )}

      {/* Success Message */}
      {result && (
        <div className="mb-6 bg-green-50 border border-green-200 rounded-lg p-4">
          <h4 className="font-semibold text-green-900 mb-2 flex items-center">
            <svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Upload Successful
          </h4>
          <p className="text-sm text-green-800">
            Successfully uploaded {result.count || 0} questions.
          </p>
        </div>
      )}

      {/* Upload Button */}
      <Button
        onClick={handleUpload}
        disabled={!selectedFile || isUploading}
        isLoading={isUploading}
        variant="primary"
        className="w-full"
      >
        <svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
        </svg>
        Upload Questions
      </Button>

      {/* Download Template */}
      <div className="mt-4 text-center">
        <button className="text-sm text-primary-600 hover:text-primary-700 font-medium">
          Download CSV Template
        </button>
      </div>
    </div>
  );
};
